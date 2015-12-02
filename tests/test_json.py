import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json

import pytest

from lasio import las, read


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_json_encoder_direct():
    t = json.dumps(lasobj)

def test_json_encoder_default():
    t = json.dumps(lasobj, default=lambda x: None)

def test_json_encoder_cls_specify():
    t = json.dumps(lasobj, cls=las.JSONEncoder)