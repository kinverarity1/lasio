import os
import logging


# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio

test_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    return os.path.join(test_dir, "examples", vers, fn)


def read_file():
    las = lasio.read(stegfn("1.2", "sample_big.las"))
    assert isinstance(las, lasio.LASFile)


def test_read_v12_sample_big(benchmark):
    benchmark(read_file)
