import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy as np
import pytest

import lasio
from lasio import read, las

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_keys_curve_mnemonics():
    l = lasio.read(egfn("sample.las"))
     # DEPT.M                      :  1  DEPTH
     # DT  .US/M               :  2  SONIC TRANSIT TIME
     # RHOB.K/M3                   :  3  BULK DENSITY
     # NPHI.V/V                    :  4   NEUTRON POROSITY
     # SFLU.OHMM                   :  5  RXO RESISTIVITY
     # SFLA.OHMM                   :  6  SHALLOW RESISTIVITY
     # ILM .OHMM                   :  7  MEDIUM RESISTIVITY
     # ILD .OHMM                   :  8  DEEP RESISTIVITY
    assert l.keys() == ['DEPT', 'DT', 'RHOB', 'NPHI', 'SFLU', 'SFLA', 'ILM', 'ILD']

def test_LASFile_getitem():
    l = lasio.read(egfn("sample.las"))
    assert np.all(l['DT'] == [123.45, 123.45, 123.45])

def test_LASFile_getitem_int():
    l = lasio.read(egfn("sample.las"))
    assert np.all(l[1] == [123.45, 123.45, 123.45])

def test_LASFile_getitem_int_negative():
    l = lasio.read(egfn("sample.las"))
    assert np.all(l[-2] == [110.2, 110.2, 110.2])

def test_data_array_slice():
    l = lasio.read(egfn("sample.las"))
    assert np.all(l[1] == l.data[:, 1])

def test_curves_attribute():
    l = lasio.read(egfn("sample.las"))
    assert isinstance(l.curves[1], las.CurveItem)

def test_get_curves_method():
    l = lasio.read(egfn("sample.las"))
    assert l.get_curve('DT') == l.curves[1]

def test_missing_lasfile_mnemonic():
    las = lasio.read(egfn('sample.las'))
    with pytest.raises(KeyError):
        las['blahblahblah']