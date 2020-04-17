import subprocess, re
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # default version
    __version__ = "0.0.0.unknown.version"

    semver_regex = re.compile('^\d+\.\d+\.\d+')

    # python setup.py --version
    tmpstr = subprocess.check_output(
        ["python", "setup.py", "--version"],
        encoding='utf-8'
    ).strip()

    if semver_regex.match(tmpstr):
       __version__ = tmpstr
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
