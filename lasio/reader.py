import codecs
import logging
import os
import re
import textwrap
import traceback

import numpy as np

from . import defaults

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

from . import defaults
from . import exceptions
from .las_items import HeaderItem, CurveItem, SectionItems, OrderedDict


logger = logging.getLogger(__name__)

URL_REGEXP = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}'
    r'\.?|[A-Z0-9-]{2,}\.?)|'  # (cont.) domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def open_file(file_ref, encoding=None, encoding_errors='replace',
              autodetect_encoding=False, autodetect_encoding_chars=40e3):
    '''Open a file if necessary.

    If ``autodetect_encoding=True`` then either ``cchardet`` or ``chardet``
    needs to be installed, or else an ``ImportError`` will be raised.

    Arguments:
        file_ref (file-like object, str): either a filename, an open file 
            object, or a string containing the contents of a file.

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see :py:mod:`codecs` module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (str, bool): auto-detection of character encoding - can
            be either 'chardet', 'cchardet', or True
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: 
        An open file-like object ready for reading from.

    '''
    if isinstance(file_ref, str): # file_ref != file-like object, so what is it?
        lines = file_ref.splitlines()
        first_line = lines[0]
        if URL_REGEXP.match(first_line): # it's a URL
            try:
                import urllib2
                url_ref = urllib2.urlopen(first_line)
                file_ref = StringIO(url_ref.read())
            except ImportError:
                import urllib.request
                response = urllib.request.urlopen(file_ref)
                enc = response.headers.get_content_charset('utf-8')
                file_ref = StringIO(response.read().decode(enc))
        elif len(lines) > 1: # it's LAS data as a string.
            file_ref = StringIO(file_ref)
        else:  # it must be a filename
            file_ref = open_with_codecs(first_line, encoding, encoding_errors, 
                                        autodetect_encoding, 
                                        autodetect_encoding_chars)
        
    # If file_ref was:
    #  - a file-like object, nothing happens and it is returned
    #    directly by this function.
    #  - a filename, the encoding is detected and the file opened and returned
    #  - a URI, a request is made and the content read and returned as a 
    #    file-like object using cStringIO
    #  - a string, the string is returned as a file-like object using StringIO

    return file_ref


def open_with_codecs(filename, encoding, encoding_errors, 
                     autodetect_encoding, nbytes):
    '''
    Read Unicode data from file.

    Arguments:
        filename (str): path to file
        encoding (str): encoding for :py:func:`codecs.open` - can be ``None``
        encoding_errors (str): unicode error handling - can be 'strict', 
            'ignore', 'replace'
        autodetect_encoding (str): auto-detection of character encoding - can
            be either 'chardet', 'cchardet', or True
        nbytes (int): number of characters for read for auto-detection

    Returns:
        a unicode or string object

    See :func:`lasio.reader.open_file` for more explanation, as most users will
    be using that function, not this one.

    '''
    if nbytes:
        nbytes = int(nbytes)

    # Forget chardet - if we can locate the BOM we just assume that's correct.
    nbytes_test = min(32, os.path.getsize(filename))
    with open(filename, mode='rb') as test:
        raw = test.read(nbytes_test)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
        autodetect_encoding = False

    # Otherwise...
    if autodetect_encoding:
        with open(filename, mode='rb') as test:
            if nbytes is None:
                raw = test.read()
            else:
                raw = test.read(nbytes)
        encoding = get_encoding(autodetect_encoding, raw)

    # Now open and return the file-like object
    return codecs.open(filename, mode='r', encoding=encoding, 
                       errors=encoding_errors)


def get_encoding(auto, raw):
    '''
    Automatically detect character encoding.

    Arguments:
        auto (str): auto-detection of character encoding - can be either
            'chardet', 'cchardet', or True (the latter will pick the fastest
            available option)
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
                    'chardet or cchardet is required for automatic'
                    ' detection of character encodings.')
            else:
                logger.debug('get_encoding Using chardet')
                method = 'chardet'
        else:
            logger.debug('get_encoding Using cchardet')
            method = 'cchardet'
    elif auto.lower() == 'chardet':
        import chardet
        logger.debug('get_encoding Using chardet')
        method = 'chardet'
    elif auto.lower() == 'cchardet':
        import cchardet as chardet
        logger.debug('get_encoding Using cchardet')
        method = 'cchardet'

    result = chardet.detect(raw)
    logger.debug('get_encoding %s results=%s' % (method, result))
    return result['encoding']


def read_file_contents(file_obj, ignore_data=False):
    '''Read file contents into memory.

    Arguments:
        file_obj (open file-like object)

    Keyword Arguments:
        null_subs (bool): True will substitute ``numpy.nan`` for invalid values
        ignore_data (bool): if True, do not read in the numerical data in the
            ~ASCII section

    Returns:
        OrderedDict

    I think of the returned dictionary as a "raw section". The keys are
    the first line of the LAS section, including the tilde. Each value is
    a dict with either::

        {"section_type": "header",
         "title": str,               # title of section (including the ~)
         "lines": [str, ],           # a list of the lines from the lAS file
         "line_nos": [int, ]         # line nos from the original file
         }
        
    or::

        {"section_type": "data",
         "title": str,              # title of section (including the ~)
         "start_line": int,         # location of data section (the title line)
         "ncols": int,              # no. of columns on first line of data,
         "array": ndarray           # 1-D numpy.ndarray,
         }

    '''
    sections = OrderedDict()
    sect_lines = []
    sect_line_nos = []
    sect_title_line = None
    
    for i, line in enumerate(file_obj):
        line = line.strip()
        if line.startswith('~A'):
            # HARD CODED FOR VERSION 1.2 and 2.0; needs review for 3.0
            # We have finished looking at the metadata and need
            # to start reading numerical data.
            sections[sect_title_line] = {
                "section_type": "header",
                "title": sect_title_line,
                "lines": sect_lines,
                "line_nos": sect_line_nos,
                }
            if not ignore_data:
                data = read_numerical_file_contents(file_obj, i + 1)
                sections[line] = {
                    "section_type": "data",
                    "start_line": i,
                    # "ncols": ncols,
                    "title": line,
                    "array": data,
                    }
            break

        elif line.startswith('~'):
            if sect_lines:
                # We have ended a section and need to start the next
                sections[sect_title_line] = {
                    "section_type": "header",
                    "title": sect_title_line,
                    "lines": sect_lines,
                    "line_nos": sect_line_nos,
                    }
                sect_lines = []
                sect_line_nos = []
            else:
                # We are entering into a section for the first time
                pass
            sect_title_line = line # either way... this is the case.

        else:
            # We are in the middle of a section.
            if not line.startswith("#"): # ignore commented-out lines.. for now.
                sect_lines.append(line)
                sect_line_nos.append(i + 1)

    # Find the number of columns in the data section(s). This is only 
    # useful if WRAP = NO, but we do it for all since we don't yet know
    # what the wrap setting is.

    for section in sections.values():
        if section["section_type"] == "data":
            file_obj.seek(0)
            for i, line in enumerate(file_obj):
                if i == section["start_line"] + 1:
                    for pattern, sub_str in defaults.SUB_PATTERNS:
                        line = re.sub(pattern, sub_str, line)
                    section["ncols"] = len(line.split())
                    break
    return sections


def read_numerical_file_contents(file_obj, i):
    '''Read data section into memory.

    Arguments:
        file_obj (open file-like object): should be positioned in line-by-line
            reading mode, with the last line read being the title of the
            ~ASCII data section.

    Returns: 
        A 1-D numpy ndarray.

    '''
    def items(f):
        for line in f:
            for pattern, sub_str in defaults.SUB_PATTERNS:
                line = re.sub(pattern, sub_str, line)
            for item in line.split():
                yield item

    return np.fromiter(items(file_obj), np.float64, -1)


def parse_header_section(sectdict, version, ignore_header_errors=False):
    '''Parse a header section dict into a SectionItems containing HeaderItems.

    Arguments:
        sectdict (dict): object returned from 
            :func:`lasio.reader.read_file_contents`
        version (float): either 1.2 or 2.0

    Keyword Arguments:
        ignore_header_errors (bool): if True, issue HeaderItem parse errors
            as :func:`logging.warning` calls instead of a
            :exc:`lasio.exceptions.LASHeaderError` exception.

    Returns:
        :class:`lasio.las_items.SectionItems`

    '''
    title = sectdict["title"]
    assert len(sectdict["lines"]) == len(sectdict["line_nos"])
    parser = SectionParser(title, version=version)
    section = SectionItems()
    for i in range(len(sectdict["lines"])):
        line = sectdict["lines"][i]
        j = sectdict["line_nos"][i]
        # if line.start
        try:
            values = read_line(line)
        except:
            message = "Line #%d - failed in %s section on line:\n%s%s" % (
                j, title, line,
                traceback.format_exc().splitlines()[-1])
            
            if ignore_header_errors:
                logger.warning(message)
            else:
                raise exceptions.LASHeaderError(message)
        else:
            section.append(parser(**values))
    return section



class SectionParser(object):

    '''Parse lines from header sections.

    Arguments:
        title (str): title line of section. Used to understand different
            order formatting across the special sections ~C, ~P, ~W, and ~V,
            depending on version 1.2 or 2.0.

    Keyword Arguments:
        version (float): version to parse according to. Default is 1.2.

    '''

    def __init__(self, title, version=1.2):
        if title.upper().startswith('~C'):
            self.func = self.curves
            self.section_name2 = "Curves"
        elif title.upper().startswith('~P'):
            self.func = self.params
            self.section_name2 = "Parameter"
        elif title.upper().startswith('~W'):
            self.func = self.metadata
            self.section_name2 = "Well"
        elif title.upper().startswith('~V'):
            self.func = self.metadata
            self.section_name2 = "Version"
            

        self.version = version
        self.section_name = title

        defs = defaults.ORDER_DEFINITIONS
        section_orders = defs[self.version][self.section_name2]
        self.default_order = section_orders[0]#
        self.orders = {}
        for order, mnemonics in section_orders[1:]:
            for mnemonic in mnemonics:
                self.orders[mnemonic] = order

    def __call__(self, **keys):
        '''Return the correct object for this type of section.

        Refer to :meth:`lasio.reader.SectionParser.metadata`,
        :meth:`lasio.reader.SectionParser.params`, and
        :meth:`lasio.reader.SectionParser.curves` for the methods actually
        used by this routine.

        Keyword arguments should be the key:value pairs returned by 
        :func:`lasio.reader.read_header_line`.

        '''
        item = self.func(**keys)
        return item

    def num(self, x, default=None):
        '''Attempt to parse a number.

        Arguments:
            x (str, int, float): potential number
            default (int, float, None): fall-back option

        Returns:
            int, float, or **default** - from most to least preferred types.

        '''
        if default is None:
            default = x
        try:
            return np.int(x)
        except:
            try:
                x = np.float(x)
            except:
                return default
        if np.isfinite(x):
            return x
        else:
            return default

    def metadata(self, **keys):
        '''Return HeaderItem correctly formatted according to the order
        prescribed for LAS v 1.2 or 2.0 for the ~W section.

        Keyword arguments should be the key:value pairs returned by 
        :func:`lasio.reader.read_header_line`.

        '''
        key_order = self.orders.get(keys['name'], self.default_order)
        if key_order == 'value:descr':
            return HeaderItem(
                keys['name'],                 # mnemonic
                keys['unit'],                 # unit
                self.num(keys['value']),      # value
                keys['descr'],                # descr
            )
        elif key_order == 'descr:value':
            return HeaderItem(
                keys['name'],                   # mnemonic
                keys['unit'],                   # unit
                keys['descr'],                  # descr
                self.num(keys['value']),        # value
            )

    def curves(self, **keys):
        '''Return CurveItem.

        Keyword arguments should be the key:value pairs returned by 
        :func:`lasio.reader.read_header_line`.

        '''
        item = CurveItem(
            keys['name'],               # mnemonic
            keys['unit'],               # unit
            keys['value'],              # value
            keys['descr'],              # descr
        )
        return item

    def params(self, **keys):
        '''Return HeaderItem for ~P section (the same between 1.2 and 2.0 specs)

        Keyword arguments should be the key:value pairs returned by 
        :func:`lasio.reader.read_header_line`.

        '''
        return HeaderItem(
            keys['name'],               # mnemonic
            keys['unit'],               # unit
            self.num(keys['value']),    # value
            keys['descr'],              # descr
        )


def read_line(*args, **kwargs):
    '''Retained for backwards-compatibility.

    See :func:`lasio.reader.read_header_line`.

    '''
    return read_header_line(*args, **kwargs)


def read_header_line(line, pattern=None):
    '''Read a line from a LAS header section.

    The line is parsed with a regular expression -- see LAS file specs for
    more details, but it should basically be in the format::

        name.unit       value : descr

    Arguments:
        line (str): line from a LAS header section

    Returns:
        A dictionary with keys 'name', 'unit', 'value', and 'descr', each
        containing a string as value.

    '''
    d = {}
    if pattern is None:
        pattern = (r'\.?(?P<name>[^.]*)\.' +
                   r'(?P<unit>[^\s:]*)' +
                   r'(?P<value>[^:]*):' +
                   r'(?P<descr>.*)')
    m = re.match(pattern, line)
    mdict = m.groupdict()
    for key, value in mdict.items():
        d[key] = value.strip()
        if key == 'unit':
            if d[key].endswith('.'):
                d[key] = d[key].strip('.')  # see issue #36
    return d

