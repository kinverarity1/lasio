import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import codecs

import pytest

from lasio import read

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)

# def test_utf8_default():
#     fn = egfn("sample_extended_chars_utf8.las")
#     with pytest.raises(Exception):
#         l = read(fn, encoding_errors="strict")

# def test_utf16le_default():
#     fn = egfn("sample_extended_chars_utf16le.las")
#     l = read(fn, encoding="utf8", encoding_errors="strict")

# def test_utf8_autodetect_encoding():
#     fn = egfn("sample_extended_chars_utf8.las")
#     l = read(fn, autodetect_encoding=True, encoding_errors="strict")

# def test_autodetect_cp437():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_cp437.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="cp437").read()

# def test_autodetect_utf8():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_utf8.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="utf8").read()

# def test_autodetect_win1252():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_win1252.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="win1252").read()
