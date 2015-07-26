from . import las


def read(file_ref, encoding=None,
         autodetect_encoding=False, autodetect_encoding_chars=20000):
    return las.LASFile(file_ref, encoding=encoding,
                       autodetect_encoding=autodetect_encoding,
                       autodetect_encoding_chars=autodetect_encoding_chars)
