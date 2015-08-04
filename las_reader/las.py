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
__version__ = "0.5.2"


HeaderItem = namedlist("HeaderItem", ["mnemonic", "unit", "value", "descr"])
Curve = namedlist("Curve", ["mnemonic", "unit", "value", "descr", "data"])


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
        ("VERS", HeaderItem("VERS", "", 2.0,
                            "CWLS log ASCII Standard -VERSION 2.0")),
        ("WRAP", HeaderItem("WRAP", "", "NO", "One line per depth step")),
        ("DLM",  HeaderItem("DLM", "", "SPACE",
                            "Column Data Section Delimiter"))]),
    "well": OrderedDictionary([
        ("STRT", HeaderItem("STRT", "m", numpy.nan, "START DEPTH")),
        ("STOP", HeaderItem("STOP", "m", numpy.nan, "STOP DEPTH")),
        ("STEP", HeaderItem("STEP", "m", numpy.nan, "STEP")),
        ("NULL", HeaderItem("NULL", "", -9999.25, "NULL VALUE")),
        ("COMP", HeaderItem("COMP", "", "", "COMPANY")),
        ("WELL", HeaderItem("WELL", "", "", "WELL")),
        ("FLD",  HeaderItem("FLD", "", "", "FIELD")),
        ("LOC",  HeaderItem("LOC", "", "", "LOCATION")),
        ("PROV", HeaderItem("PROV", "", "", "PROVINCE")),
        ("CNTY", HeaderItem("CNTY", "", "", "COUNTY")),
        ("STAT", HeaderItem("STAT", "", "", "STATE")),
        ("CTRY", HeaderItem("CTRY", "", "", "COUNTRY")),
        ("SRVC", HeaderItem("SRVC", "", "", "SERVICE COMPANY")),
        ("DATE", HeaderItem("DATE", "", "", "DATE")),
        ("UWI",  HeaderItem("UWI", "", "", "UNIQUE WELL ID")),
        ("API",  HeaderItem("API", "", "", "API NUMBER"))
    ]),
    "curves": [],
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

        # Validate version
        try:
            assert reader.version in (1.2, 2)
        except AssertionError:
            logger.warning("LAS spec version is %s -- neither 1.2 nor 2" % 
                           reader.version)
            if reader.version < 2:
                reader.version = 1.2
            else:
                reader.version = 2
        reader.wrap = self.version['WRAP'].value == 'YES'

        self.well = reader.read_section('~W')
        self.curves = reader.read_list_section('~C')
        self.params = reader.read_section('~P')
        self.other = reader.read_raw_text('~O')

        # Set null value
        reader.null = self.well['NULL'].value

        data = reader.read_data(len(self.curves))

        for i, c in enumerate(self.curves):
            d = data[:, i]
            c.data = d
        self.refresh()
        
    def refresh(self):
        '''Refresh curve names and indices.'''
        n = len(self.curves)
        curve_names = [c.mnemonic for c in self.curves]
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
                c.mnemonic += "[%d]" % (curve_count[c.mnemonic] - 1, )

        for i, c in enumerate(self.curves):
            self[c.mnemonic] = c.data
            self[i] = c.data
            self[i - n] = c.data

    @property
    def data(self):
        '''2D array of data from LAS file.'''
        return numpy.vstack([c.data for c in self.curves]).T

    def write(self, file_object, version=None, 
              STRT=None, STOP=None, STEP=None):
        '''Write to a file.

        Args:
          file_object: a file_like object opening for writing.
          version (float): either 1.2 or 2
          STRT, STOP, STEP (float): optional overrides to automatic
            calculation. By default STRT and STOP are the first and last 
            index curve values, and STEP is the first step size in the
            index curve.

        Example usage:

            >>> with open("test_output.las", mode="w") as f:
            ...     lasfile_obj.write(f, 2.0)   # <-- this method

        '''
        lines = []

        assert version in (1.2, 2, None)
        if version is None:
            version = self.version["VERS"].value
        if version == 1.2:
            self.version["VERS"] = HeaderItem(
                "VERS", "", 1.2, "CWLS LOG ASCII STANDARD - VERSION 1.2")
        elif version == 2:
            self.version["VERS"] = HeaderItem(
                "VERS", "", 2.0, "CWLS log ASCII Standard -VERSION 2.0")

        if STRT is None:
            STRT = self.index[0]
        if STOP is None:
            STOP = self.index[-1]
        if STEP is None:
            STEP = self.index[1] - self.index[0]  # Faster than numpy.gradient
        self.well["STRT"].value = STRT
        self.well["STOP"].value = STOP
        self.well["STEP"].value = STEP

        # ~Version
        lines.append("~Version ".ljust(60, "-"))
        section_widths = {
            "left_width": None,
            "middle_width": None
        }
        order_func = get_section_order_function("version", version)
        for mnemonic, header_item in self.version.items():
            logger.debug(str(header_item))
            order = order_func(mnemonic)
            logger.debug("order = %s" % (order, ))
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Well
        lines.append("~Well ".ljust(60, "-"))
        section_widths = {
            "left_width": None,
            "middle_width": None
        }
        order_func = get_section_order_function("well", version)
        for mnemonic, header_item in self.well.items():
            order = order_func(mnemonic)
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Curves
        lines.append("~Curves ".ljust(60, "-"))
        section_widths = {
            "left_width": None,
            "middle_width": None
        }
        order_func = get_section_order_function("curves", version)
        for header_item in self.curves:
            order = order_func(header_item.mnemonic)
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Params
        lines.append("~Params ".ljust(60, "-"))
        section_widths = {
            "left_width": None,
            "middle_width": None
        }
        order_func = get_section_order_function("params", version)
        for mnemonic, header_item in self.params.items():
            order = order_func(mnemonic)
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Other
        lines.append("~Other ".ljust(60, "-"))
        lines += self.other.splitlines()

        lines.append("~ASCII ".ljust(60, "-"))

        file_object.write("\n".join(lines))
        file_object.write("\n")

        data_arr = numpy.column_stack([c.data for c in self.curves])
        nrows, ncols = data_arr.shape

        def format_data_section_line(n, fmt="%10.5g", l=10, spacer=" "):
            if numpy.isnan(n):
                return spacer + str(self.well["NULL"].value).rjust(l)
            else:
                return spacer + (fmt % n).rjust(l)

        for i in range(nrows):
            line = ''
            for j in range(ncols):
                line += format_data_section_line(data_arr[i, j])
            file_object.write(line + "\n")

    def get_curve(self, mnemonic):
        '''Return Curve object.

        Args:
          mnemonic (str): the name of the curve

        Returns: Curve object (i.e. not just the data array).

        '''
        for curve in self.curves:
            if curve.mnemonic == mnemonic:
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

    def add_curve(self, mnemonic, data, unit="", descr="", value=""):
        curve = Curve(mnemonic, unit, value, descr, data)
        self.curves.append(curve)
        self.refresh()

    @property
    def header(self):
        return OrderedDictionary([
            ("~V", self.version),
            ("~W", self.well), 
            ("~C", self.curves),
            ("~P", self.params),
            ("~O", self.other)])
    



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
            eol_chars = r"[\n\t\r]"
            s = re.sub(eol_chars, " ", s)
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
            return HeaderItem(keys["name"], keys["unit"],
                              self.num(keys["value"]), keys["descr"])
        elif key_order == "descr:value":
            return HeaderItem(keys["name"], keys["unit"], keys["descr"],
                              self.num(keys["value"]))

    def curves(self, **keys):
        return Curve(keys['name'], keys['unit'], keys['value'],
                     keys['descr'], None)

    def params(self, **keys):
        return HeaderItem(keys['name'], keys['unit'], self.num(keys['value']),
                          keys['descr'])


def read_line(line, pattern=None):
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
    if pattern is None:
        pattern = (r"\.?(?P<name>[^.]+)\." +
                   r"(?P<unit>[^\s:]*)" +
                   r"(?P<value>[^:]*):" +
                   r"(?P<descr>.*)")
    m = re.match(pattern, line)
    for key, value in m.groupdict().items():
        d[key] = value.strip()
        if key == "unit":
            if d[key].endswith("."):
                d[key] = d[key].strip(".") # see issue #36
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
    if isinstance(file_ref, str):
        if os.path.exists(file_ref):
            encoding = None
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
            file_ref = codecs.open(file_ref, mode="r", encoding=encoding)
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
    if left_width is None:
        left_width = 10
    if middle_width is None:
        middle_width = 40
    mnemonic_func = lambda mnemonic: mnemonic.ljust(left_width)
    middle_func = lambda unit, right_hand_item: (
        unit
        + " " * (middle_width - len(str(unit)) - len(right_hand_item))
        + right_hand_item
    )
    if order == "descr:value":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.mnemonic),
            middle_func(str(item.unit), str(item.descr)),
            item.value
        )
    elif order == "value:descr":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.mnemonic),
            middle_func(str(item.unit), str(item.value)),
            item.descr
        )


def get_section_order_function(section, version,
                               order_definitions=ORDER_DEFINITIONS):
    '''Get a function that returns the order per mnemonic and section.

    Args:
      section (str): either "well", "params", "curves", "version"
      version (float): either 1.2 and 2.0

    Kwargs:
      order_definitions (dict): 

    Returns a function which takes a mnemonic (str) as its only argument, and
    in turn returns the order "value:descr" or "descr:value".

    '''
    section_orders = order_definitions[version][section]
    default_order = section_orders[0]
    orders = {}
    for order, mnemonics in section_orders[1:]:
        for mnemonic in mnemonics:
            orders[mnemonic] = order
    return lambda mnemonic: orders.get(mnemonic, default_order)
