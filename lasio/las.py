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
            raw_section = self.match_section(pattern)
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
        s = self.match_section("~O")

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
            s = self.match_section("~A")
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

    def match_section(self, pattern, re_func="match", flags=re.IGNORECASE):
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
        return False

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

    def add_curve(self, *args, **kwargs):
        if isinstance(args[0], CurveItem):
            for curve in args:
                self.curves.append(curve)
        else:
            self.add_curve_raw(*args, **kwargs)

    def add_curve_raw(self, mnemonic, data, unit='', descr='', value=''):
        curve = CurveItem(mnemonic, unit, value, descr)
        if hasattr(self, 'data'):
            self.data = np.column_stack([self.data, data])
        else:
            self.data = np.column_stack([data])
        curve.data = self.data[:, -1]
        self.curves.append(curve)

    def delete_curve(self, mnemonic):
        ix = self.curves.keys().index(mnemonic)
        self.curves.pop(ix)
        self.data = np.delete(self.data, np.s_[ix], axis=1)

    @property
    def header(self):
        return self.sections

    @property
    def curvesdict(self):
        d = {}
        for curve in self.curves:
            d[curve['mnemonic']] = curve
        return d

    @property
    def json(self):
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
