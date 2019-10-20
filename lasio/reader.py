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
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}"
    r"\.?|[A-Z0-9-]{2,}\.?)|"  # (cont.) domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def open_file(file_ref, **encoding_kwargs):
    """Open a file if necessary.

    If ``autodetect_encoding=True`` then either ``cchardet`` or ``chardet``
    needs to be installed, or else an ``ImportError`` will be raised.

    Arguments:
        file_ref (file-like object, str): either a filename, an open file
            object, or a string containing the contents of a file.

    See :func:`lasio.reader.open_with_codecs` for keyword arguments that can be
    used here.

    Returns:
        tuple of an open file-like object, and the encoding that
        was used to decode it (if it were read from disk).

    """
    encoding = None
    if isinstance(file_ref, str):  # file_ref != file-like object, so what is it?
        lines = file_ref.splitlines()
        first_line = lines[0]
        if URL_REGEXP.match(first_line):  # it's a URL
            logger.info("Loading URL {}".format(first_line))
            try:
                import urllib2

                response = urllib2.urlopen(first_line)
                encoding = response.headers.getparam("charset")
                file_ref = StringIO(response.read())
                logger.debug("Retrieved data had encoding {}".format(encoding))
            except ImportError:
                import urllib.request

                response = urllib.request.urlopen(file_ref)
                if response.headers.get_content_charset() is None:
                    if "encoding" in encoding_kwargs:
                        encoding = encoding_kwargs["encoding"]
                    else:
                        encoding = "utf-8"
                else:
                    encoding = response.headers.get_content_charset()
                file_ref = StringIO(response.read().decode(encoding))
                logger.debug("Retrieved data decoded via {}".format(encoding))
        elif len(lines) > 1:  # it's LAS data as a string.
            file_ref = StringIO(file_ref)
        else:  # it must be a filename
            file_ref, encoding = open_with_codecs(first_line, **encoding_kwargs)
    return file_ref, encoding


def open_with_codecs(
    filename,
    encoding=None,
    encoding_errors="replace",
    autodetect_encoding=True,
    autodetect_encoding_chars=4000,
):
    """
    Read Unicode data from file.

    Arguments:
        filename (str): path to file

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with, using
            :func:`codecs.open`.
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see
            `this section
            <https://docs.python.org/3/library/codecs.html#codec-base-classes>`__
            of the standard library's :mod:`codecs` module for more information)
        autodetect_encoding (str or bool): default True to use
            `chardet <https://github.com/chardet/chardet>`__/`cchardet
            <https://github.com/PyYoshi/cChardet>`__ to detect encoding.
            Note if set to False several common encodings will be tried but
            chardet won't be used.
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns:
        a unicode or string object

    This function is called by :func:`lasio.reader.open_file`.

    """
    if autodetect_encoding_chars:
        nbytes = int(autodetect_encoding_chars)
    else:
        nbytes = None

    # Forget [c]chardet - if we can locate the BOM we just assume that's correct.
    nbytes_test = min(32, os.path.getsize(filename))
    with open(filename, mode="rb") as test:
        raw = test.read(nbytes_test)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = "utf-8-sig"
        autodetect_encoding = False

    # If BOM wasn't found...
    if (autodetect_encoding) and (not encoding):
        with open(filename, mode="rb") as test:
            if nbytes is None:
                raw = test.read()
            else:
                raw = test.read(nbytes)
        encoding = get_encoding(autodetect_encoding, raw)
        autodetect_encoding = False

    # Or if no BOM found & chardet not installed
    if (not autodetect_encoding) and (not encoding):
        encoding = adhoc_test_encoding(filename)
        if encoding:
            logger.info(
                "{} was found by ad hoc to work but note it might not"
                " be the correct encoding".format(encoding)
            )

    # Now open and return the file-like object
    logger.info(
        'Opening {} as {} and treating errors with "{}"'.format(
            filename, encoding, encoding_errors
        )
    )
    file_obj = codecs.open(
        filename, mode="r", encoding=encoding, errors=encoding_errors
    )
    return file_obj, encoding


def adhoc_test_encoding(filename):
    test_encodings = ["ascii", "windows-1252", "latin-1"]
    for i in test_encodings:
        encoding = i
        with codecs.open(filename, mode="r", encoding=encoding) as f:
            try:
                f.readline()
                break
            except UnicodeDecodeError:
                logger.debug("{} tested, raised UnicodeDecodeError".format(i))
                pass
            encoding = None
    return encoding


def get_encoding(auto, raw):
    """
    Automatically detect character encoding.

    Arguments:
        auto (str): auto-detection of character encoding - can be either
            'chardet', 'cchardet', False, or True (the latter will pick the
            fastest available option)
        raw (bytes): array of bytes to detect from

    Returns:
        A string specifying the character encoding.

    """
    if auto is True:
        try:
            import cchardet as chardet
        except ImportError:
            try:
                import chardet
            except ImportError:
                logger.debug(
                    "chardet or cchardet is recommended for automatic"
                    " detection of character encodings. Instead trying some"
                    " common encodings."
                )
                return None
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
    logger.debug(
        "{} method detected encoding of {} at confidence {}".format(
            method, result["encoding"], result["confidence"]
        )
    )
    return result["encoding"]


def read_file_contents(file_obj, regexp_subs, value_null_subs, ignore_data=False):
    """Read file contents into memory.

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

    """
    sections = OrderedDict()
    sect_lines = []
    sect_line_nos = []
    sect_title_line = None
    section_exists = False

    for i, line in enumerate(file_obj):
        line = line.strip()
        if not line:
            continue
        if line.upper().startswith("~A"):
            # HARD CODED FOR VERSION 1.2 and 2.0; needs review for 3.0
            # We have finished looking at the metadata and need
            # to start reading numerical data.
            if not sect_title_line is None:
                sections[sect_title_line] = {
                    "section_type": "header",
                    "title": sect_title_line,
                    "lines": sect_lines,
                    "line_nos": sect_line_nos,
                }
            if not ignore_data:
                try:
                    data = read_data_section_iterative(
                        file_obj, regexp_subs, value_null_subs
                    )
                except KeyboardInterrupt:
                    raise
                except:
                    raise exceptions.LASDataError(
                        traceback.format_exc()[:-1]
                        + " in data section beginning line {}".format(i + 1)
                    )
                sections[line] = {
                    "section_type": "data",
                    "start_line": i,
                    "title": line,
                    "array": data,
                }
                logger.debug('Data section ["array"].shape = {}'.format(data.shape))
            break

        elif line.startswith("~"):
            if section_exists:
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
                section_exists = True
                pass
            sect_title_line = line  # either way... this is the case.

        else:
            # We are in the middle of a section.
            if not line.startswith("#"):  # ignore commented-out lines.. for now.
                sect_lines.append(line)
                sect_line_nos.append(i + 1)

    # Find the number of columns in the data section(s). This is only
    # useful if WRAP = NO, but we do it for all since we don't yet know
    # what the wrap setting is.

    for section in sections.values():
        if section["section_type"] == "data":
            section["ncols"] = None
            file_obj.seek(0)
            for i, line in enumerate(file_obj):
                if i == section["start_line"] + 1:
                    for pattern, sub_str in regexp_subs:
                        line = re.sub(pattern, sub_str, line)
                    section["ncols"] = len(line.split())
                    break
    return sections


def read_data_section_iterative(file_obj, regexp_subs, value_null_subs):
    """Read data section into memory.

    Arguments:
        file_obj (open file-like object): should be positioned in line-by-line
            reading mode, with the last line read being the title of the
            ~ASCII data section.
        regexp_subs (list): each item should be a tuple of the pattern and
            substitution string for a call to re.sub() on each line of the
            data section. See defaults.py READ_SUBS and NULL_SUBS for examples.
        value_null_subs (list): list of numerical values to be replaced by
            numpy.nan values.

    Returns:
        A 1-D numpy ndarray.

    """

    def items(f):
        for line in f:
            for pattern, sub_str in regexp_subs:
                line = re.sub(pattern, sub_str, line)
            for item in line.split():
                try:
                    yield np.float64(item)
                except ValueError:
                    yield item

    array = np.array([i for i in items(file_obj)])
    for value in value_null_subs:
        array[array == value] = np.nan
    return array


def get_substitutions(read_policy, null_policy):
    """Parse read and null policy definitions into a list of regexp and value
    substitutions.

    Arguments:
        read_policy (str, list, or substitution): either (1) a string defined in
            defaults.READ_POLICIES; (2) a list of substitutions as defined by
            the keys of defaults.READ_SUBS; or (3) a list of actual substitutions
            similar to the values of defaults.READ_SUBS. You can mix (2) and (3)
            together if you want.
        null_policy (str, list, or sub): as for read_policy but for
            defaults.NULL_POLICIES and defaults.NULL_SUBS

    Returns:
        regexp_subs, value_null_subs, version_NULL - two lists and a bool.
        The first list is pairs of regexp patterns and substrs, and the second
        list is just a list of floats or integers. The bool is whether or not
        'NULL' was located as a substitution.

    """
    regexp_subs = []
    numerical_subs = []
    version_NULL = False

    for policy_typ, policy, policy_subs, subs in (
        ("read", read_policy, defaults.READ_POLICIES, defaults.READ_SUBS),
        ("null", null_policy, defaults.NULL_POLICIES, defaults.NULL_SUBS),
    ):
        try:
            is_policy = policy in policy_subs
        except TypeError:
            is_policy = False
        if is_policy:
            logger.debug('using {} policy of "{}"'.format(policy_typ, policy))
            all_subs = []
            for sub in policy_subs[policy]:
                logger.debug("adding substitution {}".format(sub))
                if sub in subs:
                    all_subs += subs[sub]
                if sub == "NULL":
                    logger.debug("located substition for LAS.version.NULL as True")
                    version_NULL = True
        else:
            all_subs = []
            for item in policy:
                if item in subs:
                    all_subs += subs[item]
                    if item == "NULL":
                        logger.debug("located substition for LAS.version.NULL as True")
                        version_NULL = True
                else:
                    all_subs.append(item)
        for item in all_subs:
            try:
                iter(item)
            except TypeError:
                logger.debug("added numerical substitution: {}".format(item))
                numerical_subs.append(item)
            else:
                logger.debug(
                    'added regexp substitution: pattern={} substr="{}"'.format(
                        item[0], item[1]
                    )
                )
                regexp_subs.append(item)
    numerical_subs = [n for n in numerical_subs if not n is None]

    return regexp_subs, numerical_subs, version_NULL


def parse_header_section(
    sectdict, version, ignore_header_errors=False, mnemonic_case="preserve"
):
    """Parse a header section dict into a SectionItems containing HeaderItems.

    Arguments:
        sectdict (dict): object returned from
            :func:`lasio.reader.read_file_contents`
        version (float): either 1.2 or 2.0

    Keyword Arguments:
        ignore_header_errors (bool): if True, issue HeaderItem parse errors
            as :func:`logging.warning` calls instead of a
            :exc:`lasio.exceptions.LASHeaderError` exception.
        mnemonic_case (str): 'preserve': keep the case of HeaderItem mnemonics
                             'upper': convert all HeaderItem mnemonics to uppercase
                             'lower': convert all HeaderItem mnemonics to lowercase

    Returns:
        :class:`lasio.las_items.SectionItems`

    """
    title = sectdict["title"]
    assert len(sectdict["lines"]) == len(sectdict["line_nos"])
    parser = SectionParser(title, version=version)

    section = SectionItems()
    assert mnemonic_case in ("upper", "lower", "preserve")
    if not mnemonic_case == "preserve":
        section.mnemonic_transforms = True

    for i in range(len(sectdict["lines"])):
        line = sectdict["lines"][i]
        j = sectdict["line_nos"][i]
        if not line:
            continue
        try:
            values = read_line(line)
        except:
            message = 'line {} (section {}): "{}"'.format(
                # traceback.format_exc().splitlines()[-1].strip('\n'),
                j,
                title,
                line,
            )
            if ignore_header_errors:
                logger.warning(message)
            else:
                raise exceptions.LASHeaderError(message)
        else:
            if mnemonic_case == "upper":
                values["name"] = values["name"].upper()
            elif mnemonic_case == "lower":
                values["name"] = values["name"].lower()
            section.append(parser(**values))
    return section


class SectionParser(object):

    """Parse lines from header sections.

    Arguments:
        title (str): title line of section. Used to understand different
            order formatting across the special sections ~C, ~P, ~W, and ~V,
            depending on version 1.2 or 2.0.

    Keyword Arguments:
        version (float): version to parse according to. Default is 1.2.

    """

    def __init__(self, title, version=1.2):
        if title.upper().startswith("~C"):
            self.func = self.curves
            self.section_name2 = "Curves"
        elif title.upper().startswith("~P"):
            self.func = self.params
            self.section_name2 = "Parameter"
        elif title.upper().startswith("~W"):
            self.func = self.metadata
            self.section_name2 = "Well"
        elif title.upper().startswith("~V"):
            self.func = self.metadata
            self.section_name2 = "Version"

        self.version = version
        self.section_name = title

        defs = defaults.ORDER_DEFINITIONS
        section_orders = defs[self.version][self.section_name2]
        self.default_order = section_orders[0]  #
        self.orders = {}
        for order, mnemonics in section_orders[1:]:
            for mnemonic in mnemonics:
                self.orders[mnemonic] = order

    def __call__(self, **keys):
        """Return the correct object for this type of section.

        Refer to :meth:`lasio.reader.SectionParser.metadata`,
        :meth:`lasio.reader.SectionParser.params`, and
        :meth:`lasio.reader.SectionParser.curves` for the methods actually
        used by this routine.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        item = self.func(**keys)
        return item

    def num(self, x, default=None):
        """Attempt to parse a number.

        Arguments:
            x (str, int, float): potential number
            default (int, float, None): fall-back option

        Returns:
            int, float, or **default** - from most to least preferred types.

        """
        if default is None:
            default = x

        # in case it is a string.
        try:
            pattern, sub = defaults.READ_SUBS["comma-decimal-mark"][0]
            x = re.sub(pattern, sub, x)
        except:
            pass

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

    def strip_brackets(self, x):
        x = x.strip()
        if len(x) >= 2:
            if (x[0] == "[" and x[-1] == "]") or (x[0] == "(" and x[-1] == ")"):
                return x[1:-1]
        return x

    def metadata(self, **keys):
        """Return HeaderItem correctly formatted according to the order
        prescribed for LAS v 1.2 or 2.0 for the ~W section.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        # number_strings: fields that shouldn't be converted to numbers
        number_strings = ['API', 'UWI']

        key_order = self.orders.get(keys["name"], self.default_order)

        value = ''
        descr = ''

        if key_order == "value:descr":
            value = keys["value"]
            descr = keys["descr"]
        elif key_order == "descr:value":
            value = keys["descr"]
            descr = keys["value"]

        if keys["name"].upper() not in number_strings:
            value = self.num(value)

        item = HeaderItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            value,  # value
            descr,  # descr
        )
        return item


    def curves(self, **keys):
        """Return CurveItem.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        item = CurveItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            keys["value"],  # value
            keys["descr"],  # descr
        )
        return item

    def params(self, **keys):
        """Return HeaderItem for ~P section (the same between 1.2 and 2.0 specs)

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        return HeaderItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            self.num(keys["value"]),  # value
            keys["descr"],  # descr
        )


def read_line(*args, **kwargs):
    """Retained for backwards-compatibility.

    See :func:`lasio.reader.read_header_line`.

    """
    return read_header_line(*args, **kwargs)


def read_header_line(line, pattern=None):
    """Read a line from a LAS header section.

    The line is parsed with a regular expression -- see LAS file specs for
    more details, but it should basically be in the format::

        name.unit       value : descr

    Arguments:
        line (str): line from a LAS header section

    Returns:
        A dictionary with keys 'name', 'unit', 'value', and 'descr', each
        containing a string as value.

    """
    d = {"name": "", "unit": "", "value": "", "descr": ""}
    if pattern is None:
        if not ":" in line:
            pattern = (
                r"\.?(?P<name>[^.]*)\." + r"(?P<unit>[^\s:]*)" + r"(?P<value>[^:]*)"
            )
        else:
            pattern = (
                r"\.?(?P<name>[^.]*)\."
                + r"(?P<unit>[^\s:]*)"
                + r"(?P<value>[^:]*):"
                + r"(?P<descr>.*)"
            )
    m = re.match(pattern, line)
    if m is None:
        logger.warning("Unable to parse line as LAS header: {}".format(line))
    mdict = m.groupdict()
    for key, value in mdict.items():
        d[key] = value.strip()
        if key == "unit":
            if d[key].endswith("."):
                d[key] = d[key].strip(".")  # see issue #36
    return d
