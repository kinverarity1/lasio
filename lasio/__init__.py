import subprocess
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "A Dev version: probably in a git repo."
    tmpbytes = subprocess.check_output(
        ["git", "log", "-1", "--pretty=tformat:Commit %h"]
    ).strip()

    tmpstr = "".join( chr(x) for x in tmpbytes)
    if tmpstr.startswith("Commit"):
       __version__ = "Dev version: {}".format(tmpstr)
    pass

import os

from .las import LASFile, JSONEncoder
from .las_items import CurveItem, HeaderItem, SectionItems
from .reader import open_file

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
