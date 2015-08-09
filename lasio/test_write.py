import os

import pytest

from . import read
from .las import StringIO

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)

def test_write_sect_widths_12():
    l = read(egfn("sample_write_sect_widths_12.las"))
    s = StringIO()
    l.write(s, version=1.2)
    s.seek(0)
    print s.read()

def test_write_sect_widths_12_curves():
    l = read(egfn("sample_write_sect_widths_12.las"))
    s = StringIO()
    l.write(s, version=1.2)
    for start in ("D.M ", "A.US/M ", "B.K/M3 ", "C.V/V "):
        s.seek(0)
        assert "\n" + start in s.read()

def test_write_sect_widths_20_narrow():
    l = read(egfn("sample_write_sect_widths_20_narrow.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    print s.read()

def test_write_sect_widths_20_wide():
    l = read(egfn("sample_write_sect_widths_20_wide.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    print s.read()

# def test_write_sect_widths_12_curves():
#     l = read(egfn("sample_write_sect_widths_12.las"))
#     s = StringIO()
#     l.write(s, version=1.2)
#     s.seek(0)
#     assert """D.M                      : 1  DEPTH
# A.US/M                   : 2  SONIC TRANSIT TIME
# B.K/M3                   : 3  BULK DENSITY
# C.V/V                    : 4   NEUTRON POROSITY
# Z.OHMM                   : 5  RXO RESISTIVITY
# E.OHMM                   : 6  SHALLOW RESISTIVITY
# F.OHMM                   : 7  MEDIUM RESISTIVITY
# G.OHMM                   : 8  DEEP RESISTIVITY
# """ in s.read()
