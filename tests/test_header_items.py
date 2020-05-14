import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pprint import pformat

import pytest

import lasio
import lasio.las_items


test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)

stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn
)


def test_repr():
    h = lasio.las_items.HeaderItem(
        'MN', unit='m', value=20, descr='test testing')

    assert h.__repr__() == pformat(h)


def test_useful_mnemonic_setter_not_allowed():
    h = lasio.las_items.HeaderItem(
        'MN', unit='m', value=20, descr='test testing')

    with pytest.raises(ValueError):
        h.useful_mnemonic = "NEW_NAME"


def test_mmenomic_names_behavior():
    h = lasio.las_items.HeaderItem(
        'MN', unit='m', value=20, descr='test testing')

    h['mnemonic'] = "ZZZ"
    assert h.useful_mnemonic == "MN"

    h.mnemonic = "ZZZ"
    assert h.useful_mnemonic == "ZZZ"


def test_getitem():
    h = lasio.las_items.HeaderItem(
        'MN', unit='m', value=20, descr='test testing')

    assert h["mnemonic"] == "MN"
    assert h["original_mnemonic"] == "MN"
    assert h["useful_mnemonic"] == "MN"
    assert h["unit"] == "m"
    with pytest.raises(KeyError):
        h['notakey']


def test_header_json():
    h = lasio.las_items.HeaderItem(
        'MN', unit='m', value=20, descr='test testing')

    x = [
        '"_type": "HeaderItem"',
        '"mnemonic": "MN"',
        '"unit": "m"',
        '"value": 20',
        '"descr": "test testing"',
    ]
    expect = "{" + ", ".join(x) + "}"

    assert h.json == expect
    with pytest.raises(Exception):
        h.json = '{ "_type: "HeaderItem" }'
