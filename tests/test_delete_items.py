import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy as np
import pytest

import lasio

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_delete_curve():
    las = lasio.read(egfn("sample.las"))
    del las.curves['DT']
    assert las.curves.keys() == ['DEPT', 'RHOB', 'NPHI', 'SFLU', 'SFLA','ILM', 'ILD']

def test_delete_section_item_by_index():
    las = lasio.read(egfn('sample.las'))
    del las.params[1]
    assert las.params.keys() == ['BHT', 'FD', 'MATR', 'MDEN', 'RMF', 'DFD']

def test_delete_section_item_by_mnemonic():
    las = lasio.read(egfn('sample.las'))
    del las.params['MDEN']
    assert las.params.keys() == ['BHT', 'BS', 'FD', 'MATR', 'RMF', 'DFD']