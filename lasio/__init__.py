from .las import LASFile, JSONEncoder
from .las_items import CurveItem, HeaderItem, SectionItems
from .reader import open_file

try:
    import openpyxl
except ImportError:
    pass
else:
    from .excel import ExcelConverter

__version__ = '0.12'


def read(file_ref, **kwargs):
    '''Read a LAS file.

    Note that only versions 1.2 and 2.0 of the LAS file specification
    are currently supported.

    Arguments:
        file_ref: either a filename, an open file object, or a string of
            a LAS file contents.

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see standard library codecs module or
            Python Unicode HOWTO for more information)
        autodetect_encoding (bool): use chardet/ccharet to detect encoding
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: 
        A LASFile object representing the file -- see above

    '''
    return LASFile(file_ref, **kwargs)
