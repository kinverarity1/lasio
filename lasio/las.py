from __future__ import print_function

# Standard library packages
import codecs
import json
import logging
import os
import re
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
from .las_items import (
    HeaderItem, CurveItem, SectionItems, OrderedDict)
from . import defaults
from . import reader
from . import writer

logger = logging.getLogger(__name__)


class LASFile(object):

    '''LAS file object.

    Keyword Arguments:
        file_ref (file-like object, str): either a filename, an open file 
            object, or a string containing the contents of a file.

    See :meth:`lasio.las.LASFile.read` and :func:`lasio.reader.open_file` for
    additional keyword arguments you can use here.

    '''

    def __init__(self, file_ref=None, **kwargs):

        self._text = ''
        self.index_unit = None
        default_items = defaults.get_default_items()
        self.sections = {
            'Version': default_items['Version'],
            'Well': default_items['Well'],
            'Curves': default_items['Curves'],
            'Parameter': default_items['Parameter'],
            'Other': str(default_items['Other']),
        }

        if not (file_ref is None):
            self.read(file_ref, **kwargs)

    def read(self, file_ref, null_subs=True, ignore_data=False, 
             ignore_header_errors=False, **kwargs):
        '''Read a LAS file.

        Arguments:
            file_ref (file-like object, str): either a filename, an open file 
                object, or a string containing the contents of a file.

        Keyword Arguments:
            null_subs (bool): if True, replace invalid values with np.nan
            ignore_data (bool): if True, do not read in any of the actual data, 
                just the header metadata. False by default.
            ignore_header_errors (bool): ignore LASHeaderErrors (False by 
                default)

        See :func:`lasio.reader.open_file` for additional keyword arguments you
        can use here.

        '''

        file_obj = reader.open_file(file_ref, **kwargs)
        self.raw_sections = reader.read_file_contents(
            file_obj, ignore_data=ignore_data)
        if hasattr(file_obj, "close"):
            file_obj.close()

        def add_section(pattern, name, **sect_kws):
            raw_section = self.match_raw_section(pattern)
            drop = []
            if raw_section:
                self.sections[name] = reader.parse_header_section(raw_section, 
                                                                  **sect_kws)
                drop.append(raw_section["title"])
            else:
                logger.warning("Header section %s regexp=%s was not found."
                               % (name, pattern))
            for key in drop:
                self.raw_sections.pop(key)

        add_section("~V", "Version", version=1.2, 
                    ignore_header_errors=ignore_header_errors)

        # Set version
        try:
            version = self.version['VERS'].value
        except KeyError:
            logger.warning('VERS item not found in the ~V section')

        # Validate version
        try:
            assert version in (1.2, 2)
        except AssertionError:
            logger.warning('LAS version is %s -- neither 1.2 nor 2' % version)
            if version < 2:
                version = 1.2
            else:
                version = 2

        add_section("~W", "Well", version=version, 
                    ignore_header_errors=ignore_header_errors)
        add_section("~C", "Curves", version=version, 
                    ignore_header_errors=ignore_header_errors)
        add_section("~P", "Parameter", version=version, 
                    ignore_header_errors=ignore_header_errors)
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
                logger.warning('Found nonstandard LAS section: ' + s["title"])
                self.sections[s["title"][1:]] = "\n".join(s["lines"])
                drop.append(s["title"])
        for key in drop:
            self.raw_sections.pop(key)

        if not ignore_data:
            null = self.well['NULL'].value

            drop = []
            s = self.match_raw_section("~A")
            if s:
                arr = s["array"]
                if null_subs:
                    arr[arr == null] = np.nan

                n_curves = len(self.curves)
                n_arr_cols = len(self.curves) # provisional pending below check
                logger.debug("n_curves=%d ncols=%d" % (n_curves, s["ncols"]))
                if self.version["WRAP"].value == "NO":
                    if s["ncols"] > n_curves:
                        n_arr_cols = s["ncols"]
                data = np.reshape(arr, (-1, n_arr_cols))

                self.set_data(data, truncate=False)
                drop.append(s["title"])
            else:
                logger.warning("No data section (regexp='~A') found")
            for key in drop:
                self.raw_sections.pop(key)

        if (self.well['STRT'].unit.upper() in defaults.METRE_UNITS and
                self.well['STOP'].unit.upper() in defaults.METRE_UNITS and
                self.well['STEP'].unit.upper() in defaults.METRE_UNITS and
                self.curves[0].unit.upper() in defaults.METRE_UNITS):
            self.index_unit = 'M'
        elif (self.well['STRT'].unit.upper() in defaults.FEET_UNITS and
              self.well['STOP'].unit.upper() in defaults.FEET_UNITS and
              self.well['STEP'].unit.upper() in defaults.FEET_UNITS and
              self.curves[0].unit.upper() in defaults.FEET_UNITS):
            self.index_unit = 'FT'

    def write(self, file_ref, **kwargs):
        '''Write LAS file to disk.

        Arguments:
            file_ref (open file-like object or str): a file-like object opening
                for writing, or a filename.
    
        All ``**kwargs`` are passed to :func:`lasio.writer.write` -- please
        check the docstring of that function for more keyword arguments you can
        use here!

        Examples:

            >>> with open('test_output.las', mode='w') as f:
            ...     lasfile_obj.write(f, version=2.0)   # <-- this method

        '''
        opened_file = False
        if isinstance(file_ref, basestring) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")
        writer.write(self, file_ref, **kwargs)
        if opened_file:
            file_ref.close()

    def to_excel(self, filename):
        '''Export LAS file to a Microsoft Excel workbook.

        This function will raise an :exc:`ImportError` if ``openpyxl`` is not
        installed.

        Arguments:
            filename (str)

        '''
        from . import excel
        converter = excel.ExcelConverter(self)
        converter.write(filename)

    def match_raw_section(self, pattern, re_func="match", flags=re.IGNORECASE):
        '''Find raw section with a regular expression.

        Arguments:
            pattern (str): regular expression (you need to include the tilde)

        Keyword Arguments:
            re_func (str): either "match" or "search", see python ``re`` module.
            flags (int): flags for :func:`re.compile`

        Returns:
            dict

        Intended for internal use only.

        '''
        for title in self.raw_sections.keys():
            title = title.strip()
            p = re.compile(pattern, flags=flags)
            if re_func == "match":
                re_func = re.match
            elif re_func == "search":
                re_func == re.search
            m = re_func(p, title)
            if m:
                return self.raw_sections[title]

    def get_curve(self, mnemonic):
        '''Return CurveItem object.

        Arguments:
            mnemonic (str): the name of the curve

        Returns:
            :class:`lasio.las_items.CurveItem` (not just the data array)

        '''
        for curve in self.curves:
            if curve.mnemonic == mnemonic:
                return curve

    def __getitem__(self, key):
        '''Provide access to curve data.

        Arguments:
            key (str, int): either a curve mnemonic or the column index.

        Returns:
            1D :class:`numpy.ndarray` (the data for the curve)

        '''
        if isinstance(key, int):
            return self.curves[key].data
        elif isinstance(key, str):
            if key in self.keys():
                return self.curves[key].data
        else:
            super(LASFile, self).__getitem__(key)

    def __setitem__(self, key, value):
        '''Not implemented.

        It is not possible yet to set curve data via the LASFile's item
        access shortcut.

        '''
        assert NotImplementedError('not yet')

    def keys(self):
        '''Return curve mnemonics.'''
        return [c.mnemonic for c in self.curves]

    def values(self):
        '''Return data for each curve.'''
        return [c.data for c in self.curves]

    def items(self):
        '''Return mnemonics and data for all curves.'''
        return [(c.mnemonic, c.data) for c in self.curves]

    def iterkeys(self):
        return iter(list(self.keys()))

    def itervalues(self):
        return iter(list(self.values()))

    def iteritems(self):
        return iter(list(self.items()))

    @property
    def version(self):
        '''Header information from the Version (~V) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        '''
        return self.sections['Version']

    @version.setter
    def version(self, section):
        self.sections['Version'] = section

    @property
    def well(self):
        '''Header information from the Well (~W) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        '''
        return self.sections['Well']

    @well.setter
    def well(self, section):
        self.sections['Well'] = section

    @property
    def curves(self):
        '''Curve information and data from the Curves (~C) and data section..

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        '''
        return self.sections['Curves']

    @curves.setter
    def curves(self, section):
        self.sections['Curves'] = section

    @property
    def curvesdict(self):
        '''Curve information and data from the Curves (~C) and data section..

        Returns:
            dict

        '''
        d = {}
        for curve in self.curves:
            d[curve['mnemonic']] = curve
        return d

    @property
    def params(self):
        '''Header information from the Parameter (~P) section.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        '''
        return self.sections['Parameter']

    @params.setter
    def params(self, section):
        self.sections['Parameter'] = section

    @property
    def other(self):
        '''Header information from the Other (~O) section.

        Returns:
            str

        '''
        return self.sections['Other']

    @other.setter
    def other(self, section):
        self.sections['Other'] = section

    @property
    def metadata(self):
        '''All header information joined together.

        Returns:
            :class:`lasio.las_items.SectionItems` object.

        '''
        s = SectionItems()
        for section in self.sections:
            for item in section:
                s.append(item)
        return s

    @metadata.setter
    def metadata(self, value):
        raise NotImplementedError('Set values in the section directly')

    @property
    def header(self):
        '''All header information

        Returns:
            dict

        '''
        return self.sections

    def df(self):
        '''Return data as a :class:`pandas.DataFrame` structure.'''
        import pandas as pd
        df = pd.DataFrame(self.data, columns=[c.mnemonic for c in self.curves])
        if len(self.curves) > 0:
            df = df.set_index(self.curves[0].mnemonic)
        return df

    def set_data(self, array_like, names=None, truncate=False):
        '''Set the LAS file data array.

        Arguments:
            array_like (array_like): 2-D data array

        Keyword Arguments:
            names (list, optional): used to replace the names of the existing
                :class:`lasio.las_items.CurveItem` objects.
            truncate (bool): remove any columns which are not included in the
                Curves (~C) section.

        '''
        data = np.asarray(array_like)
        if truncate:
            data = data[:, len(self.curves)]
        else:
            for i in range(data.shape[1]):
                if i < len(self.curves):
                    curve = self.curves[i]
                    if names:
                        curve.name = names[i]
                else:
                    if names:
                        name = names[i]
                    else:
                        name = ''
                    curve = CurveItem(name)
                    self.curves.insert(i, curve)
                curve.data = data[:, i]
        self.data = data

    def set_data_from_df(self, df, **kwargs):
        '''Set the LAS file data from a :class:`pandas.DataFrame`.

        Arguments:
            df (pandas.DataFrame): curve mnemonics are the column names.

        Keyword arguments are passed to :meth:`lasio.las.LASFile.set_data`.

        '''
        df_values = np.vstack([df.index.values, df.values.T]).T
        names = [df.index.name] + [str(name) for name in df.columns.values]
        self.set_data(df_values, names=names, **kwargs)

    @property
    def index(self):
        '''Return data from the first column of the LAS file data (depth/time).

        '''
        return self.curves[0].data

    @property
    def depth_m(self):
        '''Return the index as metres.'''
        if self.index_unit == 'M':
            return self.index
        elif self.index_unit == 'FT':
            return self.index * 0.3048
        else:
            raise exceptions.LASUnknownUnitError(
                'Unit of depth index not known')

    @property
    def depth_ft(self):
        '''Return the index as feet.'''
        if self.index_unit == 'M':
            return self.index / 0.3048
        elif self.index_unit == 'FT':
            return self.index
        else:
            raise exceptions.LASUnknownUnitError(
                'Unit of depth index not known')

    def add_curve(self, *args, **kwargs):
        '''Add curve(s) to the LAS file.

        If the first argument is a :class:`lasio.las_items.CurveItem` object,
        then this method will assume all the arguments are CurveItem objects
        and add them all.

        Otherwise, the arguments will all be passed to
        :meth:`lasio.las.LASFile.add_curve_raw` and a single curve will be
        created and added.

        '''
        if isinstance(args[0], CurveItem):
            for curve in args:
                self.curves.append(curve)
        else:
            self.add_curve_raw(*args, **kwargs)

    def add_curve_raw(self, mnemonic, data, unit='', descr='', value=''):
        '''Add data to the LAS file as a curve.

        Arguments:
            mnemonic (str): the curve's mnemonic
            data (array-like, 1-D): the curve's data.

        Keyword Arguments:
            unit (str, optional): the unit for the curve
            descr (str, optional): short description (keep it to a single line!)
            value (float, str, int): value (e.g. API code??)

        '''
        curve = CurveItem(mnemonic, unit, value, descr)
        if hasattr(self, 'data'):
            self.data = np.column_stack([self.data, data])
        else:
            self.data = np.column_stack([data])
        curve.data = self.data[:, -1]
        self.curves.append(curve)

    def delete_curve(self, mnemonic):
        '''Remove curve by its mnemonic.

        Arguments:
            mnemonic (str): curve mnemonic (must exist in the file)

        '''
        ix = self.curves.keys().index(mnemonic)
        self.curves.pop(ix)
        self.data = np.delete(self.data, np.s_[ix], axis=1)

    @property
    def json(self):
        '''Return object contents as a JSON string.'''
        obj = OrderedDict()
        for name, section in self.sections.items():
            try:
                obj[name] = section.json
            except AttributeError:
                obj[name] = json.dumps(section)
        return json.dumps(obj)

    @json.setter
    def json(self, value):
        raise Exception('Cannot set objects from JSON')



class Las(LASFile):

    '''LAS file object.

    Retained for backwards compatibility.

    '''
    pass


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, LASFile):
            d = {'metadata': {},
                 'data': {}}
            for name, section in obj.sections.items():
                if isinstance(section, basestring):
                    d['metadata'][name] = section
                else:
                    d['metadata'][name] = []
                    for item in section:
                        d['metadata'][name].append(dict(item))
            for curve in obj.curves:
                d['data'][curve.mnemonic] = list(curve.data)
            return d
