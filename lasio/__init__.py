import logging
import os

def add_logging_level(levelName, levelNum, methodName=None):
    """
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
    -------
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
    are currently supported.

    Arguments:
        file_ref (file-like object, str): either a filename, an open file
            object, or a string containing the contents of a file.

    Returns:
        a :class:`lasio.LASFile` object representing the file -- see above

    There are a number of optional keyword arguments that can be passed to this
    function that control how the LAS file is opened and parsed. Any of the
    keyword arguments from the below functions can be used here:

    * :func:`lasio.reader.open_with_codecs` - manage issues relate to character
      encodings
    * :meth:`lasio.las.LASFile.read` - control how NULL values and errors are
      handled during parsing

    """
    return LASFile(file_ref, **kwargs)
