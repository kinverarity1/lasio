import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import glob
import fnmatch
import traceback
import logging

import numpy
import pytest

import lasio

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

logger = logging.getLogger(__name__)



def test_read_v12_sample_big():
    l = lasio.read(stegfn("1.2", "sample_big.las"))
