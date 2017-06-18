import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy as np
import pytest

from lasio import read

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_delete_curve():
    l = read(egfn("sample.las"))
    shape = l.data.shape[1]
    curve = l.curves.keys()[1]
    l.delete_curve(curve)
    assert curve not in l.curves.keys()
    assert len(l.curves.keys()) == (shape - 1)
    assert l.curves.keys() == ['DEPT', 'RHOB', 'NPHI', 'SFLU', 'SFLA','ILM', 'ILD']
