import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy
import pytest
import pickle

from lasio import las, read, exceptions


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)


def test_pickle_default_wb():
    las = read(egfn('sample.las'))
    with open('binary_serialization', 'wb') as fw:
        pickle.dump(las, fw)
    with open('binary_serialization', 'rb') as fr:
        las = pickle.load(fr)
    os.remove('binary_serialization')
