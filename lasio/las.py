from __future__ import print_function

try:  # will work in Python 3
    from collections.abc import Sequence
except ImportError:  # Support Python 2.7
    from collections import Sequence

import csv
import json
import logging
import re
import sys
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
    * :meth:`lasio.LASFile.read` - control how NULL values and errors are
      handled during parsing

    Attributes:
        encoding (str or None): the character encoding used when reading the
            file in from disk

    """

    def __init__(self, file_ref=None, **read_kwargs):
        super(LASFile, self).__init__()
        self._text = ""
        self.index_unit = None
        self.index_initial = None
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
        ignore_header_errors=False,
        ignore_comments=("#",),
        ignore_data_comments="#",
        mnemonic_case="upper",
        ignore_data=False,
        engine="numpy",
        use_normal_engine_for_wrapped=True,
        read_policy="default",
        null_policy="strict",
        index_unit=None,
        dtypes="auto",
        **kwargs
    ):
        """Read a LAS file.

        Arguments:
            file_ref (file-like object, str): either a filename, an open file
                object, or a string containing the contents of a file.

        Keyword Arguments:
            ignore_header_errors (bool): ignore LASHeaderErrors (False by
                default)
            ignore_comments (sequence/str): ignore lines beginning with these
                characters e.g. ``("#", '"')`` in header sections.
            ignore_data_comments (str): ignore lines beginning with this
                character in data sections only.
            mnemonic_case (str): 'preserve': keep the case of HeaderItem mnemonics
                                 'upper': convert all HeaderItem mnemonics to uppercase
                                 'lower': convert all HeaderItem mnemonics to lowercase
            ignore_data (bool): if True, do not read in any of the actual data,
                just the header metadata. False by default.
            engine (str): "normal": parse data section with normal Python reader
                (quite slow); "numpy": parse data section with `numpy.genfromtxt` (fast).
                By default the engine is "numpy".
            use_normal_engine_for_wrapped (bool): if header metadata indicates that
                the file is wrapped, always use the 'normal' engine. Default is True.
                The only reason you should use False is if speed is a very high priority
                and you had files with metadata that incorrectly indicates they are
                wrapped.
            read_policy (): TODO
            null_policy (str or list): see
                http://lasio.readthedocs.io/en/latest/data-section.html#handling-invalid-data-indicators-automatically
            index_unit (str): Optionally force-set the index curve's unit to "m" or "ft"
            dtypes ("auto", dict or list): specify the data types for each curve in the
                ~ASCII data section. If "auto", each curve will be converted to floats if
                possible and remain as str if not. If a dict you can specify only the
                curve mnemonics you want to convert as a key. If a list, please specify
                data types for each curve in order. Note that the conversion currently
                only occurs via numpy.ndarray.astype() and therefore only a few simple
                casts will work e.g. `int`, `float`, `str`.
            encoding (str): character encoding to open file_ref with, using
                :func:`io.open` (this is handled by
                :func:`lasio.reader.open_with_codecs`)
            encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
                handle errors with encodings (see
                `this section
                <https://docs.python.org/3/library/codecs.html#codec-base-classes>`__
                of the standard library's :mod:`codecs` module for more information)
                (this is handled by :func:`lasio.reader.open_with_codecs`)
            autodetect_encoding (str or bool): default True to use
                `chardet <https://github.com/chardet/chardet>`__/`cchardet
                <https://github.com/PyYoshi/cChardet>`__ to detect encoding.
                Note if set to False several common encodings will be tried but
                chardet won't be used.
                (this is handled by :func:`lasio.reader.open_with_codecs`)
            autodetect_encoding_chars (int/None): number of chars to read from LAS
                file for auto-detection of encoding.
                (this is handled by :func:`lasio.reader.open_with_codecs`)

        """

        logger.debug("Reading {}...".format(str(file_ref)))

        # Determine which lines to ignore:
        if ignore_comments is None:
            ignore_comments = []
        if isinstance(ignore_comments, str):
            ignore_comments = [ignore_comments]

        logger.debug("Ignore header lines beginning with {}".format(ignore_comments))
        logger.debug("Ignore data lines beginning with {}".format(ignore_data_comments))

        # Attempt to read file
        file_obj = ""
        try:
            file_obj, self.encoding = reader.open_file(file_ref, **kwargs)

            test_lidar = file_obj.read(4)
            if test_lidar == "LASF":
                raise IOError("This is a LASer file (i.e. LiDAR data), not a Log ASCII Standard file")
            else:
                file_obj.seek(0)

            logger.debug(
                "Fetching substitutions for read_policy {} and null policy {}".format(
                    read_policy, null_policy
                )
            )
            provisional_version = 2.0
            provisional_wrapped = "YES"
            provisional_null = None
            provisional_delimiter = "SPACE"

            section_positions = reader.find_sections_in_file(file_obj)
            logger.debug("Found {} sections".format(len(section_positions)))
            if len(section_positions) == 0:
                raise KeyError("No ~ sections found. Is this a LAS file?")

            data_section_indices = []
            # This is a transitional data_section_indicies till the las30 data
            # reading can handle 1.2 and 2.0 data, then it will be merged back
            # into data_section_indices
            las3_data_section_indices = []

            las3_section_indicators = ["_DATA", "_PARAMETER", "_DEFINITION"]

            for i, (k, first_line, last_line, section_title) in enumerate(
                section_positions
            ):
                section_type = reader.determine_section_type(section_title)
                logger.debug(
                    "Parsing {typ} section at lines {first_line}-{last_line} ({k} bytes) {title}".format(
                        typ=section_type,
                        title=section_title,
                        first_line=first_line + 1,
                        last_line=last_line + 1,
                        k=k,
                    )
                )

                # Read traditional LAS header item section
                if section_type == "Header items":
                    file_obj.seek(k)
                    sct_items = reader.parse_header_items_section(
                        file_obj,
                        line_nos=(first_line, last_line),
                        version=provisional_version,
                        ignore_header_errors=ignore_header_errors,
                        mnemonic_case=mnemonic_case,
                        ignore_comments=ignore_comments,
                    )

                    # Update provisional statuses
                    if "VERS" in sct_items:
                        provisional_version = sct_items.VERS.value
                    if "WRAP" in sct_items:
                        provisional_wrapped = sct_items.WRAP.value
                    if "NULL" in sct_items:
                        provisional_null = sct_items.NULL.value
                    if "DLM" in sct_items:
                        provisional_delimiter = sct_items.DLM.value

                    # las3 sections can contain _Data, _Parameter or _Definition
                    las3_section = any(
                        [
                            section_str in section_title[1:].upper()
                            for section_str in las3_section_indicators
                        ]
                    )

                    # TODO: Revise so that Version, Well and Parameter(Log_Parameter)
                    # are handled the properly for LAS-1.2, LAS-2.0 LAS-3.0
                    # Set "Curves" for LAS-1.2, LAS-2.0, LAS-3.0
                    if (
                        section_title[1] == "C" and "_" not in section_title
                    ) or "~Log_Definition" in section_title:
                        self.sections["Curves"] = sct_items
                    elif (
                        section_title[1] == "P" and "_" not in section_title
                    ) or "~Log_Parameter" in section_title:
                        self.sections["Parameter"] = sct_items
                    # Set any other LAS3.0  sections
                    elif provisional_version == 3.0 and las3_section:
                        self.sections[section_title[1:]] = sct_items
                    # Set regular sections
                    elif section_title[1] == "V":
                        self.sections["Version"] = sct_items
                    elif section_title[1] == "W":
                        self.sections["Well"] = sct_items
                    else:
                        self.sections[section_title[1:]] = sct_items

                # Read free-text LAS header section
                elif section_type == "Header (other)":
                    file_obj.seek(k)
                    line_no = first_line
                    contents = []
                    for line in file_obj:
                        if line.startswith("~") and line_no == last_line:
                            break
                        if line.startswith("~"):
                            continue
                        line_no += 1
                        contents.append(line.strip("\n").strip())
                        if line_no == last_line:
                            break
                    sct_contents = "\n".join(contents)

                    if section_title[1] == "O":
                        self.sections["Other"] = sct_contents
                    else:
                        self.sections[section_title[1:]] = sct_contents

                elif section_type == "Data":
                    logger.debug("Storing reference and returning later...")
                    data_section_indices.append(i)

                # Initial stub for parsing las3 data. This is probably a
                # transitional section that will merge with 1.2/2.0 data
                # parsing once fully functional
                elif section_type == "Las3_Data":
                    logger.debug("Storing Las3_Data reference and returning later...")
                    las3_data_section_indices.append(i)

            line_splitter = reader.define_line_splitter(provisional_delimiter)

            if provisional_delimiter == "COMMA":
                read_policy = "comma-delimiter"
            regexp_subs, value_null_subs, version_NULL = reader.get_substitutions(
                read_policy, null_policy
            )

            if not ignore_data:

                # Override the default "numpy" parser with the 'normal' parser
                # for these conditions:
                # - file is wrapped
                # - null_policy is not "strict"
                # - dtypes is not "auto". Numpy can handle specified dtypes but
                #   the performance decays to the 'normal' performance level.

                # normal engine.
                if provisional_wrapped == "YES" or null_policy != "strict" or dtypes != "auto":
                    if engine != "normal":
                        logger.warning("Only engine='normal' can read wrapped files")
                        if use_normal_engine_for_wrapped:
                            engine = "normal"

                if (
                    len(data_section_indices) == 0
                    and len(las3_data_section_indices) > 0
                ):
                    data_section_indices = las3_data_section_indices
                # Check for the number of columns in each data section.
                for k, first_line, last_line, section_title in [
                    section_positions[i] for i in data_section_indices
                ]:
                    logger.debug("Reading data section {}".format(section_title))

                    file_obj.seek(k)
                    n_columns = reader.inspect_data_section(
                        file_obj,
                        (first_line, last_line),
                        regexp_subs,
                        ignore_data_comments=ignore_data_comments,
                    )

                    # How many curves should the reader attempt to find?
                    reader_n_columns = n_columns
                    if reader_n_columns == -1:
                        reader_n_columns = len(self.curves)

                    file_obj.seek(k)

                    # Convert dtypes passed as dict into list for all columns
                    # defaulting to float for any not specified.
                    if isinstance(dtypes, dict):
                        dtypes = [dtypes.get(c.mnemonic, float) for c in self.curves]

                    # Notes see 2d9e43c3 and e960998f for 'try' background

                    # Attempt to read the data section
                    if engine == "numpy":
                        try:
                            curves_data_gen = reader.read_data_section_iterative_numpy_engine(
                                file_obj, (first_line, last_line)
                            )
                        except KeyboardInterrupt:
                            raise
                        except:
                            try:
                                file_obj.seek(k)
                                curves_data_gen = (
                                    reader.read_data_section_iterative_normal_engine(
                                        file_obj,
                                        (first_line, last_line),
                                        regexp_subs,
                                        value_null_subs,
                                        ignore_data_comments=ignore_data_comments,
                                        n_columns=reader_n_columns,
                                        dtypes=dtypes,
                                        line_splitter=line_splitter,
                                    )
                                )
                            except KeyboardInterrupt:
                                raise
                            except:
                                raise exceptions.LASDataError(
                                    traceback.format_exc()[:-1]
                                    + " in data section beginning line {}".format(i + 1)
                                )

                    if engine == "normal":
                        try:
                            curves_data_gen = (
                                reader.read_data_section_iterative_normal_engine(
                                    file_obj,
                                    (first_line, last_line),
                                    regexp_subs,
                                    value_null_subs,
                                    ignore_data_comments=ignore_data_comments,
                                    n_columns=reader_n_columns,
                                    dtypes=dtypes,
                                    line_splitter=line_splitter,
                                )
                            )
                        except KeyboardInterrupt:
                            raise
                        except:
                            raise exceptions.LASDataError(
                                traceback.format_exc()[:-1]
                                + " in data section beginning line {}".format(i + 1)
                            )

                    # Assign data to curves.
                    data_assigned_to_curves = {curve_idx: False for curve_idx in range(len(self.curves))}
                    curve_idx = 0
                    curve_length = 0
                    for curve_arr in curves_data_gen:

                        # Do not replace nulls in the index curve.
                        if version_NULL and curve_arr.dtype == float and curve_idx != 0:
                            logger.debug(
                                "Replacing {} with nan in {}-th curve".format(
                                    provisional_null, curve_idx
                                )
                            )
                            curve_arr[curve_arr == provisional_null] = np.nan

                        logger.debug(
                            "Assigning data {} to curve #{}".format(
                                curve_arr, curve_idx
                            )
                        )
                        if curve_length == 0:
                            curve_length = len(curve_arr)
                        if curve_idx < len(self.curves):
                            self.curves[curve_idx].data = curve_arr
                        else:
                            logger.debug("Creating new curve")
                            curve = CurveItem(mnemonic="", data=curve_arr)
                            self.curves.append(curve)
                        data_assigned_to_curves[curve_idx] = True
                        curve_idx += 1

                    # Assign missing data indicators for curves which have no data in the
                    # data section.
                    for curve_idx, flag in data_assigned_to_curves.items():
                        if flag is False:
                            logger.warning(
                                "Curve #{:.0f} '{:s}' is defined in the ~C section "
                                "but there is no data in ~A"
                                .format(curve_idx, self.curves[curve_idx].mnemonic)
                            )
                            self.curves[curve_idx].data = np.empty(curve_length) * np.nan

        finally:
            if hasattr(file_obj, "close"):
                file_obj.close()

            # TODO: reimplement these warnings!!

            ###### logger.warning("No data section (regexp='~A') found")
            ###### logger.warning("No numerical data found inside ~A section")

        # Understand the depth/index unit.

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
            matches = []
            for index_unit, possibilities in defaults.DEPTH_UNITS.items():
                for check_unit in check_units_on:
                    if any([check_unit.unit == p for p in possibilities]) or any(
                        [check_unit.unit.upper() == p for p in possibilities]
                    ):
                        matches.append(index_unit)
            matches = set(matches)
            if len(matches) == 1:
                self.index_unit = tuple(matches)[0]
            elif len(matches) == 0:
                self.index_unit = None
            else:
                logger.warning("Conflicting index units found: {}".format(matches))
                self.index_unit = None

        if len(self.curves) > 0:
            self.index_initial = self.index.copy()

    def update_start_stop_step(self, STRT=None, STOP=None, STEP=None, fmt="%.5f"):
        """Configure or change STRT, STOP, and STEP values on the LASFile object.

        Keyword Arguments:
            STRT, STOP, STEP (str, int, float): value to set on the relevant
                header item in the ~Well section - can be any
                data type.
            fmt (str): Python format string for formatting the STRT/STOP/STEP
                value in the situation where any of those keyword arguments
                are None

        If STRT/STOP/STEP are not passed to this method, they will be automatically
        calculated from the index curve.

        """

        # If we are getting STRT and STOP from the data then format them to a
        # standard precision.
        # If they are passed in with values, don't format them because we
        # assume they are at the user's expected precision.

        # If the 'try' fails because self.index doesn't exist or is empty
        # then use the default or parameter values for STRT, STOP, and STEP.
        try:
            if STRT is None:
                STRT = fmt % self.index[0]
            if STOP is None:
                STOP = fmt % self.index[-1]
            if STEP is None:
                # prevents an error being thrown in the case of only a single sample being written
                if STOP != STRT:
                    raw_step = self.index[1] - self.index[0]
                    STEP = fmt % raw_step
        except IndexError:
            pass

        self.well["STRT"].value = STRT
        self.well["STOP"].value = STOP
        self.well["STEP"].value = STEP

    def update_units_from_index_curve(self):
        """Align STRT/STOP/STEP header item units with the index curve's units."""
        # Check units
        if self.curves and self.curves[0].unit:
            unit = self.curves[0].unit
        else:
            unit = self.well["STRT"].unit
        self.well["STRT"].unit = unit
        self.well["STOP"].unit = unit
        self.well["STEP"].unit = unit
        # Check that curves exists to avoid throwing an expection.
        # to write to an non-existant object.
        if self.curves:
            self.curves[0].unit = unit

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

        try:
            import openpyxl
        except ImportError:
            pass
        else:
            from .excel import ExcelConverter

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
            :class:`lasio.CurveItem` (not just the data array)

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

        See :meth:`lasio.LASFile.append_curve_item` or
        :meth:`lasio.LASFile.append_curve` for more details.

        """
        if isinstance(value, CurveItem):
            if key != value.mnemonic:
                raise KeyError(
                    "key {} does not match value.mnemonic {}".format(
                        key, value.mnemonic
                    )
                )
            if key in self.curves.keys():
                ix = self.curves.keys().index(key)
                self.replace_curve_item(ix, value)
            else:
                self.append_curve_item(value)
        else:
            # Assume value is an ndarray
            if key in self.curves.keys():
                self.update_curve(mnemonic=key, data=value)
            else:
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
            :class:`lasio.SectionItems` object.

        """
        return self.sections["Version"]

    @version.setter
    def version(self, section):
        self.sections["Version"] = section

    @property
    def well(self):
        """Header information from the Well (~W) section.

        Returns:
            :class:`lasio.SectionItems` object.

        """
        return self.sections["Well"]

    @well.setter
    def well(self, section):
        self.sections["Well"] = section

    @property
    def curves(self):
        """Curve information and data from the Curves (~C) and data section..

        Returns:
            :class:`lasio.SectionItems` object.

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
            :class:`lasio.SectionItems` object.

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
                :class:`lasio.CurveItem` objects.
            truncate (bool): remove any columns which are not included in the
                Curves (~C) section.

        Note: you can pass a :class:`pandas.DataFrame` to this method.
        If you do this, the index of the DataFrame will be used as the first
        curve in the LAS file (i.e. it will not be discarded).

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
        while data.size > 0 and (data.shape[1] > len(self.curves)):
            self.curves.append(CurveItem(""))

        if not names:
            names = [c.original_mnemonic for c in self.curves]
        else:
            # Extend names list if necessary.
            while len(self.curves) > len(names):
                names.append("")
        logger.debug("set_data. names to use: {}".format(names))

        if data.size > 0:
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

        Keyword arguments are passed to :meth:`lasio.LASFile.set_data`.

        """
        df_values = np.vstack([df.index.values, df.values.T]).T
        if (not "names" in kwargs) or (not kwargs["names"]):
            kwargs["names"] = [df.index.name] + [
                str(name) for name in df.columns.values
            ]
        self.set_data(df_values, **kwargs)

    def stack_curves(self, mnemonic, sort_curves=True):
        """Stack multi-channel curve data to a numpy 2D ndarray. Provide a
        stub name (prefix shared by all curves that will be stacked) or a
        list of curve mnemonic strings.

        Keyword Arguments:
            mnemonic (str or list): Supply the first several characters of
                the channel set to be stacked. Alternatively, supply a list
                of the curve names (mnemonics strings) to be stacked.
            sort_curves (bool): Natural sort curves based on mnemonic prior
                to stacking.

        Returns:
            2-D numpy array
        """
        if isinstance(mnemonic, np.ndarray):
            mnemonic = list(mnemonic)

        if (not mnemonic) or (not all([i for i in mnemonic])):
            raise ValueError("`mnemonic` must not contain empty element")

        keys = self.curves.keys()
        if isinstance(mnemonic, str):
            channels = [i for i in keys if i.startswith(mnemonic)] or [mnemonic]
        elif isinstance(mnemonic, Sequence):
            channels = list(mnemonic)
        else:
            raise TypeError("`mnemonic` argument must be string or sequence")
        print(channels)

        if not set(keys).issuperset(set(channels)):
            missing = ", ".join(set(channels).difference(set(keys)))
            raise KeyError("{} not found in LAS curves.".format(missing))

        if sort_curves:
            nat_sort = lambda x: [
                int(i) if i.isdigit() else i for i in re.split(r"(\d+)", x)
            ]
            channels.sort(key=nat_sort)

        indices = [keys.index(i) for i in channels]
        return self.data[:, indices]

    @property
    def index(self):
        """Return data from the first column of the LAS file data (depth/time)."""
        return self.curves[0].data

    @property
    def depth_m(self):
        """Return the index as metres."""
        if self._index_unit_contains("M"):
            return self.index
        elif self._index_unit_contains("F"):
            return self.index * 0.3048
        elif self._index_unit_contains(".1IN"):
            return (self.index / 120) * 0.3048
        else:
            raise exceptions.LASUnknownUnitError("Unit of depth index not known")

    @property
    def depth_ft(self):
        """Return the index as feet."""
        if self._index_unit_contains("M"):
            return self.index / 0.3048
        elif self._index_unit_contains("F"):
            return self.index
        elif self._index_unit_contains(".1IN"):
            return self.index / 120
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

    def replace_curve_item(self, ix, curve_item):
        """Replace a CurveItem.

        Args:
            ix (int): position to insert CurveItem i.e. 0 for start
            curve_item (lasio.CurveItem)

        """
        self.delete_curve(ix=ix)
        self.insert_curve_item(ix, curve_item)

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

    def update_curve(self, mnemonic=None, ix=None, data=False, unit=False, descr=False, value=False):
        """Update a curve.

        Keyword Arguments:
            ix (int): index of curve in LASFile.curves.
            mnemonic (str): mnemonic of curve.
            data (ndarray): new data array (False if no update desired)
            unit (str): new value for unit (False if no update desired)
            descr (str): new description (False if no update desired)
            value (str/int/float etc): new value (False if no update desired)

        The index takes precedence over the mnemonic.

        """
        if ix is None:
            ix = self.curves.keys().index(mnemonic)
        curve = self.curves[ix]
        if data is not False:
            curve.data = data
        if unit is not False:
            curve.unit = unit
        if descr is not False:
            curve.descr = descr
        if value is not False:
            curve.value = value

    @property
    def json(self):
        """Return object contents as a JSON string."""
        return self.to_json()

    def to_json_old(self):
        """
        deprecated: to_json_old version=0.25.1 since=20200507 remove=20210508
        replacement_options: to_json()
        """
        obj = OrderedDict()
        for name, section in self.sections.items():
            try:
                obj[name] = section.json
            except AttributeError:
                obj[name] = json.dumps(section)
        return json.dumps(obj)

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder)

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
                    try:
                        d["metadata"][name] = section.dictview()
                    except:
                        for item in section:
                            d["metadata"][name].append(dict(item))
            for curve in obj.curves:
                d["data"][curve.mnemonic] = [
                    None if np.isnan(x) else x for x in curve.data
                ]
            return d
