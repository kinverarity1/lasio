import os

from . import read

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)


def test_wrapped():
    fn = egfn("1001178549.las")
    l = read(fn)
