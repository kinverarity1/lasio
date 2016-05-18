'''las.py - read Log ASCII Standard files

See README.rst and LICENSE for more information.

'''
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
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

# Required third-party packages available on PyPi:

from namedlist import namedlist
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
        file_ref: either a filename, an open file object, or a string of
            a LAS file contents.
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    '''

    def __init__(self, file_ref=None, **kwargs):

        self._text = ''
        self.index_unit = None
        self.sections = {
            'Version': defaults.DEFAULT_ITEMS['Version'],
            'Well': defaults.DEFAULT_ITEMS['Well'],
            'Curves': defaults.DEFAULT_ITEMS['Curves'],
            'Parameter': defaults.DEFAULT_ITEMS['Parameter'],
            'Other': str(defaults.DEFAULT_ITEMS['Other']),
        }

        if not (file_ref is None):
            self.read(file_ref, **kwargs)

    def read(self, file_ref, null_subs=True, **kwargs):
        '''Read a LAS file.

        Arguments:
            file_ref: either a filename, an open file object, or a string of
                a LAS file contents.

        Keyword Arguments:
            encoding (str): character encoding to open file_ref with
            encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
                handle errors with encodings (see standard library codecs module or
                Python Unicode HOWTO for more information)
            autodetect_encoding (bool): use chardet/cchardet to detect encoding
            autodetect_encoding_chars (int/None): number of chars to read from LAS
                file for auto-detection of encoding.

        '''

        f = reader.open_file(file_ref, **kwargs)

        self._text = f.read()
        logger.debug('LASFile.read LAS content is type %s' % type(self._text))

        read_parser = reader.Reader(self._text, version=1.2)
        self.sections['Version'] = read_parser.read_section('~V')

        # Set version
        try:
            # raise Exception('%s %s' % (type(self.version['VERS']), self.version['VERS']))
            read_parser.version = self.version['VERS'].value
        except KeyError:
            raise KeyError('No key VERS in ~V section')

        # Validate version
        try:
            assert read_parser.version in (1.2, 2)
        except AssertionError:
            logger.warning('LAS spec version is %s -- neither 1.2 nor 2' %
                           read_parser.version)
            if read_parser.version < 2:
                read_parser.version = 1.2
            else:
                read_parser.version = 2
        read_parser.wrap = self.version['WRAP'].value == 'YES'

        self.sections['Well'] = read_parser.read_section('~W')
        self.sections['Curves'] = read_parser.read_section('~C')
        try:
            self.sections['Parameter'] = read_parser.read_section('~P')
        except exceptions.LASHeaderError:
            logger.warning(traceback.format_exc().splitlines()[-1])
        self.sections['Other'] = read_parser.read_raw_text('~O')

        # Deal with nonstandard sections that some operators and/or
        # service companies (eg IHS) insist on adding.
        s, d = read_parser.read_raw_text(r'~[BDEFGHIJKLMNQRSTUXYZ]',
                                                return_section=True)
        if d is not None:
            logger.warning('Found nonstandard LAS section: ' + s)
            self.sections[s] = d

        # Set null value
        read_parser.null = self.well['NULL'].value

        data = read_parser.read_data(len(self.curves), null_subs=null_subs)
        self.set_data(data, truncate=False)

        if (self.well['STRT'].unit.upper() == 'M' and
                self.well['STOP'].unit.upper() == 'M' and
                self.well['STEP'].unit.upper() == 'M' and
                self.curves[0].unit.upper() == 'M'):
            self.index_unit = 'M'
        elif (self.well['STRT'].unit.upper() in ('F', 'FT') and
              self.well['STOP'].unit.upper() in ('F', 'FT') and
              self.well['STEP'].unit.upper() in ('F', 'FT') and
              self.curves[0].unit.upper() in ('F', 'FT')):
            self.index_unit = 'FT'

    def write(self, file_object, version=None, wrap=None,
              STRT=None, STOP=None, STEP=None, fmt='%10.5g'):
        '''Write to a file.

        Arguments:
            file_object: a file_like object opening for writing.
            version (float): either 1.2 or 2
            wrap (bool): True, False, or None (last uses WRAP item in version)
            STRT (float): optional override to automatic calculation using 
                the first index curve value.
            STOP (float): optional override to automatic calculation using 
                the last index curve value.
            STEP (float): optional override to automatic calculation using 
                the first step size in the index curve.
            fmt (str): format string for numerical data being written to data
                section.

        Examples:

            >>> with open('test_output.las', mode='w') as f:
            ...     lasfile_obj.write(f, 2.0)   # <-- this method

        '''
        writer.write(self, file_object, version=version, wrap=wrap,
                     STRT=STRT, STOP=STOP, STEP=STEP, fmt=fmt)

    def get_curve(self, mnemonic):
        '''Return Curve object.

        Arguments:
            mnemonic (str): the name of the curve

        Returns: 
            A Curve object, not just the data array.

        '''
        for curve in self.curves:
            if curve.mnemonic == mnemonic:
                return curve

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.curves[key].data
        elif isinstance(key, str):
            if key in self.keys():
                return self.curves[key].data
        else:
            super(LASFile, self).__getitem__(key)

    def __setitem__(self, key, value):
        assert NotImplementedError('not yet')

    def keys(self):
        return [c.mnemonic for c in self.curves]

    def values(self):
        return [c.data for c in self.curves]

    def items(self):
        return [(c.mnemonic, c.data) for c in self.curves]

    def iterkeys(self):
        return iter(list(self.keys()))

    def itervalues(self):
        return iter(list(self.values()))

    def iteritems(self):
        return iter(list(self.items()))

    @property
    def version(self):
        return self.sections['Version']

    @version.setter
    def version(self, section):
        self.sections['Version'] = section

    @property
    def well(self):
        return self.sections['Well']

    @well.setter
    def well(self, section):
        self.sections['Well'] = section

    @property
    def curves(self):
        return self.sections['Curves']

    @curves.setter
    def curves(self, section):
        self.sections['Curves'] = section

    @property
    def params(self):
        return self.sections['Parameter']

    @params.setter
    def params(self, section):
        self.sections['Parameter'] = section

    @property
    def other(self):
        return self.sections['Other']

    @other.setter
    def other(self, section):
        self.sections['Other'] = section

    @property
    def metadata(self):
        s = SectionItems()
        for section in self.sections:
            for item in section:
                s.append(item)
        return s

    @metadata.setter
    def metadata(self, value):
        raise Warning('Set values in the version/well/params attrs directly')

    def df(self):
        import pandas as pd
        df = pd.DataFrame(self.data, columns=[c.mnemonic for c in self.curves])
        if len(self.curves) > 0:
            df = df.set_index(self.curves[0].mnemonic)
        return df

    def set_data(self, array_like, names=None, truncate=False):
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
        df_values = np.vstack([df.index.values, df.values.T]).T
        names = [df.index.name] + [str(name) for name in df.columns.values]
        self.set_data(df_values, names=names, **kwargs)

    @property
    def index(self):
        return self.curves[0].data

    @property
    def depth_m(self):
        if self.index_unit == 'M':
            return self.index
        elif self.index_unit == 'FT':
            return self.index * 0.3048
        else:
            raise exceptions.LASUnknownUnitError(
                'Unit of depth index not known')

    @property
    def depth_ft(self):
        if self.index_unit == 'M':
            return self.index / 0.3048
        elif self.index_unit == 'FT':
            return self.index
        else:
            raise exceptions.LASUnknownUnitError(
                'Unit of depth index not known')

    def add_curve(self, mnemonic, data, unit='', descr='', value=''):
        curve = CurveItem(mnemonic, unit, value, descr)
        if hasattr(self, 'data'):
            self.data = np.column_stack([self.data, data])
        else:
            self.data = np.column_stack([data])
        curve.data = self.data[:, -1]
        self.curves[mnemonic] = curve

    @property
    def header(self):
        return self.sections


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
