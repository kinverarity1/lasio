'''las.py - read Log ASCII Standard files

See README.md and LICENSE for more information.

'''
from __future__ import print_function

# Standard library packages
import codecs
import collections
import logging
import os
import re
try:
    import cStringIO as StringIO
except ImportError:
    try:  # cStringIO not available on this system
        import StringIO
    except ImportError:  # Python 3
        from io import StringIO
    else:
        from StringIO import StringIO
else:
    from StringIO import StringIO
import traceback

# Third-party packages available on PyPi
from namedlist import namedlist
import numpy


logger = logging.getLogger(__name__)
__version__ = "0.4"


Metadata = namedlist('Metadata', ['mnemonic', 'unit', 'value', 'descr'])
Curve = namedlist('Curve', ['mnemonic', 'unit', 'API_code', 'descr', 'data',
                            'name'])
Parameter = namedlist('Parameter', ['mnemonic', 'unit', 'value', 'descr'])


class LASDataError(Exception):

    '''Error during reading of numerical data from LAS file.'''
    pass


class LASHeaderError(Exception):

    '''Error during reading of header data from LAS file.'''
    pass


class OrderedDictionary(collections.OrderedDict):

    '''A minor wrapper over collections.OrderedDict.

    This wrapper has a better string representation.

    '''

    def __repr__(self):
        l = []
        for key, value in self.items():
            s = "'%s': %s" % (key, value)
            l.append(s)
        s = '{' + ',\n '.join(l) + '}'
        return s

    @property
    def _d(self):
        if hasattr(list(self.values())[0], 'value'):
            return dict([(k, v.value) for k, v in list(self.items())])
        else:
            return dict([(k, v.descr) for k, v in list(self.items())])


DEFAULT_ITEMS = {
    "version": OrderedDictionary([
        ("VERS", Metadata("VERS", "", 2.0,
                          "CWLS log ASCII Standard -VERSION 2.0")),
        ("WRAP", Metadata("WRAP", "", "NO", "One line per depth step")),
        ("DLM",  Metadata("DLM", "", "SPACE",
                          "Column Data Section Delimiter"))]),
    "well": OrderedDictionary([
        ("STRT", Metadata("STRT", "m", numpy.nan, "START DEPTH")),
        ("STOP", Metadata("STOP", "m", numpy.nan, "STOP DEPTH")),
        ("STEP", Metadata("STEP", "m", numpy.nan, "STEP")),
        ("NULL", Metadata("NULL", "", -9999.25, "NULL VALUE")),
        ("COMP", Metadata("COMP", "", -9999.25, "COMPANY")),
        ("WELL", Metadata("WELL", "", -9999.25, "WELL")),
        ("FLD",  Metadata("FLD", "", -9999.25, "FIELD")),
        ("LOC",  Metadata("LOC", "", -9999.25, "LOCATION")),
        ("PROV", Metadata("PROV", "", -9999.25, "PROVINCE")),
        ("CNTY", Metadata("CNTY", "", -9999.25, "COUNTY")),
        ("STAT", Metadata("STAT", "", -9999.25, "STATE")),
        ("CTRY", Metadata("CTRY", "", -9999.25, "COUNTRY")),
        ("SRVC", Metadata("SRVC", "", -9999.25, "SERVICE COMPANY")),
        ("DATE", Metadata("DATE", "", -9999.25, "DATE")),
        ("UWI",  Metadata("UWI", "", -9999.25, "UNIQUE WELL ID")),
        ("API",  Metadata("API", "", -9999.25, "API NUMBER"))
    ]),
    "curves": [
        ("DEPT", Curve("DEPT", "m", "API code", "1 :   DEPTH", [], "DEPT"))
    ],
    "params": OrderedDictionary([]),
    "other": "",
    "data": numpy.zeros(shape=(0, 1))}

ORDER_DEFINITIONS = {
    1.2: {"version": ["value:descr"],
          "well":    ["descr:value",
                      ("value:descr", ["STRT", "STOP", "STEP", "NULL"])],
          "curves":  ["value:descr"],
          "params":  ["value:descr"]},
    2.0: {"version": ["value:descr"],
          "well":    ["value:descr"],
          "curves":  ["value:descr"],
          "params":  ["value:descr"]}}


class LASFile(OrderedDictionary):

    '''LAS file object.

    Kwargs:
      file_ref: either a filename, an open file object, or a string of
        a LAS file contents.
      encoding (str): character encoding to open file_ref with
      autodetect_encoding (bool): use chardet/ccharet to detect encoding
      autodetect_encoding_chars (int/None): number of chars to read from LAS
        file for auto-detection of encoding.

    '''

    def __init__(self, file_ref=None, encoding=None,
                 autodetect_encoding=False, autodetect_encoding_chars=20000):
        OrderedDictionary.__init__(self)

        self._text = ''
        self.version = OrderedDictionary(DEFAULT_ITEMS["version"].items())
        self.well = OrderedDictionary(DEFAULT_ITEMS["well"].items())
        self.curves = list(DEFAULT_ITEMS["curves"])
        self.params = OrderedDictionary(DEFAULT_ITEMS["params"].items())
        self.other = str(DEFAULT_ITEMS["other"])

        if not (file_ref is None):
            self.read(file_ref, encoding=encoding,
                      autodetect_encoding=autodetect_encoding,
                      autodetect_encoding_chars=autodetect_encoding_chars)

    def read(self, file_ref, encoding=None,
             autodetect_encoding=False, autodetect_encoding_chars=20000):
        '''Read a LAS file.

        Args:
          file_ref: either a filename, an open file object, or a string of
            a LAS file contents.

        Kwargs:
          encoding (str): character encoding to open file_ref with
          autodetect_encoding (bool): use chardet/ccharet to detect encoding
          autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

        '''
        f = open_file(file_ref, encoding=encoding,
                      autodetect_encoding=autodetect_encoding,
                      autodetect_encoding_chars=autodetect_encoding_chars)

        self._text = f.read()
        reader = Reader(self._text, version=1.2)

        self.version = reader.read_section('~V')

        # Set version
        try:
            reader.version = self.version['VERS'].value
        except KeyError:
            raise KeyError("No key VERS in ~V section")
        reader.wrap = self.version['WRAP'].value == 'YES'

        self.well = reader.read_section('~W')
        self.curves = reader.read_list_section('~C')
        self.params = reader.read_section('~P')
        self.other = reader.read_raw_text('~O')

        # Set null value
        reader.null = self.well['NULL'].value

        data = reader.read_data(len(self.curves))

        n = len(self.curves)
        curve_names = [c.name for c in self.curves]
        curve_freq = {}
        curve_count = {}
        for curve_name in curve_names:
            if not curve_name in curve_freq:
                curve_freq[curve_name] = 1
            else:
                curve_freq[curve_name] += 1
            curve_count[curve_name] = 0
        for i, c in enumerate(self.curves):
            curve_count[c.mnemonic] += 1
            if curve_freq[c.mnemonic] > 1:
                c.name += '[%d]' % curve_count[c.mnemonic]

        for i, c in enumerate(self.curves):
            d = data[:, i]
            c.data = d
            if c.mnemonic in list(self.keys()):
                logger.warning('Multiple curves with the same mnemonic (%s).'
                               % c.mnemonic)
                self[c.name] = d
            else:
                self[c.name] = d
            self[i] = d
            self[i - n] = d

    @property
    def data(self):
        '''2D array of data from LAS file.'''
        return numpy.vstack([c.data for c in self.curves]).T

    def write(self, file, version=None):
        lines = []

        assert version in (1.2, 2, None)
        if version is None:
            version = self.version["VERS"].value
        if version == 1.2:
            self.version["VERS"] = Metadata(
                "VERS", "", 1.2, "CWLS LOG ASCII STANDARD - VERSION 1.2")
        elif version == 2:
            self.version["VERS"] = Metadata(
                "VERS", "", 2.0, "CWLS log ASCII Standard -VERSION 2.0")

            # CONTINUE WORKING HERE

        # TODO: Issue #5
        self.version['WRAP'] = Metadata(
            'WRAP', '', 'NO',  'One line per depth step')

        lines.append("~Version ".ljust(60, "-"))
        l_mnem = 0
        l_value = 0
        for vm in list(self.version.values()):
            if len(vm.mnemonic) > l_mnem:
                l_mnem = len(vm.mnemonic)
            if len(str(vm.value)) > l_value:
                l_value = len(str(vm.value))
        for vm in list(self.version.values()):
            vm_d = vm.todict()
            vm_d['mnemonic'] = vm_d['mnemonic'].rjust(l_mnem)
            vm_d['value'] = str(vm_d['value']).rjust(l_value)
            lines.append(VERS_FMT.format(**vm_d))

        # Write Well section
        self.well['NULL'] = Metadata('NULL', '', -999.25, '')

        lines.append('~Well '.ljust(60, '-'))
        l_left = 0
        left_rev = lambda rt: '{mnemonic}.{unit} {value}'.format(**rt.todict())
        left_norm = lambda rt: '{mnemonic}.{unit} {descr}'.format(
            **rt.todict())
        for wm in list(self.well.values()):
            if wm.mnemonic in WELL_REV_MNEMONICS:
                s_left = left_rev(wm)
            else:
                s_left = left_norm(wm)
            if len(s_left) > l_left:
                l_left = len(s_left)
        for wm in list(self.well.values()):
            wm_leftmost = '{mnemonic}.{unit}'.format(**wm.todict())
            if wm.mnemonic in WELL_REV_MNEMONICS:
                wm_left = wm_leftmost + str(wm.value).rjust(
                    l_left - len(wm_leftmost))
                lines.append(wm_left + ': ' + wm.descr)
            else:
                wm_left = wm_leftmost + str(wm.descr).rjust(
                    l_left - len(wm_leftmost))
                lines.append(wm_left + ': ' + wm.value)

        # Write Curves section
        lines.append('~Curves '.ljust(60, '-'))
        l_mnem_unit = 0
        l_API_code = 0
        for cm in self.curves:
            s_mnem_unit = '{mnemonic}.{unit}'.format(**cm.todict())
            if len(s_mnem_unit) > l_mnem_unit:
                l_mnem_unit = len(s_mnem_unit)
            s_API_code = str(cm.API_code)
            if len(s_API_code) > l_API_code:
                l_API_code = len(s_API_code)
        for cm in self.curves:
            s_left = '{mnemonic}.{unit}'.format(
                **cm.todict()).ljust(l_mnem_unit)
            s_right = str(cm.API_code).rjust(l_API_code)
            lines.append(s_left + ' ' + s_right + ': ' + cm.descr)

        # Write Params section
        lines.append('~Parameters '.ljust(60, '-'))
        l_mnem_unit = 0
        l_value = 0
        for pm in list(self.params.values()):
            s_mnem_unit = '{mnemonic}.{unit}'.format(**pm.todict())
            if len(s_mnem_unit) > l_mnem_unit:
                l_mnem_unit = len(s_mnem_unit)
            s_value = str(pm.value)
            if len(s_value) > l_value:
                l_value = len(s_value)
        for pm in list(self.params.values()):
            s_left = '{mnemonic}.{unit}'.format(
                **pm.todict()).ljust(l_mnem_unit)
            s_right = str(pm.value).rjust(l_value)
            lines.append(s_left + ' ' + s_right + ': ' + pm.descr)

        # Write Other section
        lines.append('~Other '.ljust(60, '-'))
        lines += self.other.split('\n')

        # Write Data section
        lines.append('~ASCII Data '.ljust(60, '-'))
        file.write('\n'.join(lines))
        file.write('\n')
        data_arr = numpy.column_stack([c.data for c in self.curves])
        nrows, ncols = data_arr.shape
        # FORMAT %10.5g

        def fmt(n, fmt='%10.5g', l=10, spacer=' '):
            if numpy.isnan(n):
                return spacer + str(self.well['NULL'].value).rjust(l)
            else:
                return spacer + (fmt % n).rjust(l)
        for i in range(nrows):
            line = ''
            for j in range(ncols):
                line += fmt(data_arr[i, j])
            file.write(line + '\n')
        # numpy.savetxt(file, data_arr, fmt='%10.5g')

    def get_curve_name(self, curve_name):
        for curve in self.curves:
            if curve.name == curve_name:
                return curve

    def keys(self):
        k = list(super(OrderedDictionary, self).keys())
        return [ki for ki in k if isinstance(ki, str)]

    def values(self):
        return [self[k] for k in list(self.keys())]

    def items(self):
        return [(k, self[k]) for k in list(self.keys())]

    def iterkeys(self):
        return iter(list(self.keys()))

    def itervalues(self):
        return iter(list(self.values()))

    def iteritems(self):
        return iter(list(self.items()))

    @property
    def metadata(self):
        d = {}
        for di in (self.version, self.well, self.params):
            for k, v in list(di.items()):
                d[k] = v.value
        return d

    @metadata.setter
    def metadata(self, value):
        raise Warning('Set values in the version/well/params attrs directly')

    @property
    def index(self):
        return self.data[:, 0]


class Las(LASFile):

    '''LAS file object.

    Retained for backwards compatibility.

    '''
    pass


class Reader(object):

    def __init__(self, text, version):
        self.lines = text.splitlines()
        self.version = version
        self.null = numpy.nan
        self.wrap = True

    @property
    def section_names(self):
        names = []
        for line in self.lines:
            line = line.strip().strip('\t').strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('~'):
                names.append(line)
        return names

    def iter_section_lines(self, section_name, ignore_comments=True):
        in_section = False
        for i, line in enumerate(self.lines):
            line = line.strip().strip('\t').strip()
            if not line:
                continue
            if ignore_comments and line.startswith('#'):
                continue
            if line.startswith(section_name):
                if in_section:
                    return
                else:
                    in_section = True
                    continue
            if line.lower().startswith('~') and in_section:
                # Start of the next section; we're done here.
                break
            if in_section:
                yield line

    def read_raw_text(self, section_name):
        return '\n'.join(self.iter_section_lines(section_name,
                                                 ignore_comments=False))

    def read_section(self, section_name):
        parser = SectionParser(section_name, version=self.version)
        d = OrderedDictionary()
        for line in self.iter_section_lines(section_name):
            try:
                values = read_line(line)
            except:
                raise LASHeaderError("Failed in %s section on line:\n%s%s" % (
                    section_name, line,
                    traceback.format_exc().splitlines()[-1]))
            else:
                d[values['name']] = parser(**values)
        return d

    def read_list_section(self, section_name):
        parser = SectionParser(section_name, version=self.version)
        l = []
        for line in self.iter_section_lines(section_name):
            try:
                values = read_line(line)
            except:
                raise LASHeaderError("Failed in %s section on line:\n%s%s" % (
                    section_name, line,
                    traceback.format_exc().splitlines()[-1]))
            else:
                l.append(parser(**values))
        return l

    def read_data(self, number_of_curves=None):
        s = self.read_data_string()
        if not self.wrap:
            try:
                arr = numpy.loadtxt(StringIO(s))
            except:
                raise LASDataError("Failed to read data:\n%s" % (
                                   traceback.format_exc().splitlines()[-1]))
        else:
            s = s.replace('\n', ' ').replace('\t', ' ')
            try:
                arr = numpy.loadtxt(StringIO(s))
            except:
                raise LASDataError("Failed to read wrapped data: %s" % (
                                   traceback.format_exc().splitlines()[-1]))
            logger.debug('arr shape = %s' % (arr.shape))
            logger.debug('number of curves = %s' % number_of_curves)
            arr = numpy.reshape(arr, (-1, number_of_curves))
        if not arr.shape or (arr.ndim == 1 and arr.shape[0] == 0):
            logger.warning('No data present.')
            return None, None
        else:
            logger.info('LAS file shape = %s' % str(arr.shape))
        logger.debug('checking for nulls (NULL = %s)' % self.null)
        arr[arr == self.null] = numpy.nan
        return arr

    def read_data_string(self):
        start_data = None
        for i, line in enumerate(self.lines):
            line = line.strip().strip('\t').strip()
            if line.startswith('~A'):
                start_data = i + 1
                break
        s = '\n'.join(self.lines[start_data:])
        s = re.sub(r'(\d)-(\d)', r'\1 -\2', s)
        s = re.sub('-?\d*\.\d*\.\d*', ' NaN NaN ', s)
        s = re.sub('NaN.\d*', ' NaN NaN ', s)
        return s


class SectionParser(object):

    def __init__(self, section_name, version=1.2):
        if section_name.startswith('~C'):
            self.func = self.curves
        elif section_name.startswith('~P'):
            self.func = self.params
        else:
            self.func = self.metadata

        self.version = version
        self.section_name = section_name
        self.section_name2 = {"~C": "curves",
                              "~W": "well",
                              "~V": "version",
                              "~P": "params"}[section_name]

        section_orders = ORDER_DEFINITIONS[self.version][self.section_name2]
        self.default_order = section_orders[0]
        self.orders = {}
        for order, mnemonics in section_orders[1:]:
            for mnemonic in mnemonics:
                self.orders[mnemonic] = order

    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        return self.num(r, default=r)

    def num(self, x, default=None):
        if default is None:
            default = x
        try:
            return numpy.int(x)
        except:
            try:
                return numpy.float(x)
            except:
                return default

    def metadata(self, **keys):
        key_order = self.orders.get(keys["name"], self.default_order)
        if key_order == "value:descr":
            return Metadata(keys["name"], keys["unit"],
                            self.num(keys["value"]), keys["descr"])
        elif key_order == "descr:value":
            return Metadata(keys["name"], keys["unit"], keys["descr"],
                            self.num(keys["value"]))

    def curves(self, **keys):
        return Curve(keys['name'], keys['unit'], keys['value'],
                     keys['descr'], None, keys['name'])

    def params(self, **keys):
        return Parameter(keys['name'], keys['unit'], self.num(keys['value']),
                         keys['descr'])


def read_line(line):
    '''Read a line from a LAS header section.

    Args:
      line (str): line from a LAS header section

    Returns: dict with keys "name", "unit", "value", and "descr", each
    containing a string as value.

    The line is parsed with a regular expression -- see LAS file specs for
    more details, but it should basically be in the format:

        name.unit       value : descr

    '''

    d = {}
    pattern = (r"(?P<name>[^.]+)\." +
               r"(?P<unit>[^\s:]*)" +
               r"(?P<value>[^:]*):" +
               r"(?P<descr>.*)")
    m = re.match(pattern, line)
    for key, value in m.groupdict().items():
        d[key] = value.strip()
    return d


def open_file(file_ref, encoding=None,
              autodetect_encoding=False, autodetect_encoding_chars=20000):
    '''Open a file if necessary.

    Args:
      file_ref: either a filename, an open file object, or a string of
        a LAS file contents.

    Kwargs:
      encoding (str): character encoding to open file_ref with
      autodetect_encoding (bool): use chardet/ccharet to detect encoding
      autodetect_encoding_chars (int/None): number of chars to read from LAS
        file for auto-detection of encoding.

    Returns: an open file object.

    If autodetect_encoding is True then either cchardet or chardet (see PyPi)
    needs to be installed, or else an ImportError will be raised.

    '''
    if isinstance(file_ref, basestring):
        if os.path.exists(file_ref):
            if autodetect_encoding:
                try:
                    import cchardet as chardet
                except ImportError:
                    try:
                        import chardet
                    except ImportError:
                        raise ImportError("chardet or cchardet is required for"
                                          " automatic detection of character"
                                          " encodings.")
                with open(file_ref, mode="rb") as test_file:
                    chunk = test_file.read(autodetect_encoding_chars)
                    result = chardet.detect(chunk)
                    encoding = result["encoding"]
            file_ref = codecs.open(file_ref, mode="r", encoding=None)
        else:
            file_ref = StringIO(file_ref)
    return file_ref


def get_formatter_function(order, left_width=None, middle_width=None):
    '''Create function to format a LAS header item.

    Args:
      order: format of item, either "descr:value" or "value:descr" -- see
        LAS 1.2 and 2.0 specifications for more information.

    Kwargs:
      left_width (int): number of characters to the left hand side of the
        first period
      middle_width (int): total number of characters minus 1 between the 
        first period from the left and the first colon from the left.

    Returns a function which takes a header item (e.g. Metadata, Curve, 
    Parameter) as its single argument and which in turn returns a string
    which is the correctly formatted LAS header line.

    '''
    mnemonic_func = lambda mnemonic: mnemonic.ljust(left_width)
    middle_func = lambda unit, right_hand_item: (
        unit + " " * (middle_width - len(unit) - len(right_hand_item))
        + right_hand_item)
    if order == "descr:value":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.mnemonic), middle_func(unit, item.descr),
            item.value)
    elif order == "value:descr":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.mnemonic), middle_func(unit, item.value),
            item.descr)
