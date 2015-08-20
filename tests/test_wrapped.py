import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lasio import read

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)


def test_wrapped():
    fn = egfn("1001178549.las")
    l = read(fn)
