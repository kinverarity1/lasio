import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging

import codecs

import pytest

from lasio import read

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)

def test_encoding_attr():
    las = read(egfn("encodings_utf8.las"), autodetect_encoding='cchardet')
    assert las.encoding == 'UTF-8'

def test_utf8_cchardet(): las = read(egfn("encodings_utf8.las"), autodetect_encoding='cchardet')
def test_utf8wbom_cchardet(): las = read(egfn("encodings_utf8wbom.las"), autodetect_encoding='cchardet')
def test_utf16lebom_cchardet(): las = read(egfn("encodings_utf16lebom.las"), autodetect_encoding='cchardet')
def test_utf16le_specified_ok(): las = read(egfn("encodings_utf16le.las"), encoding='UTF-16-LE')
def test_utf16le_cchardet_fails(): 
    with pytest.raises(Exception):
        las = read(egfn("encodings_utf16le.las"), autodetect_encoding='cchardet')
def test_utf16bebom_cchardet(): las = read(egfn("encodings_utf16bebom.las"), autodetect_encoding='cchardet')
def test_iso88591_cchardet(): las = read(egfn("encodings_iso88591.las"), autodetect_encoding='cchardet')
def test_cp1252_cchardet(): las = read(egfn("encodings_cp1252.las"), autodetect_encoding='cchardet')

