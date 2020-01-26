import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json

import pytest

from lasio import las, read


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_json_encoder_direct():
    l = read(egfn("sample.las"))
    with pytest.raises(TypeError):
        t = json.dumps(l)

def test_json_encoder_default():
    l = read(egfn("sample.las"))
    t = json.dumps(l, default=lambda x: None)

def test_json_encoder_cls_specify():
    l = read(egfn("sample.las"))
    t = json.dumps(l, cls=las.JSONEncoder)

def test_json_headers():
    l = read("./tests/examples/2.0/sample_2.0.las")
    lj = json.dumps(l, cls=las.JSONEncoder)
    pylj = json.loads(lj)
    assert(pylj['metadata']['Version']['VERS'] == 2.0)
    assert(pylj['metadata']['Version']['WRAP'] == 'NO')
    assert(pylj['metadata']['Well']['STRT'] == 1670)
    assert(pylj['metadata']['Curves']['DT'] == '60 520 32 00')
    assert(pylj['metadata']['Parameter']['DFD'] == 1525)

