import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging

import codecs

import pytest

from pathlib import Path

from lasio import read, reader

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)


def test_encoding_attr():
    las = read(egfn("encodings_utf8.las"), autodetect_encoding="chardet")
    assert las.encoding.upper() == "UTF-8"


def test_utf8_chardet():
    las = read(egfn("encodings_utf8.las"), autodetect_encoding="chardet")


def test_utf8wbom_chardet():
    las = read(egfn("encodings_utf8wbom.las"), autodetect_encoding="chardet")


def test_utf16lebom_chardet():
    las = read(egfn("encodings_utf16lebom.las"), autodetect_encoding="chardet")


def test_utf16le_specified_ok():
    las = read(egfn("encodings_utf16le.las"), encoding="UTF-16-LE")


@pytest.mark.skip(reason="this is not behaving properly see PR #326")
def test_utf16le_chardet_fails():
    with pytest.raises(Exception):
        las = read(egfn("encodings_utf16le.las"), autodetect_encoding="chardet")


def test_utf16bebom_chardet():
    las = read(egfn("encodings_utf16bebom.las"), autodetect_encoding="chardet")


def test_iso88591_chardet():
    las = read(egfn("encodings_iso88591.las"), autodetect_encoding="chardet")


def test_cp1252_chardet():
    las = read(egfn("encodings_cp1252.las"), autodetect_encoding="chardet")


"""
Verify encodings for pathlib.Path objects
"""


def test_pathlib_utf8_chardet():
    las = read(Path(egfn("encodings_utf8.las")), autodetect_encoding="chardet")


def test_pathlib_utf8wbom_chardet():
    las = read(Path(egfn("encodings_utf8wbom.las")), autodetect_encoding="chardet")


def test_pathlib_utf16lebom_chardet():
    las = read(Path(egfn("encodings_utf16lebom.las")), autodetect_encoding="chardet")


def test_pathlib_utf16le_specified_ok():
    las = read(Path(egfn("encodings_utf16le.las")), encoding="UTF-16-LE")


@pytest.mark.skip(reason="this is not behaving properly see PR #326")
def test_pathlib_utf16le_chardet_fails():
    with pytest.raises(Exception):
        las = read(Path(egfn("encodings_utf16le.las")), autodetect_encoding="chardet")


def test_pathlib_utf16bebom_chardet():
    las = read(Path(egfn("encodings_utf16bebom.las")), autodetect_encoding="chardet")


def test_pathlib_iso88591_chardet():
    las = read(Path(egfn("encodings_iso88591.las")), autodetect_encoding="chardet")


def test_pathlib_cp1252_chardet():
    las = read(Path(egfn("encodings_cp1252.las")), autodetect_encoding="chardet")


def test_adhoc_test_encoding():
    filename = stegfn("1.2", "sample.las")
    res = reader.adhoc_test_encoding(filename)
    assert res == "ascii"


def test_open_with_codecs_no_autodetect():
    filename = stegfn("1.2", "sample.las")
    obj, encoding = reader.open_with_codecs(filename, autodetect_encoding=False)
    assert encoding == "ascii"


def test_open_with_codecs_no_autodetect_chars():
    filename = stegfn("1.2", "sample.las")
    obj, encoding = reader.open_with_codecs(filename, autodetect_encoding_chars=0)
    assert encoding.upper() == "ASCII"
