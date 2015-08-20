import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import codecs

import pytest

from lasio import read

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)

