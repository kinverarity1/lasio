from . import las

from las import __version__, LASFile, Curve, HeaderItem


def read(file_ref, encoding=None,
         autodetect_encoding=False, autodetect_encoding_chars=20000):
    '''Read a LAS file.

        Args:
          file_ref: either a filename, an open file object, or a string of
            a LAS file contents.

        Kwargs:
          encoding (str): character encoding to open file_ref with
          autodetect_encoding (bool): use chardet/ccharet to detect encoding
          autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns: a las.LASFile object

    Note that it only supports versions 1.2 and 2.0 of the LAS file
    specification.

    '''
    return las.LASFile(file_ref, encoding=encoding,
                       autodetect_encoding=autodetect_encoding,
                       autodetect_encoding_chars=autodetect_encoding_chars)
