
import os

from .las_version import version
from .las import LASFile, JSONEncoder
from .las_items import CurveItem, HeaderItem, SectionItems
from .reader import open_file

__version__ = version()

try:
    import openpyxl
except ImportError:
    pass
else:
    from .excel import ExcelConverter





def read(file_ref, **kwargs):
    '''Read a LAS file.

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

    '''
    return LASFile(file_ref, **kwargs)
