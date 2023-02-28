import os
import pytest
import numpy as np
# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import lasio

test_dir = os.path.dirname(__file__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def test_stack_curves_with_stub():
    las = lasio.read(egfn("multi_channel.las"))
    sc = las.stack_curves("CBP")
    assert (
        sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0003])
    ).all()


def test_stack_unordered_curves_with_stub():
    las = lasio.read(egfn("multi_channel_out_of_order.las"))
    sc = las.stack_curves("CBP")
    assert (
        sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0003])
    ).all()


def test_stack_unordered_natural_sorting_with_stub():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves("CBP")
    assert (
        sc[0]
        == np.array([0.0144, 0.0011, 0.0013, 0.002, 0.0055, 0.0103, 0.0543, 0.2003])
    ).all()


def test_stack_curves_with_list():
    las = lasio.read(egfn("multi_channel.las"))
    sc = las.stack_curves(
        ["CBP1", "CBP2", "CBP3", "CBP4", "CBP5", "CBP6", "CBP7", "CBP8"]
    )
    assert (
        sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0003])
    ).all()


def test_stack_curves_with_ndarray():
    las = lasio.read(egfn("multi_channel.las"))
    sc = las.stack_curves(
        np.array(["CBP1", "CBP2", "CBP3", "CBP4", "CBP5", "CBP6", "CBP7", "CBP8"])
    )
    assert (
        sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0003])
    ).all()


def test_stack_unordered_curves_with_list():
    las = lasio.read(egfn("multi_channel_out_of_order.las"))
    sc = las.stack_curves(
        ["CBP1", "CBP2", "CBP3", "CBP4", "CBP5", "CBP6", "CBP7", "CBP8"]
    )
    assert (
        sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0003])
    ).all()


def test_stack_unordered_natural_sorting_with_list():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves(
        ["CBP13", "CBP2003", "CBP11", "CBP1", "CBP103", "CBP543", "CBP20", "CBP55"]
    )
    assert (
        sc[0]
        == np.array([0.0144, 0.0011, 0.0013, 0.002, 0.0055, 0.0103, 0.0543, 0.2003])
    ).all()


def test_stack_unordered_natural_no_sort_with_list():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves(
        ["CBP13", "CBP2003", "CBP11", "CBP1", "CBP103", "CBP543", "CBP20", "CBP55"],
        sort_curves=False,
    )
    assert (
        sc[0]
        == np.array([0.0013, 0.2003, 0.0011, 0.0144, 0.0103, 0.0543, 0.002, 0.0055])
    ).all()


def test_stack_empty_string():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(ValueError):
        las.stack_curves("")


def test_stack_empty_list():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(ValueError):
        las.stack_curves([])


def test_stack_nothing():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(TypeError):
        las.stack_curves()


def test_stack_list_with_empty_element():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(ValueError):
        las.stack_curves(["CBP1", ""])


def test_stack_mnemonic_not_in_LAS():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(KeyError) as e:
        las.stack_curves("TCMR")
    assert e.value.args[0] == "TCMR not found in LAS curves."


def test_stack_mnemonics_in_list_not_in_LAS():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    with pytest.raises(KeyError) as e:
        las.stack_curves(["CBP1", "CBP13", "KTIM", "TCMR"])
    assert (e.value.args[0] == "TCMR, KTIM not found in LAS curves.") or (
        e.value.args[0] == "KTIM, TCMR not found in LAS curves."
    )
