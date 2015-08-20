import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy
import pytest

from lasio import las, read


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
    with pytest.raises(las.LASUnknownUnitError):
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
