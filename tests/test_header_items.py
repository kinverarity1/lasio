import os

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pprint import pformat

import json
import pytest

import lasio
import lasio.las_items


test_dir = os.path.dirname(__file__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    return os.path.join(test_dir, "examples", vers, fn)


def test_repr():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")

    assert h.__repr__() == pformat(h)


def test_useful_mnemonic_setter_not_allowed():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")

    # Writing to useful_mnemonic is prevented by exception.
    with pytest.raises(ValueError):
        h.useful_mnemonic = "NEW_NAME"


def test_mmenomic_names_behavior():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")

    # mnemonic is not changed
    h["mnemonic"] = "ZZZ"
    assert h["mnemonic"] == "MN"
    assert h.mnemonic == "MN"
    assert h.useful_mnemonic == "MN"

    # mnemonic is changed
    h.mnemonic = "ZZZ"
    assert h.useful_mnemonic == "ZZZ"


def test_getitem():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")

    assert h["mnemonic"] == "MN"
    assert h["original_mnemonic"] == "MN"
    assert h["useful_mnemonic"] == "MN"
    assert h["unit"] == "m"
    with pytest.raises(KeyError):
        h["notakey"]


def test_header_json():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")

    # HeaderItem transformed to json string that includes
    # object type and property key/values.
    myjson = h.json

    # Transform json string into a python dictionary
    result = json.loads(myjson)

    for key in result.keys():
        if key == "_type":
            # type of the object this json came from
            assert result[key] == "HeaderItem"
        else:
            # data key/values: mnemonic, name, value, descr
            assert result[key] == h[key]

    # Verify write-to-HeaderItem.json is discouraged.
    with pytest.raises(Exception):
        h.json = '{ "_type: "HeaderItem" }'
