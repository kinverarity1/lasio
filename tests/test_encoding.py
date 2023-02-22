import os

from pathlib import Path

from lasio import read, reader


def egfn(fn):
    # egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
    return os.path.join(os.path.dirname(__file__), "examples", fn)


def stegfn(vers, fn):
    # stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)
    return os.path.join(os.path.dirname(__file__), "examples", vers, fn)


def test_encoding_attr():
    las = read(egfn("encodings_utf8.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-8"


def test_utf8_chardet():
    las = read(egfn("encodings_utf8.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-8"


def test_utf8wbom_chardet():
    las = read(egfn("encodings_utf8wbom.las"), autodetect_encoding="chardet")
    # "SIG" is short for signature. This means it will use the BOM metadata
    # instead of the file contents to identify the encoding
    assert las.encoding.upper() == "UTF-8-SIG"


def test_utf16lebom_chardet():
    # BE = Big Endian. Big Endian is the default endian.
    las = read(egfn("encodings_utf16lebom.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16"


def test_utf16le_specified_ok():
    # LE = Little Endian
    las = read(egfn("encodings_utf16le.las"), encoding="UTF-16-LE")
    assert las.encoding.upper() == "UTF-16-LE"


def test_utf16le_chardet():
    # 02-15-2023: chardet is correctly identifying this file now, chardet: 5.1.0.
    las = read(egfn("encodings_utf16le.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16LE"


def test_utf16bebom_chardet():
    las = read(egfn("encodings_utf16bebom.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16"


def test_iso88591_chardet():
    las = read(egfn("encodings_iso88591.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "ISO-8859-1"


def test_cp1252_chardet():
    #  Chardet read the file as ISO-8859-1
    las = read(egfn("encodings_cp1252.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "ISO-8859-1"


"""
Verify encodings for pathlib.Path objects
"""


def test_pathlib_utf8_chardet():
    las = read(Path(egfn("encodings_utf8.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-8"


def test_pathlib_utf8wbom_chardet():
    las = read(Path(egfn("encodings_utf8wbom.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-8-SIG"


def test_pathlib_utf16lebom_chardet():
    las = read(Path(egfn("encodings_utf16lebom.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16"


def test_pathlib_utf16le_specified_ok():
    las = read(Path(egfn("encodings_utf16le.las")), encoding="UTF-16-LE")
    assert las.encoding.upper() == "UTF-16-LE"


def test_pathlib_utf16le_chardet():
    # 02-15-2023: chardet is correctly identifying this file now, chardet: 5.1.0.
    las = read(Path(egfn("encodings_utf16le.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16LE"


def test_pathlib_utf16bebom_chardet():
    las = read(Path(egfn("encodings_utf16bebom.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-16"


def test_pathlib_iso88591_chardet():
    las = read(Path(egfn("encodings_iso88591.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "ISO-8859-1"


def test_pathlib_cp1252_chardet():
    las = read(Path(egfn("encodings_cp1252.las")), autodetect_encoding="chardet")
    assert las.encoding.upper() == "ISO-8859-1"


def test_adhoc_test_encoding():
    filename = stegfn("1.2", "sample.las")
    encoding = reader.adhoc_test_encoding(filename)
    assert encoding.upper() == "ASCII"


def test_open_with_codecs_no_autodetect():
    filename = stegfn("1.2", "sample.las")
    obj, encoding = reader.open_with_codecs(filename, autodetect_encoding=False)
    assert encoding.upper() == "ASCII"


def test_open_with_codecs_no_autodetect_chars():
    filename = stegfn("1.2", "sample.las")
    obj, encoding = reader.open_with_codecs(filename, autodetect_encoding_chars=0)
    assert encoding.upper() == "ASCII"
