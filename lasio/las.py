from __future__ import print_function

# Standard library packages
import codecs
import csv
import json
import logging
import os
import re
import sys
import textwrap
import traceback

# get basestring in py3

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    unicode = str
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    bytes = str
    basestring = basestring

# Required third-party packages available on PyPi:

import numpy as np

# internal lasio imports

from . import exceptions
from .las_items import HeaderItem, CurveItem, SectionItems, OrderedDict
from . import defaults
from . import reader
from . import writer

logger = logging.getLogger(__name__)


class LASFile(object):

    """LAS file object.

    Keyword Arguments:
        file_ref (file-like object, str): either a filename, an open file
            object, or a string containing the contents of a file.

    See these routines for additional keyword arguments you can use when
    reading in a LAS file:

    * :func:`lasio.reader.open_with_codecs` - manage issues relate to character
      encodings
    * :meth:`lasio.las.LASFile.read` - control how NULL values and errors are
      handled during parsing

    Attributes:
        encoding (str or None): the character encoding used when reading the
            file in from disk

    """

    def __init__(self, file_ref=None, **read_kwargs):
        super(LASFile, self).__init__()
        self._text = ""
        self.index_unit = None
        default_items = defaults.get_default_items()
        self.sections = {
            "Version": default_items["Version"],
            "Well": default_items["Well"],
            "Curves": default_items["Curves"],
            "Parameter": default_items["Parameter"],
            "Other": str(default_items["Other"]),
        }

        if not (file_ref is None):
            self.read(file_ref, **read_kwargs)

    def read(
        self,
        file_ref,
        ignore_data=False,
        read_policy="default",
        null_policy="strict",
        ignore_header_errors=False,
        mnemonic_case="upper",
        index_unit=None,
        **kwargs
    ):
        """Read a LAS file.

        Arguments:
            file_ref (file-like object, str): either a filename, an open file
                object, or a string containing the contents of a file.

        Keyword Arguments:
            null_policy (str or list): see
                http://lasio.readthedocs.io/en/latest/data-section.html#handling-invalid-data-indicators-automatically
            ignore_data (bool): if True, do not read in any of the actual data,
                just the header metadata. False by default.
            ignore_header_errors (bool): ignore LASHeaderErrors (False by
                default)
            mnemonic_case (str): 'preserve': keep the case of HeaderItem mnemonics
                                 'upper': convert all HeaderItem mnemonics to uppercase
                                 'lower': convert all HeaderItem mnemonics to lowercase
            index_unit (str): Optionally force-set the index curve's unit to "m" or "ft"

        See :func:`lasio.reader.open_with_codecs` for additional keyword
        arguments which help to manage issues relate to character encodings.

        """

        file_obj, self.encoding = reader.open_file(file_ref, **kwargs)

        regexp_subs, value_null_subs, version_NULL = reader.get_substitutions(
            read_policy, null_policy
        )

        try:
            self.raw_sections = reader.read_file_contents(
                file_obj, regexp_subs, value_null_subs, ignore_data=ignore_data
            )
        finally:
            if hasattr(file_obj, "close"):
                file_obj.close()

        if len(self.raw_sections) == 0:
            raise KeyError("No ~ sections found. Is this a LAS file?")

        def add_section(pattern, name, **sect_kws):
            raw_section = self.match_raw_section(pattern)
            drop = []
            if raw_section:
                self.sections[name] = reader.parse_header_section(
                    raw_section, **sect_kws
                )
                drop.append(raw_section["title"])
            else:
                logger.warning(
                    "Header section %s regexp=%s was not found." % (name, pattern)
                )
            for key in drop:
                self.raw_sections.pop(key)

        add_section(
            "~V",
            "Version",
            version=1.2,
            ignore_header_errors=ignore_header_errors,
            mnemonic_case=mnemonic_case,
        )

        # Establish version and wrap values if possible.

        try:
            version = self.version["VERS"].value
        except KeyError:
            logger.warning("VERS item not found in the ~V section.")
            version = None

        try:
            wrap = self.version["WRAP"].value
        except KeyError:
            logger.warning("WRAP item not found in the ~V section")
            wrap = None

        # Validate version.
        #
        # If VERS was missing and version = None, then the file will be read in
        # as if version were 2.0. But there will be no VERS HeaderItem, meaning
        # that las.write(..., version=None) will fail with a KeyError. But
        # las.write(..., version=1.2) will work because a new VERS HeaderItem
        # will be created.

        try:
            assert version in (1.2, 2, None)
        except AssertionError:
            if version < 2:
                version = 1.2
            else:
                version = 2
        else:
            if version is None:
                logger.info("Assuming that LAS VERS is 2.0")
                version = 2

        add_section(
            "~W",
            "Well",
            version=version,
            ignore_header_errors=ignore_header_errors,
            mnemonic_case=mnemonic_case,
        )

        # Establish NULL value if possible.

        try:
            null = self.well["NULL"].value
        except KeyError:
            logger.warning("NULL item not found in the ~W section")
            null = None

        add_section(
            "~C",
            "Curves",
            version=version,
            ignore_header_errors=ignore_header_errors,
            mnemonic_case=mnemonic_case,
        )
        add_section(
            "~P",
            "Parameter",
            version=version,
            ignore_header_errors=ignore_header_errors,
            mnemonic_case=mnemonic_case,
        )
        s = self.match_raw_section("~O")

        drop = []
        if s:
            self.sections["Other"] = "\n".join(s["lines"])
            drop.append(s["title"])
        for key in drop:
            self.raw_sections.pop(key)

        # Deal with nonstandard sections that some operators and/or
        # service companies (eg IHS) insist on adding.
        drop = []
        for s in self.raw_sections.values():
            if s["section_type"] == "header":
                logger.warning("Found nonstandard LAS section: " + s["title"])
                self.sections[s["title"][1:]] = "\n".join(s["lines"])
                drop.append(s["title"])
        for key in drop:
            self.raw_sections.pop(key)

        if not ignore_data:
            drop = []
            s = self.match_raw_section("~A")
            s_valid = True
            if s is None:
                logger.warning("No data section (regexp='~A') found")
                s_valid = False
            try:
                if s["ncols"] is None:
                    logger.warning("No numerical data found inside ~A section")
                    s_valid = False
            except:
                pass

            if s_valid:
                arr = s["array"]
                logger.debug("~A data.shape {}".format(arr.shape))
                if version_NULL:
                    arr[arr == null] = np.nan
                logger.debug(
                    "~A after NULL replacement data.shape {}".format(arr.shape)
                )

                n_curves = len(self.curves)
                n_arr_cols = len(self.curves)  # provisional pending below check
                logger.debug("n_curves=%d ncols=%d" % (n_curves, s["ncols"]))
                if wrap == "NO":
                    if s["ncols"] > n_curves:
                        n_arr_cols = s["ncols"]
                try:
                    data = np.reshape(arr, (-1, n_arr_cols))
                except ValueError as e:
                    err_msg = (
                        "cannot reshape ~A array of "
                        "size {arr_shape} into "
                        "{n_arr_cols} columns".format(
                            arr_shape=arr.shape, n_arr_cols=n_arr_cols
                        )
                    )
                    if sys.version_info.major < 3:
                        e.message = err_msg
                        raise e
                    else:
                        raise ValueError(err_msg).with_traceback(e.__traceback__)
                self.set_data(data, truncate=False)
                drop.append(s["title"])
            for key in drop:
                self.raw_sections.pop(key)

        if "m" in str(index_unit):
            index_unit = "m"

        if index_unit:
            self.index_unit = index_unit
        else:
            check_units_on = []
            for mnemonic in ("STRT", "STOP", "STEP"):
                if mnemonic in self.well:
                    check_units_on.append(self.well[mnemonic])
            if len(self.curves) > 0:
                check_units_on.append(self.curves[0])
            for index_unit, possibilities in defaults.DEPTH_UNITS.items():
                if all(i.unit.upper() in possibilities for i in check_units_on):
                    self.index_unit = index_unit

    def write(self, file_ref, **kwargs):
        """Write LAS file to disk.

        Arguments:
            file_ref (open file-like object or str): a file-like object opening
                for writing, or a filename.

        All ``**kwargs`` are passed to :func:`lasio.writer.write` -- please
        check the docstring of that function for more keyword arguments you can
        use here!

        Examples:

            >>> import lasio
            >>> las = lasio.read("tests/examples/sample.las")
            >>> with open('test_output.las', mode='w') as f:
            ...     las.write(f, version=2.0)   # <-- this method

        """
        opened_file = False
        if isinstance(file_ref, basestring) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")
        writer.write(self, file_ref, **kwargs)
        if opened_file:
            file_ref.close()

    def to_excel(self, filename):
        """Export LAS file to a Microsoft Excel workbook.

        This function will raise an :exc:`ImportError` if ``openpyxl`` is not
        installed.

        Arguments:
            filename (str)

        """
        from . import excel

        converter = excel.ExcelConverter(self)
        converter.write(filename)

    def to_csv(self, file_ref, mnemonics=True, units=True, units_loc="line", **kwargs):
        """Export to a CSV file.

        Arguments:
            file_ref (open file-like object or str): a file-like object opening
                for writing, or a filename.

        Keyword Arguments:
            mnemonics (list, True, False): write mnemonics as a header line at the
                start. If list, use the supplied items as mnemonics. If True,
                use the curve mnemonics.
            units (list, True, False): as for mnemonics.
            units_loc (str or None): either 'line', '[]' or '()'. 'line' will put
                units on the line following the mnemonics (good for WellCAD).
                '[]' and '()' will put the units in either brackets or
                parentheses following the mnemonics, on the single header line
                (better for Excel)
            **kwargs: passed to :class:`csv.writer`. Note that if
                ``lineterminator`` is **not** specified here, then it will be
                sent to :class:`csv.writer` as ``lineterminator='\\n'``.

        """
        opened_file = False
        if isinstance(file_ref, basestring) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")

        if not "lineterminator" in kwargs:
            kwargs["lineterminator"] = "\n"
        writer = csv.writer(file_ref, **kwargs)

        if mnemonics is True:
            mnemonics = [c.original_mnemonic for c in self.curves]
        if units is True:
            units = [c.unit for c in self.curves]

        if mnemonics:
            if units_loc in ("()", "[]") and units:
                mnemonics = [
                    m + " " + units_loc[0] + u + units_loc[1]
                    for m, u in zip(mnemonics, units)
                ]
            writer.writerow(mnemonics)
        if units:
            if units_loc == "line":
                writer.writerow(units)

        for i in range(self.data.shape[0]):
            writer.writerow(self.data[i, :])

        if opened_file:
            file_ref.close()

    def match_raw_section(self, pattern, re_func="match", flags=re.IGNORECASE):
        """Find raw section with a regular expression.

        Arguments:
            pattern (str): regular expression (you need to include the tilde)

        Keyword Arguments:
            re_func (str): either "match" or "search", see python ``re`` module.
            flags (int): flags for :func:`re.compile`

        Returns:
            dict

        Intended for internal use only.

        """
        for title in self.raw_sections.keys():
            title = title.strip()
            p = re.compile(pattern, flags=flags)
            if re_func == "match":
                re_func = re.match
            elif re_func == "search":
                re_func = re.search
            m = re_func(p, title)
            if m:
                return self.raw_sections[title]

    def get_curve(self, mnemonic):
        """Return CurveItem object.

        Arguments:
            mnemonic (str): the name of the curve

        Returns:
            :class:`lasio.las_items.CurveItem` (not just the data array)

        """
        for curve in self.curves:
            if curve.mnemonic == mnemonic:
                return curve

    def __getitem__(self, key):
        """Provide access to curve data.

        Arguments:
            key (str, int): either a curve mnemonic or the column index.

        Returns:
            1D :class:`numpy.ndarray` (the data for the curve)

        """
        # TODO: If I implement 2D arrays, need to check here for :1 :2 :3 etc.
        curve_mnemonics = [c.mnemonic for c in self.curves]
        if isinstance(key, int):
            return self.curves[key].data
        elif key in curve_mnemonics:
            return self.curves[key].data
        else:
            raise KeyError("{} not found in curves ({})".format(key, curve_mnemonics))

    def __setitem__(self, key, value):
        """Append a curve.

        Arguments:
            key (str): the curve mnemonic
            value (1D data or CurveItem): either the curve data, or a CurveItem

        See :meth:`lasio.las.LASFile.append_curve_item` or
        :meth:`lasio.las.LASFile.append_curve` for more details.

        """
        if isinstance(value, CurveItem):
            if key != value.mnemonic:
                raise KeyError(
                    "key {} does not match value.mnemonic {}".format(
                        key, value.mnemonic
                    )
                )
            self.append_curve_item(value)
        else:
            # Assume value is an ndarray
            self.append_curve(key, value)

    def keys(self):
        """Return curve mnemonics."""
        return [c.mnemonic for c in self.curves]

    def values(self):
        """Return data for each curve."""
        return [c.data for c in self.curves]

    def items(self):
        """Return mnemonics and data for all curves."""
        return [(c.mnemonic, c.data) for c in self.curves]

    def iterkeys(self):
        return iter(list(self.keys()))

    def itervalues(self):
        return iter(list(self.values()))

    def iteritems(self):
        return iter(list(self.items()))

    @property
    def version(self):
        """Header information from the Version (~V) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        """
        return self.sections["Version"]

    @version.setter
    def version(self, section):
        self.sections["Version"] = section

    @property
    def well(self):
        """Header information from the Well (~W) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        """
        return self.sections["Well"]

    @well.setter
    def well(self, section):
        self.sections["Well"] = section

    @property
    def curves(self):
        """Curve information and data from the Curves (~C) and data section..

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        """
        return self.sections["Curves"]

    @curves.setter
    def curves(self, section):
        self.sections["Curves"] = section

    @property
    def curvesdict(self):
        """Curve information and data from the Curves (~C) and data section..

        Returns:
            dict

        """
        d = {}
        for curve in self.curves:
            d[curve["mnemonic"]] = curve
        return d

    @property
    def params(self):
        """Header information from the Parameter (~P) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        """
        return self.sections["Parameter"]

    @params.setter
    def params(self, section):
        self.sections["Parameter"] = section

    @property
    def other(self):
        """Header information from the Other (~O) section.

        Returns:
            str

        """
        return self.sections["Other"]

    @other.setter
    def other(self, section):
        self.sections["Other"] = section

    @property
    def metadata(self):
        """All header information joined together.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        """
        s = SectionItems()
        for section in self.sections:
            for item in section:
                s.append(item)
        return s

    @metadata.setter
    def metadata(self, value):
        raise NotImplementedError("Set values in the section directly")

    @property
    def header(self):
        """All header information

        Returns:
            dict

        """
        return self.sections

    def df(self):
        """Return data as a :class:`pandas.DataFrame` structure.

        The first Curve of the LASFile object is used as the pandas
        DataFrame's index.

        """
        import pandas as pd
        from pandas.api.types import is_object_dtype

        df = pd.DataFrame(self.data, columns=[c.mnemonic for c in self.curves])
        for column in df.columns:
            if is_object_dtype(df[column].dtype):
                try:
                    df[column] = df[column].astype(np.float64)
                except ValueError:
                    pass
        if len(self.curves) > 0:
            df = df.set_index(self.curves[0].mnemonic)
        return df

    @property
    def data(self):
        return np.vstack([c.data for c in self.curves]).T

    @data.setter
    def data(self, value):
        return self.set_data(value)

    def set_data(self, array_like, names=None, truncate=False):
        """Set the data for the LAS; actually sets data on individual curves.

        Arguments:
            array_like (array_like or :class:`pandas.DataFrame`): 2-D data array

        Keyword Arguments:
            names (list, optional): used to replace the names of the existing
                :class:`lasio.las_items.CurveItem` objects.
            truncate (bool): remove any columns which are not included in the
                Curves (~C) section.

        Note: you can pass a :class:`pandas.DataFrame` to this method.

        """
        try:
            import pandas as pd
        except ImportError:
            pass
        else:
            if isinstance(array_like, pd.DataFrame):
                return self.set_data_from_df(
                    array_like, **dict(names=names, truncate=False)
                )
        data = np.asarray(array_like)

        # Truncate data array if necessary.
        if truncate:
            data = data[:, len(self.curves)]

        # Extend curves list if necessary.
        while data.shape[1] > len(self.curves):
            self.curves.append(CurveItem(""))

        if not names:
            names = [c.original_mnemonic for c in self.curves]
        else:
            # Extend names list if necessary.
            while len(self.curves) > len(names):
                names.append("")
        logger.debug("set_data. names to use: {}".format(names))

        for i, curve in enumerate(self.curves):
            curve.mnemonic = names[i]
            curve.data = data[:, i]

        self.curves.assign_duplicate_suffixes()

    def set_data_from_df(self, df, **kwargs):
        """Set the LAS file data from a :class:`pandas.DataFrame`.

        Arguments:
            df (pandas.DataFrame): curve mnemonics are the column names.
                The depth column for the curves must be the index of the
                DataFrame.

        Keyword arguments are passed to :meth:`lasio.las.LASFile.set_data`.

        """
        df_values = np.vstack([df.index.values, df.values.T]).T
        if (not "names" in kwargs) or (not kwargs["names"]):
            kwargs["names"] = [df.index.name] + [
                str(name) for name in df.columns.values
            ]
        self.set_data(df_values, **kwargs)

    @property
    def index(self):
        """Return data from the first column of the LAS file data (depth/time).

        """
        return self.curves[0].data

    @property
    def depth_m(self):
        """Return the index as metres."""
        if self._index_unit_contains("M"):
            return self.index
        elif self._index_unit_contains("F"):
            return self.index * 0.3048
        else:
            raise exceptions.LASUnknownUnitError("Unit of depth index not known")

    @property
    def depth_ft(self):
        """Return the index as feet."""
        if self._index_unit_contains("M"):
            return self.index / 0.3048
        elif self._index_unit_contains("F"):
            return self.index
        else:
            raise exceptions.LASUnknownUnitError("Unit of depth index not known")

    def _index_unit_contains(self, unit_code):
        """Check value of index_unit string, ignoring case

        Args:
            index unit code (string) e.g. 'M' or 'FT'
        """
        return self.index_unit and (unit_code.upper() in self.index_unit.upper())

    def add_curve_raw(self, mnemonic, data, unit="", descr="", value=""):
        """Deprecated. Use append_curve_item() or insert_curve_item() instead."""
        return self.append_curve_item(self, mnemonic, data, unit, descr, value)

    def append_curve_item(self, curve_item):
        """Add a CurveItem.

        Args:
            curve_item (lasio.CurveItem)

        """
        self.insert_curve_item(len(self.curves), curve_item)

    def insert_curve_item(self, ix, curve_item):
        """Insert a CurveItem.

        Args:
            ix (int): position to insert CurveItem i.e. 0 for start
            curve_item (lasio.CurveItem)

        """
        assert isinstance(curve_item, CurveItem)
        self.curves.insert(ix, curve_item)

    def add_curve(self, *args, **kwargs):
        """Deprecated. Use append_curve() or insert_curve() instead."""
        return self.append_curve(*args, **kwargs)

    def append_curve(self, mnemonic, data, unit="", descr="", value=""):
        """Add a curve.

        Arguments:
            mnemonic (str): the curve mnemonic
            data (1D ndarray): the curve data

        Keyword Arguments:
            unit (str): curve unit
            descr (str): curve description
            value (int/float/str): value e.g. API code.

        """
        return self.insert_curve(len(self.curves), mnemonic, data, unit, descr, value)

    def insert_curve(self, ix, mnemonic, data, unit="", descr="", value=""):
        """Insert a curve.

        Arguments:
            ix (int): position to insert curve at i.e. 0 for start.
            mnemonic (str): the curve mnemonic
            data (1D ndarray): the curve data

        Keyword Arguments:
            unit (str): curve unit
            descr (str): curve description
            value (int/float/str): value e.g. API code.

        """
        curve = CurveItem(mnemonic, unit, value, descr, data)
        self.insert_curve_item(ix, curve)

    def delete_curve(self, mnemonic=None, ix=None):
        """Delete a curve.

        Keyword Arguments:
            ix (int): index of curve in LASFile.curves.
            mnemonic (str): mnemonic of curve.

        The index takes precedence over the mnemonic.

        """
        if ix is None:
            ix = self.curves.keys().index(mnemonic)
        self.curves.pop(ix)

    @property
    def json(self):
        """Return object contents as a JSON string."""
        obj = OrderedDict()
        for name, section in self.sections.items():
            try:
                obj[name] = section.json
            except AttributeError:
                obj[name] = json.dumps(section)
        return json.dumps(obj)

    @json.setter
    def json(self, value):
        raise Exception("Cannot set objects from JSON")


class Las(LASFile):

    """LAS file object.

    Retained for backwards compatibility.

    """

    pass


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LASFile):
            d = {"metadata": {}, "data": {}}
            for name, section in obj.sections.items():
                if isinstance(section, basestring):
                    d["metadata"][name] = section
                else:
                    d["metadata"][name] = []
                    for item in section:
                        d["metadata"][name].append(dict(item))
            for curve in obj.curves:
                d["data"][curve.mnemonic] = list(curve.data)
            return d
