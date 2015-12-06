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

# The standard library OrderedDict was introduced in Python 2.7 so
# we have a third-party option to support Python 2.6

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

# Convoluted import for StringIO in order to support:
#
# - Python 3 - io.StringIO
# - Python 2 (optimized) - cStringIO.StringIO
# - Python 2 (all) - StringIO.StringIO

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

# Required third-party packages available on PyPi:

from namedlist import namedlist
import numpy

# Optional third-party packages available on PyPI are mostly
# imported inline below.


logger = logging.getLogger(__name__)
__version__ = "0.9.1"


class LASDataError(Exception):

    '''Error during reading of numerical data from LAS file.'''
    pass


class LASHeaderError(Exception):

    '''Error during reading of header data from LAS file.'''
    pass


class LASUnknownUnitError(Exception):

    '''Error of unknown unit in LAS file.'''
    pass


class HeaderItem(OrderedDict):
    def __init__(self, mnemonic, unit="", value="", descr=""):
        
        # The original mnemonic needs to be stored for rewriting a new file.
        # it might be nothing - '' - or a duplicate e.g. two 'RHO' curves,
        # or unique - 'X11124' - or perhaps invalid??

        self.original_mnemonic = mnemonic

        # We also need to store a more useful mnemonic, which will be used
        # (technically not, but read on) for people to access the curve while
        # the LASFile object exists. For example, a curve which is unnamed
        # and has the mnemonic '' will be accessed via 'UNKNOWN'.

        if mnemonic.strip() == '':
            self.useful_mnemonic = 'UNKNOWN'
        else:
            self.useful_mnemonic = mnemonic

        # But note that we need to (later) check (repeatedly) for duplicate
        # mnemonics. Any duplicates will have ':1', ':2', ':3', etc., appended
        # to them. The result of this will be stored in the below variable,
        # which is what the user should actually see and use 99.5% of the time.

        self.mnemonic = self.useful_mnemonic

        self.unit = unit
        self.value = value
        self.descr = descr

    def __getitem__(self, key):
        if key == 'mnemonic':
            return self.mnemonic
        elif key == 'original_mnemonic':
            return self.original_mnemonic
        elif key == 'useful_mnemonic':
            return self.useful_mnemonic
        elif key == 'unit':
            return self.unit
        elif key == 'value':
            return self.value
        elif key == 'descr':
            return self.descr
        else:
            super(HeaderItem, self).__getitem__(key)

    def __repr__(self):
        return (
            "%s(mnemonic=%s, unit=%s, value=%s, "
            "descr=%s, original_mnemonic=%s)" % (
                self.__class__.__name__, self.mnemonic, self.unit, self.value, 
                self.descr, self.original_mnemonic))


class CurveItem(HeaderItem):
    @property
    def API_code(self):
        return self.value
    


class SectionItems(list):

    def __contains__(self, testitem):
        '''Allows testing of a mnemonic or an actual item.'''
        for item in self:
            if testitem == item.mnemonic:
                return True 
            elif testitem.mnemonic == item.mnemonic:
                return True
            elif testitem is item:
                return True
        else:
            return False

    def keys(self):
        return [item.mnemonic for item in self]

    def values(self):
        return self

    def items(self):
        return [(item.mnemonic, item) for item in self]

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self)

    def iteritems(self):
        return iter(self.items())

    def __getitem__(self, key):
        for item in self:
            if item.mnemonic == key:
                return item
        if isinstance(key, int):
            return super(SectionItems, self).__getitem__(key)
        else:
            raise KeyError("%s not in %s" % (key, self.keys()))

    def __setitem__(self, key, newitem):
        for i, item in enumerate(self):
            if key == item.mnemonic:

                # This is very important. We replace items where
                # 'mnemonic' is equal - i.e. we do not check useful_mnemonic
                # or original_mnemonic. Is this correct? Needs to thought
                # about and tested more carefully.

                logger.debug('SectionItems.__setitem__ Replaced %s item' % key)
                return super(SectionItems, self).__setitem__(i, newitem)  
        else:
            self.append(newitem)

    def append(self, newitem):
        '''Check to see if the item's mnemonic needs altering.'''
        logger.debug("SectionItems.append type=%s str=%s" % (type(newitem), newitem))
        super(SectionItems, self).append(newitem)

        # Check to fix the :n suffixes
        existing = [item.useful_mnemonic for item in self]
        locations = []
        for i, item in enumerate(self):
            if item.useful_mnemonic == newitem.mnemonic:
                locations.append(i)
        if len(locations) > 1:
            current_count = 1
            for i, loc in enumerate(locations):
                item = self[loc]
                # raise Exception("%s" % str(type(item)))
                item.mnemonic = item.useful_mnemonic + ":%d" % (i + 1)



class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return list(obj)
        return json.JSONEncoder(self, obj)



DEFAULT_ITEMS = {
    "Version": [
        HeaderItem("VERS", "", 2.0, "CWLS log ASCII Standard -VERSION 2.0"),
        HeaderItem("WRAP", "", "NO", "One line per depth step"),
        HeaderItem("DLM", "", "SPACE", "Column Data Section Delimiter"),
        ],
    "Well": [
        HeaderItem("STRT", "m", numpy.nan, "START DEPTH"),
        HeaderItem("STOP", "m", numpy.nan, "STOP DEPTH"),
        HeaderItem("STEP", "m", numpy.nan, "STEP"),
        HeaderItem("NULL", "", -9999.25, "NULL VALUE"),
        HeaderItem("COMP", "", "", "COMPANY"),
        HeaderItem("WELL", "", "", "WELL"),
        HeaderItem("FLD", "", "", "FIELD"),
        HeaderItem("LOC", "", "", "LOCATION"),
        HeaderItem("PROV", "", "", "PROVINCE"),
        HeaderItem("CNTY", "", "", "COUNTY"),
        HeaderItem("STAT", "", "", "STATE"),
        HeaderItem("CTRY", "", "", "COUNTRY"),
        HeaderItem("SRVC", "", "", "SERVICE COMPANY"),
        HeaderItem("DATE", "", "", "DATE"),
        HeaderItem("UWI", "", "", "UNIQUE WELL ID"),
        HeaderItem("API", "", "", "API NUMBER")
        ],
    "Curves": [],
    "Parameter": [],
    "Other": "",
    "Data": numpy.zeros(shape=(0, 1)),
    }


ORDER_DEFINITIONS = {
    1.2: OrderedDict([
        ("Version", ["value:descr"]),
        ("Well", [
            "descr:value",
            ("value:descr", ["STRT", "STOP", "STEP", "NULL"])]),
        ("Curves", ["value:descr"]),
        ("Parameter", ["value:descr"]),
        ]),
    2.0: OrderedDict([
        ("Version", ["value:descr"]),
        ("Well", ["value:descr"]),
        ("Curves", ["value:descr"]),
        ("Parameter", ["value:descr"])
        ])}


URL_REGEXP = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}'
    r'\.?|[A-Z0-9-]{2,}\.?)|'  # (cont.) domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class LASFile(OrderedDict):

    '''LAS file object.

    Keyword Arguments:
        file_ref: either a filename, an open file object, or a string of
            a LAS file contents.
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): "strict", "replace" (default), "ignore" - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    '''

    def __init__(self, file_ref=None, **kwargs):
        OrderedDict.__init__(self)

        self._text = ''
        self._use_pandas = "auto"
        self.index_unit = None
        self.sections = {
            "Version": DEFAULT_ITEMS["Version"],
            "Well": DEFAULT_ITEMS["Well"],
            "Curves": DEFAULT_ITEMS["Curves"],
            "Parameter": DEFAULT_ITEMS["Parameter"],
            "Other": str(DEFAULT_ITEMS["Other"]),
            }

        if not (file_ref is None):
            self.read(file_ref, **kwargs)

    def read(self, file_ref, use_pandas="auto", null_subs=True, **kwargs):
        '''Read a LAS file.

        Arguments:
            file_ref: either a filename, an open file object, or a string of
                a LAS file contents.

        Keyword Arguments:
            use_pandas (str): bool or "auto" -- use pandas if available -- provide
                False option for faster loading where pandas functionality is not
                needed. "auto" becomes True if pandas is installed, and False if not.
            encoding (str): character encoding to open file_ref with
            encoding_errors (str): "strict", "replace" (default), "ignore" - how to
                handle errors with encodings (see standard library codecs module or
                Python Unicode HOWTO for more information)
            autodetect_encoding (bool): use chardet/cchardet to detect encoding
            autodetect_encoding_chars (int/None): number of chars to read from LAS
                file for auto-detection of encoding.

        '''
        if not use_pandas is None:
            self._use_pandas = use_pandas

        f = open_file(file_ref, **kwargs)

        self._text = f.read()
        logger.debug("LASFile.read LAS content is type %s" % type(self._text))

        reader = Reader(self._text, version=1.2)
        self.sections["Version"] = reader.read_section('~V')

        # Set version
        try:
            # raise Exception("%s %s" % (type(self.version['VERS']), self.version["VERS"]))
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

        self.sections["Well"] = reader.read_section('~W')
        self.sections["Curves"] = reader.read_section('~C')
        try:
            self.sections["Parameter"] = reader.read_section('~P')
        except LASHeaderError:
            logger.warning(traceback.format_exc().splitlines()[-1])
        self.sections["Other"] = reader.read_raw_text('~O')

        # Set null value
        reader.null = self.well['NULL'].value

        data = reader.read_data(len(self.curves), null_subs=null_subs)

        for i, c in enumerate(self.curves):
            d = data[:, i]
            c.data = d

        if (self.well["STRT"].unit.upper() == "M" and
                self.well["STOP"].unit.upper() == "M" and
                self.well["STEP"].unit.upper() == "M" and
                self.curves[0].unit.upper() == "M"):
            self.index_unit = "M"
        elif (self.well["STRT"].unit.upper() in ("F", "FT") and
              self.well["STOP"].unit.upper() in ("F", "FT") and
              self.well["STEP"].unit.upper() in ("F", "FT") and
              self.curves[0].unit.upper() in ("F", "FT")):
            self.index_unit = "FT"

        self.refresh()

    def refresh(self, use_pandas=None):
        '''Refresh curve names and indices.'''
        if not use_pandas is None:
            self._use_pandas = use_pandas

        n = len(self.curves)
        for i, curve in enumerate(self.curves):
            self[curve.mnemonic] = curve.data
            self[i] = curve.data
            self[i - n] = curve.data

        if not self._use_pandas is False:
            try:
                import pandas
            except ImportError:
                logger.info(
                    "pandas not installed - skipping LASFile.df creation")
                self._use_pandas = False

        if self._use_pandas:
            self.df = pandas.DataFrame(self.data, columns=self.keys())
            self.df.set_index(self.curves[0].mnemonic, inplace=True)

    @property
    def data(self):
        '''2D array of data from LAS file.'''
        return numpy.vstack([c.data for c in self.curves]).T

    def write(self, file_object, version=None, wrap=None,
              STRT=None, STOP=None, STEP=None, fmt="%10.5g"):
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

            >>> with open("test_output.las", mode="w") as f:
            ...     lasfile_obj.write(f, 2.0)   # <-- this method

        '''
        if wrap is None:
            wrap = self.version["WRAP"] == "YES"
        elif wrap is True:
            self.version["WRAP"] = HeaderItem(
                "WRAP", "", "YES", "Multiple lines per depth step")
        elif wrap is False:
            self.version["WRAP"] = HeaderItem(
                "WRAP", "", "NO", "One line per depth step")
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


        # Check for any changes in the pandas dataframe and if there are,
        # create new curves so they are reflected in the output LAS file.

        if self._use_pandas:
            curve_names = lambda: [ci.mnemonic for ci in self.curves]
            for df_curve_name in list(self.df.columns.values):
                if not df_curve_name in curve_names():
                    self.add_curve(df_curve_name, self.df[df_curve_name])
        
        # Write each section.

        # ~Version
        logger.debug('LASFile.write Version section')
        lines.append("~Version ".ljust(60, "-"))
        order_func = get_section_order_function("Version", version)
        section_widths = get_section_widths("Version", self.version, version, order_func)
        for header_item in self.version.values():
            mnemonic = header_item.original_mnemonic
            # logger.debug("LASFile.write " + str(header_item))
            order = order_func(mnemonic)
            # logger.debug("LASFile.write order = %s" % (order, ))
            logger.debug('LASFile.write %s\norder=%s section_widths=%s' % (header_item, order, section_widths))
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Well
        logger.debug('LASFile.write Well section')
        lines.append("~Well ".ljust(60, "-"))
        order_func = get_section_order_function("Well", version)
        section_widths = get_section_widths("Well", self.well, version, order_func)
        # logger.debug('LASFile.write well section_widths=%s' % section_widths)
        for header_item in self.well.values():
            mnemonic = header_item.original_mnemonic
            order = order_func(mnemonic)
            logger.debug('LASFile.write %s\norder=%s section_widths=%s' % (header_item, order, section_widths))
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Curves
        logger.debug('LASFile.write Curves section')
        lines.append("~Curves ".ljust(60, "-"))
        order_func = get_section_order_function("Curves", version)
        section_widths = get_section_widths("Curves", self.curves, version, order_func)
        for header_item in self.curves:
            mnemonic = header_item.original_mnemonic
            order = order_func(mnemonic)
            formatter_func = get_formatter_function(order, **section_widths)
            line = formatter_func(header_item)
            lines.append(line)

        # ~Params
        lines.append("~Params ".ljust(60, "-"))
        order_func = get_section_order_function("Parameter", version)
        section_widths = get_section_widths("Parameter", self.params, version, order_func)
        for header_item in self.params.values():
            mnemonic = header_item.original_mnemonic
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

        def format_data_section_line(n, fmt, l=10, spacer=" "):
            if numpy.isnan(n):
                return spacer + str(self.well["NULL"].value).rjust(l)
            else:
                return spacer + (fmt % n).rjust(l)

        twrapper = textwrap.TextWrapper(width=79)
        for i in range(nrows):
            depth_slice = ''
            for j in range(ncols):
                depth_slice += format_data_section_line(data_arr[i, j], fmt)

            if wrap:
                lines = twrapper.wrap(depth_slice)
                logger.debug("LASFile.write Wrapped %d lines out of %s" %
                             (len(lines), depth_slice))
            else:
                lines = [depth_slice]

            if self.version["VERS"].value == 1.2:
                for line in lines:
                    if len(line) > 255:
                        logger.warning("LASFile.write Data line > 256 chars: %s" % line)

            for line in lines:
                file_object.write(line + "\n")

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
        return self.sections["Version"]
    
    @version.setter
    def version(self, section):
        self.sections["Version"] = section

    @property
    def well(self):
        return self.sections["Well"]
    
    @well.setter
    def well(self, section):
        self.sections["Well"] = section

    @property
    def curves(self):
        return self.sections["Curves"]
    
    @curves.setter
    def curves(self, section):
        self.sections["Curves"] = section

    @property
    def params(self):
        return self.sections["Parameter"]
    
    @params.setter
    def params(self, section):
        self.sections["Parameter"] = section

    @property
    def other(self):
        return self.sections["Other"]
    
    @other.setter
    def other(self, section):
        self.sections["Other"] = section
    

    @property
    def metadata(self):
        d = OrderedDict()
        for di in (self.version, self.well, self.params):
            for k, v in list(di.items()):
                d[k] = v.value
        return d

    @metadata.setter
    def metadata(self, value):
        raise Warning('Set values in the version/well/params attrs directly')

    @property
    def df(self):
        if self._use_pandas:
            return self._df
        else:
            logger.warning(
                "pandas is not installed or use_pandas was set to False")
            # raise Warning("pandas is not installed or use_pandas was set to False")

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def index(self):
        return self.data[:, 0]

    @property
    def depth_m(self):
        if self.index_unit == "M":
            return self.index
        elif self.index_unit == "FT":
            return self.index * 0.3048
        else:
            raise LASUnknownUnitError("Unit of depth index not known")

    @property
    def depth_ft(self):
        if self.index_unit == "M":
            return self.index / 0.3048
        elif self.index_unit == "FT":
            return self.index
        else:
            raise LASUnknownUnitError("Unit of depth index not known")

    def add_curve(self, mnemonic, data, unit="", descr="", value=""):
        # assert not mnemonic in self.curves
        curve = CurveItem(mnemonic, unit, value, descr)
        curve.data = data
        self.curves[mnemonic] = curve
        self.refresh()

    @property
    def header(self):
        return OrderedDict([
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
        section = SectionItems()
        for line in self.iter_section_lines(section_name):
            try:
                values = read_line(line)
            except:
                raise LASHeaderError("Failed in %s section on line:\n%s%s" % (
                    section_name, line,
                    traceback.format_exc().splitlines()[-1]))
            else:
                section.append(parser(**values))
        return section

    def read_data(self, number_of_curves=None, null_subs=True):
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
            logger.debug('Reader.read_data arr shape = %s' % (arr.shape))
            logger.debug('Reader.read_data number of curves = %s' % number_of_curves)
            arr = numpy.reshape(arr, (-1, number_of_curves))
        if not arr.shape or (arr.ndim == 1 and arr.shape[0] == 0):
            logger.warning('Reader.read_dataN o data present.')
            return None, None
        else:
            logger.info('Reader.read_data LAS file shape = %s' % str(arr.shape))
        logger.debug('Reader.read_data checking for nulls (NULL = %s)' % self.null)
        if null_subs:
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
        self.section_name2 = {"~C": "Curves",
                              "~W": "Well",
                              "~V": "Version",
                              "~P": "Parameter"}[section_name]

        section_orders = ORDER_DEFINITIONS[self.version][self.section_name2]
        self.default_order = section_orders[0]
        self.orders = {}
        for order, mnemonics in section_orders[1:]:
            for mnemonic in mnemonics:
                self.orders[mnemonic] = order

    def __call__(self, **keys):
        item = self.func(**keys)
        # if item.name == "":
        #     item.mnemonic = "UNKNOWN"
        return item

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
            return HeaderItem(
                keys["name"],                 # mnemonic
                keys["unit"],                 # unit
                self.num(keys["value"]),      # value
                keys["descr"],                # descr
                )
        elif key_order == "descr:value":
            return HeaderItem(
                keys["name"],                   # mnemonic
                keys["unit"],                   # unit
                keys["descr"],                  # descr
                self.num(keys["value"]),        # value
                )

    def curves(self, **keys):
        # logger.debug(str(keys))
        item = CurveItem(
            keys['name'],               # mnemonic
            keys['unit'],               # unit
            keys['value'],              # value
            keys['descr'],              # descr
            )
        # logger.debug(str(item))
        item.data = None
        return item

    def params(self, **keys):
        return HeaderItem(
            keys['name'],               # mnemonic
            keys['unit'],               # unit
            self.num(keys['value']),    # value
            keys['descr'],              # descr
            )


def read_line(line, pattern=None):
    '''Read a line from a LAS header section.

    The line is parsed with a regular expression -- see LAS file specs for
    more details, but it should basically be in the format::

        name.unit       value : descr

    Arguments:
        line (str): line from a LAS header section

    Returns:
        A dictionary with keys "name", "unit", "value", and "descr", each
        containing a string as value.

    '''
    d = {}
    if pattern is None:
        pattern = (r"\.?(?P<name>[^.]*)\." +
                   r"(?P<unit>[^\s:]*)" +
                   r"(?P<value>[^:]*):" +
                   r"(?P<descr>.*)")
    m = re.match(pattern, line)
    mdict = m.groupdict()
    # if mdict["name"] == "":
    #     mdict["name"] = "UNKNOWN"
    for key, value in mdict.items():
        d[key] = value.strip()
        if key == "unit":
            if d[key].endswith("."):
                d[key] = d[key].strip(".")  # see issue #36
    return d


def open_file(file_ref, encoding=None, encoding_errors="replace",
              autodetect_encoding=False, autodetect_encoding_chars=40e3):
    '''Open a file if necessary.

    If autodetect_encoding is True then either cchardet or chardet (see PyPi)
    needs to be installed, or else an ImportError will be raised.

    Arguments:
        file_ref: either a filename, an open file object, a URL, or a string of
            a LAS file contents.

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): "strict", "replace" (default), "ignore" - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: 
        An open file-like object ready for reading from.

    '''
    if isinstance(file_ref, str):
        lines = file_ref.splitlines()
        if len(lines) == 1:  # File name
            if URL_REGEXP.match(file_ref):
                try:
                    import urllib2
                    file_ref = urllib2.urlopen(file_ref)
                except ImportError:
                    import urllib.request
                    response = urllib.request.urlopen(file_ref)
                    enc = response.headers.get_content_charset("utf-8")
                    file_ref = StringIO(response.read().decode(enc))
            else:  # filename
                data = get_unicode_from_filename(
                    file_ref, encoding, encoding_errors, autodetect_encoding,
                    autodetect_encoding_chars)
                file_ref = StringIO(data)
        else:
            file_ref = StringIO("\n".join(lines))
    return file_ref


def get_unicode_from_filename(fn, enc, errors, auto, nbytes):
    '''
    Read Unicode data from file.

    Arguments:
        fn (str): path to file
        enc (str): encoding - can be None
        errors (str): unicode error handling - can be "strict", "ignore", "replace"
        auto (str): auto-detection of character encoding - can be either
            "chardet", "cchardet", or True
        nbytes (int): number of characters for read for auto-detection

    Returns:
        a unicode or string object

    '''
    if nbytes:
        nbytes = int(nbytes)

    # Detect BOM in UTF-8 files

    nbytes_test = min(32, os.path.getsize(fn))
    with open(fn, mode="rb") as test:
        raw = test.read(nbytes_test)
    if raw.startswith(codecs.BOM_UTF8):
        enc = "utf-8-sig"
        auto = False

    if auto:
        with open(fn, mode="rb") as test:
            if nbytes is None:
                raw = test.read()
            else:
                raw = test.read(nbytes)
        enc = get_encoding(auto, raw)

    # codecs.open is smarter than cchardet or chardet IME.

    with codecs.open(fn, mode="r", encoding=enc, errors=errors) as f:
        data = f.read()

    return data


def get_encoding(auto, raw):
    '''
    Automatically detect character encoding.

    Arguments:
        auto (str): auto-detection of character encoding - can be either
            "chardet", "cchardet", or True
        raw (bytes): array of bytes to detect from

    Returns:
        A string specifying the character encoding.

    '''
    if auto is True:
        try:
            import cchardet as chardet
        except ImportError:
            try:
                import chardet
            except ImportError:
                raise ImportError(
                    "chardet or cchardet is required for automatic"
                    " detection of character encodings.")
            else:
                logger.debug("get_encoding Using chardet")
                method = "chardet"
        else:
            logger.debug("get_encoding Using cchardet")
            method = "cchardet"
    elif auto.lower() == "chardet":
        import chardet
        logger.debug("get_encoding Using chardet")
        method = "chardet"
    elif auto.lower() == "cchardet":
        import cchardet as chardet
        logger.debug("get_encoding Using cchardet")
        method = "cchardet"

    result = chardet.detect(raw)
    logger.debug("get_encoding %s results=%s" % (method, result))
    return result["encoding"]


def get_formatter_function(order, left_width=None, middle_width=None):
    '''Create function to format a LAS header item.

    Arguments:
        order: format of item, either "descr:value" or "value:descr" -- see
            LAS 1.2 and 2.0 specifications for more information.

    Keyword Arguments:
        left_width (int): number of characters to the left hand side of the
            first period
        middle_width (int): total number of characters minus 1 between the
            first period from the left and the first colon from the left.

    Returns:
        A function which takes a header item (e.g. LASHeaderItem or Curve)
        as its single argument and which in turn returns a string which is
        the correctly formatted LAS header line.

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
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.descr)),
            item.value
        )
    elif order == "value:descr":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.value)),
            item.descr
        )


def get_section_order_function(section, version,
                               order_definitions=ORDER_DEFINITIONS):
    '''Get a function that returns the order per mnemonic and section.

    Arguments:
        section (str): either "well", "params", "curves", "version"
        version (float): either 1.2 and 2.0

    Keyword Arguments:
        order_definitions (dict): ...

    Returns:
        A function which takes a mnemonic (str) as its only argument, and 
        in turn returns the order "value:descr" or "descr:value".

    '''
    section_orders = order_definitions[version][section]
    default_order = section_orders[0]
    orders = {}
    for order, mnemonics in section_orders[1:]:
        for mnemonic in mnemonics:
            orders[mnemonic] = order
    return lambda mnemonic: orders.get(mnemonic, default_order)


def get_section_widths(section_name, items, version, order_func, middle_padding=5):
    '''Find minimum section widths fitting the content in *items*.

    Arguments:
        section_name (str): either "version", "well", "curves", or "params"
        items (SectionItems): section items
        version (float): either 1.2 or 2.0

    '''
    section_widths = {
        "left_width": None,
        "middle_width": None
    }
    if len(items) > 0:
        section_widths["left_width"] = max([len(i.original_mnemonic) for i in items])
        middle_widths = []
        for i in items:
            order = order_func(i.mnemonic)
            rhs_element = order.split(':')[0]
            logger.debug('get_section_widths %s\n\torder=%s rhs_element=%s' % (i, order, rhs_element))
            middle_widths.append(len(str(i.unit)) + 1 + len(str(i[rhs_element])))
        section_widths['middle_width'] = max(middle_widths)
    return section_widths


def read(file_ref, **kwargs):
    '''Read a LAS file.

    Note that only versions 1.2 and 2.0 of the LAS file specification
    are currently supported.

    Arguments:
        file_ref: either a filename, an open file object, or a string of
            a LAS file contents.

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): "strict", "replace" (default), "ignore" - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: 
        A LASFile object representing the file -- see above

    '''
    return LASFile(file_ref, **kwargs)
