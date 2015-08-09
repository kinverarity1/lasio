import os

import pytest

from . import read
from .las import StringIO

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)

def test_write():
    l = read(egfn("sample_write_sect_widths.las"))
    s = StringIO()
    l.write(s, version=1.2)
    