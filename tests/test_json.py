import os
import json
import pytest

# 02-21-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio
import lasio.examples
from lasio import read


test_dir = os.path.dirname(__file__)


def egfn(fn):
    # egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    # stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)
    return os.path.join(test_dir, "examples", vers, fn)


def test_json_encoder_direct():
    las = read(egfn("sample.las"))
    with pytest.raises(TypeError):
        t = json.dumps(las)
        # Should never get here because of the Exception
        assert t == "null"


def test_json_encoder_default():
    las = read(egfn("sample.las"))
    t = json.dumps(las, default=lambda x: None)
    assert t == "null"


def test_json_encoder_cls_specify():
    las = read(egfn("sample.las"))
    t = json.dumps(las, cls=lasio.JSONEncoder)
    pylj = json.loads(t)
    # Verify this is still structurally sound LAS content
    assert len(pylj["metadata"]["Curves"]) == len(pylj["data"])


def test_json_headers():
    las = read("./tests/examples/2.0/sample_2.0.las")
    lj = json.dumps(las, cls=lasio.JSONEncoder)
    pylj = json.loads(lj)
    assert pylj["metadata"]["Version"]["VERS"] == 2.0
    assert pylj["metadata"]["Version"]["WRAP"] == "NO"
    assert pylj["metadata"]["Well"]["STRT"] == 1670
    assert pylj["metadata"]["Curves"]["DT"] == "60 520 32 00"
    assert pylj["metadata"]["Parameter"]["DFD"] == 1525


def test_json_null():
    las = lasio.examples.open("sample_null.las")
    lj = json.dumps(las, cls=lasio.JSONEncoder, sort_keys=True)
    assert lj == open(egfn("sample_null.json"), "r").read()
