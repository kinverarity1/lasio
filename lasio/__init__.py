"""Lasio package for reading and writing Log Ascii Standard well files."""

import logging
import os

def add_logging_level(levelName, levelNum, methodName=None):
    """Add a new logging level to current logger.

    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example

    >>> add_logging_level('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

add_logging_level("TRACE_LASIO", logging.DEBUG - 5, "trace_lasio")

from .las_version import version
from .las import LASFile, JSONEncoder
from .las_items import CurveItem, HeaderItem, SectionItems
from .reader import open_file

__version__ = version()


def read(file_ref, **kwargs):
    """Read a LAS file.

    Note that only versions 1.2 and 2.0 of the LAS file specification
    are fully supported. There is partial support for reading LAS 3.0 files.

    Arguments:
        file_ref( :term:`file-like object` or :class:`str`): either a filename,
            an open file object, or a string containing the contents of a file.

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
        read_policy (str or list): Apply regular expression substitutions for common errors in
                fixed-width formatted data sections. If you do not want any such substitutions
                to applied, pass ``read_policy=()``.
        null_policy (str or list): see
            https://lasio.readthedocs.io/en/latest/data-section.html#handling-invalid-data-indicators-automatically
        accept_regexp_sub_recommendations (bool): Accept recommendations to auto-
            matically remove read substitutions (applied by the default read_policy)
            which look for numeric run-on errors involving hyphens. This avoids
            incorrect parsing of dates such as '2018-05-22' as three separate columns
            containing '2018', '-5' and '-22'. The read substitutions are applied only
            if the inspection code of the data section finds a hyphen in every line.
            The only circumstance where this should be manually set to False is where
            you have very problematic fixed-column-width data sections involving negative
            values.
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
        autodetect_encoding (str or bool): default True to use `chardet
            <https://github.com/chardet/chardet>`__ to detect encoding.
            Note if set to False several common encodings will be tried but
            chardet won't be used.
            (this is handled by :func:`lasio.reader.open_with_codecs`)
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.
            (this is handled by :func:`lasio.reader.open_with_codecs`)


    Returns:
        a :class:`lasio.LASFile` object representing the file

    The documented arguments above are combined from these methods:

    * :func:`lasio.reader.open_with_codecs` - manage issues relate to character
      encodings
    * :meth:`lasio.LASFile.read` - control how NULL values and errors are
      handled during parsing

    """
    return LASFile(file_ref, **kwargs)
