import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch
from pprint import pformat

import numpy
import pytest
import math

import lasio
import lasio.las_items
from lasio import las, read, exceptions


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)


def test_autodepthindex():
    m = read(egfn("autodepthindex_M.las"))
    f = read(egfn("autodepthindex_F.las"))
    ft = read(egfn("autodepthindex_FT.las"))
    err = read(egfn("autodepthindex_M_FT.las"))


def test_autodepthindex_inconsistent():
    err = read(egfn("autodepthindex_M_FT.las"))
    with pytest.raises(exceptions.LASUnknownUnitError):
        print(err.depth_m)


def test_autodepthindex_m():
    l = read(egfn("autodepthindex_M.las"))
    assert (l.depth_ft[-1] * 0.3048 == l.index[-1])


def test_autodepthindex_f():
    l = read(egfn("autodepthindex_F.las"))
    assert (l.depth_m[-1] / 0.3048 == l.index[-1])


def test_autodepthindex_ft():
    l = read(egfn("autodepthindex_FT.las"))
    assert (l.depth_m[-1] / 0.3048 == l.index[-1])

def test_autodepthindex_feet():
    l = read(egfn("autodepthindex_FEET.las"))
    assert (l.depth_m[-1] / 0.3048 == l.index[-1])

def test_df_indexing():
    l = read(egfn("6038187_v1.2.las"))
    metres = 9.05
    spacing = l.well["STEP"].value
    calc_index = math.floor((metres / spacing) - (l.well["STRT"].value / spacing))
    calc_index = int(calc_index)
    assert l["GAMN"][calc_index] == l.df()["GAMN"][metres]


# TODO: make above test in reverse-ordered LAS (e.g. STRT > STOP)

def test_df_reverse():
    l = read(egfn("sample_rev.las"))
    metres = 1667
    spacing = l.well["STEP"].value
    calc_index = math.floor((metres // spacing) - (l.well["STRT"].value // spacing))
    calc_index = int(calc_index)
    assert l["DT"][calc_index] == l.df()["DT"][metres]

def test_df_curve_names():
    l = read(egfn("sample_rev.las"))
    assert l.keys()[1:] == list(l.df().columns.values)

def test_non_standard_section():
    l = read(egfn("non-standard-header-section.las"))
    assert "SPECIAL INFORMATION" in l.sections.keys()

def test_non_standard_sections():
    l = read(egfn("non-standard-header-sections.las"))
    assert "SPECIAL INFORMATION" in l.sections.keys()
    assert "extra special information" in l.sections.keys()

def test_repr():
    h = lasio.las_items.HeaderItem('MN', unit='m', value=20, descr='test testing')
    assert h.__repr__() == pformat(h)

def test_mnemonic_case_preserved():
    las = lasio.read(egfn('sample_mnemonic_case.las'), mnemonic_case='preserve')
    assert [c.mnemonic for c in las.curves] == ['Dept', 'Sflu', 'NPHI', 'SFLU', 'SFLU', 'sflu', 'SfLu']

def test_mnemonic_case_upper():
    las = lasio.read(egfn('sample_mnemonic_case.las'), mnemonic_case='upper')
    assert [c.mnemonic for c in las.curves] == ['DEPT', 'SFLU', 'NPHI', 'SFLU', 'SFLU', 'SFLU', 'SFLU']

def test_mnemonic_case_lower():
    las = lasio.read(egfn('sample_mnemonic_case.las'), mnemonic_case='lower')
    assert [c.mnemonic for c in las.curves] == ['dept', 'sflu', 'nphi', 'sflu', 'sflu', 'sflu', 'sflu']

