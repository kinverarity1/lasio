import fnmatch
import os

import numpy
import pytest

from lasio import las, read


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "test_examples", vers, fn)


def test_autodepthindex():
    m = read(egfn("autodepthindex_M.las"))
    f = read(egfn("autodepthindex_F.las"))
    ft = read(egfn("autodepthindex_FT.las"))
    err = read(egfn("autodepthindex_M_FT.las"))


def test_autodepthindex_inconsistent():
    err = read(egfn("autodepthindex_M_FT.las"))
    with pytest.raises(las.LASUnknownUnitError):
        print(err.index_m)


def test_autodepthindex_m():
    l = read(egfn("autodepthindex_M.las"))
    assert l.index_ft[-1] == 328.084


def test_autodepthindex_f():
    l = read(egfn("autodepthindex_F.las"))
    assert numpy.abs(l.index_m[-1] - 30.48) < 0.00001


def test_autodepthindex_ft():
    l = read(egfn("autodepthindex_FT.las"))
    assert numpy.abs(l.index_m[-1] - 30.48) < 0.00001
