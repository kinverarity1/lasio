
# Standard library packages
import codecs
import json
import logging
import os
import re
import textwrap
import traceback

import numpy as np

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


def open_file(file_ref, encoding=None, encoding_errors='replace'):
    '''Open a file if necessary.

    If autodetect_encoding is True then either cchardet or chardet (see PyPi)
    needs to be installed, or else an ImportError will be raised.

    Arguments:
        file_ref: either a filename, an open file object, or a URI.

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: 
        An open file-like object ready for reading from.

    '''
    if isinstance(file_ref, str): # file_ref != file-like object, so what is it?
        file_ref = file_ref.splitlines()[0]
        if URL_REGEXP.match(file_ref): # file_ref == URI
            try:
                import urllib2
                file_ref = urllib2.urlopen(file_ref)
            except ImportError:
                import urllib.request
                response = urllib.request.urlopen(file_ref)
                enc = response.headers.get_content_charset('utf-8')
                file_ref = StringIO(response.read().decode(enc))
        else:  # file_ref == filename
            file_ref = codecs.open(file_ref, 'r', encoding, encoding_errors)
    # else: file_ref is already a file-like object.
    return file_ref


def read(file_ref, null_subs, **kwargs):
    sections = OrderedDict()
    sect_lines = []
    sect_title_line = None
    file_ref = open_file(file_ref, **kwargs)
    for line in file_ref:
        line = line.strip()
        if line.startswith('~A'):
            # We have finished looking at the metadata and need
            # to start reading numerical data.
            sections[sect_title_line] = StringIO('\n'.join(sect_lines))
            sections[line] = read_numerical_data(file_ref, null_subs)
        elif line.startswith('~'):
            if sect_lines:
                # We have ended a section and need to start the next
                sections[sect_title_line] = StringIO('\n'.join(sect_lines))
                sect_lines = []
            else:
                # We are entering into a section for the first time
                pass
            sect_title_line = line # either way... this is the case.
        else:
            # We are in the middle of a section.
            sect_lines.append(line)
    return sections


def read_numerical_data(file_ref, null_subs):

    def items(f):
        for line in f:
            for item in line.split():
                yield item
    
    return np.fromiter(items(file_ref), np.float64, -1)
    # data = data.reshape((-1, num_cols))


class Reader(object):

    def __init__(self, text, version):
        self.lines = text.splitlines()
        self.version = version
        self.null = np.nan
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
                raise exceptions.LASHeaderError(
                    'Failed in %s section on line:\n%s%s' % (
                        section_name, line,
                        traceback.format_exc().splitlines()[-1]))
            else:
                section.append(parser(**values))
        return section

    def read_data(self, number_of_curves=None, null_subs=True):
        s = self.read_data_string()
        if not self.wrap:
            try:
                arr = np.loadtxt(StringIO(s))
            except:
                raise exceptions.LASDataError('Failed to read data:\n%s' % (
                    traceback.format_exc().splitlines()[-1]))
        else:
            eol_chars = r'[\n\t\r]'
            s = re.sub(eol_chars, ' ', s)
            try:
                arr = np.loadtxt(StringIO(s))
            except:
                raise exceptions.LASDataError(
                    'Failed to read wrapped data: %s' % (
                        traceback.format_exc().splitlines()[-1]))
            logger.debug('Reader.read_data arr shape = %s' % (arr.shape))
            logger.debug('Reader.read_data number of curves = %s' %
                         number_of_curves)
            arr = np.reshape(arr, (-1, number_of_curves))
        if not arr.shape or (arr.ndim == 1 and arr.shape[0] == 0):
            logger.warning('Reader.read_dataN o data present.')
            return None, None
        else:
            logger.info('Reader.read_data LAS file shape = %s' %
                        str(arr.shape))
        logger.debug(
            'Reader.read_data checking for nulls (NULL = %s)' % self.null)
        if null_subs:
            arr[arr == self.null] = np.nan
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
        self.section_name2 = {'~C': 'Curves',
                              '~W': 'Well',
                              '~V': 'Version',
                              '~P': 'Parameter'}[section_name]

        section_orders = defaults.ORDER_DEFINITIONS[
            self.version][self.section_name2]
        self.default_order = section_orders[0]
        self.orders = {}
        for order, mnemonics in section_orders[1:]:
            for mnemonic in mnemonics:
                self.orders[mnemonic] = order

    def __call__(self, **keys):
        item = self.func(**keys)
        # if item.name == '':
        #     item.mnemonic = 'UNKNOWN'
        return item

    def num(self, x, default=None):
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
        # logger.debug(str(keys))
        item = CurveItem(
            keys['name'],               # mnemonic
            keys['unit'],               # unit
            keys['value'],              # value
            keys['descr'],              # descr
        )
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
    # if mdict['name'] == '':
    #     mdict['name'] = 'UNKNOWN'
    for key, value in mdict.items():
        d[key] = value.strip()
        if key == 'unit':
            if d[key].endswith('.'):
                d[key] = d[key].strip('.')  # see issue #36
    return d


def get_encoding(auto, raw):
    '''
    Automatically detect character encoding.

    Arguments:
        auto (str): auto-detection of character encoding - can be either
            'chardet', 'cchardet', or True
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
