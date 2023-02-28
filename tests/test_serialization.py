import os
import pickle

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lasio import read

test_dir = os.path.dirname(__file__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    return os.path.join(test_dir, "examples", vers, fn)


def test_pickle_default_wb():
    las = read(egfn("sample.las"))
    with open("binary_serialization", "wb") as fw:
        pickle.dump(las, fw)
    with open("binary_serialization", "rb") as fr:
        las = pickle.load(fr)
    os.remove("binary_serialization")
