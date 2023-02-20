import os

import numpy as np
import pytest

import logging

import lasio
import lasio.examples


logger = logging.getLogger(__name__)

test_dir = os.path.dirname(__file__)


def egfn(fn):
    # egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    # stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)
    return os.path.join(test_dir, "examples", vers, fn)


def test_version():
    assert "." in lasio.__version__


def test_keys_curve_mnemonics():
    las = lasio.read(egfn("sample.las"))
    # DEPT.M                      :  1  DEPTH
    # DT  .US/M               :  2  SONIC TRANSIT TIME
    # RHOB.K/M3                   :  3  BULK DENSITY
    # NPHI.V/V                    :  4   NEUTRON POROSITY
    # SFLU.OHMM                   :  5  RXO RESISTIVITY
    # SFLA.OHMM                   :  6  SHALLOW RESISTIVITY
    # ILM .OHMM                   :  7  MEDIUM RESISTIVITY
    # ILD .OHMM                   :  8  DEEP RESISTIVITY
    assert las.keys() == ["DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]


def test_LASFile_getitem():
    las = lasio.read(egfn("sample.las"))
    assert np.all(las["DT"] == [123.45, 123.45, 123.45])


def test_LASFile_getitem_int():
    las = lasio.read(egfn("sample.las"))
    assert np.all(las[1] == [123.45, 123.45, 123.45])


def test_LASFile_getitem_int_negative():
    las = lasio.read(egfn("sample.las"))
    assert np.all(las[-2] == [110.2, 110.2, 110.2])


def test_data_array_slice():
    las = lasio.read(egfn("sample.las"))
    assert np.all(las[1] == las.data[:, 1])


def test_curves_attribute():
    las = lasio.read(egfn("sample.las"))
    assert isinstance(las.curves[1], lasio.las.CurveItem)


def test_get_curves_method():
    las = lasio.read(egfn("sample.las"))
    assert las.get_curve("DT") == las.curves[1]


def test_missing_lasfile_mnemonic():
    las = lasio.read(egfn("sample.las"))
    with pytest.raises(KeyError):
        las["blahblahblah"]


def test_append_curve_and_item():
    las = lasio.LASFile()
    data = [1, 2, 3]
    las.append_curve("TEST1", data=data)
    las.append_curve_item(lasio.CurveItem("TEST2", data=data))
    assert (las["TEST1"] == las["TEST2"]).all()


def test_data_attr():
    las = lasio.LASFile()
    las.append_curve("TEST1", data=[1, 2, 3])
    las.append_curve_item(lasio.CurveItem("TEST2", data=[4, 5, 6]))
    las.append_curve("TEST3", data=[7, 8, 9])
    logger.debug("las.data = {}".format(las.data))
    # the .all() method assumes these are numpy ndarrays; that should be the case.
    assert (las.data == np.asarray([[1, 4, 7], [2, 5, 8], [3, 6, 9]])).all()


def test_update_curve():
    las = lasio.examples.open("sample.las")
    las["NPHI"] = las["NPHI"] * 100
    assert "NPHI" in las.keys()
    assert "NPHI:1" not in las.keys()
    assert "NPHI:2" not in las.keys()


def test_replace_curve():
    las = lasio.examples.open("sample.las")
    las["NPHI"] = lasio.CurveItem("NPHI", "%", "Porosity", data=(las["NPHI"] * 100))
    assert las.keys() == ["DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]
    assert (las["NPHI"] == [45, 45, 45]).all()
