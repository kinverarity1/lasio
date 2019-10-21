import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import numpy as np

import lasio

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)


def test_stack_curves_with_stub():
    las = lasio.read(egfn("multi_channel.las"))
    sc = las.stack_curves(stub='CBP')
    assert (sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.    , 0.    , 0.    , 0.    , 0.0003])).all()


def test_stack_unordered_curves_with_stub():
    las = lasio.read(egfn("multi_channel_out_of_order.las"))
    sc = las.stack_curves(stub='CBP')
    assert (sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.    , 0.    , 0.    , 0.    , 0.0003])).all()


def test_stack_unordered_natural_sorting_with_stub():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves(stub='CBP')
    assert (sc[0] == np.array([0.0144, 0.0011, 0.0013, 0.002 , 0.0055, 0.0103, 0.0543, 0.2003])).all()


def test_stack_curves_with_list():
    las = lasio.read(egfn("multi_channel.las"))
    sc = las.stack_curves(curve_list=['CBP1', 'CBP2', 'CBP3', 'CBP4', 'CBP5', 'CBP6', 'CBP7', 'CBP8'])
    assert (sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.    , 0.    , 0.    , 0.    , 0.0003])).all()


def test_stack_unordered_curves_with_list():
    las = lasio.read(egfn("multi_channel_out_of_order.las"))
    sc = las.stack_curves(curve_list=['CBP1', 'CBP2', 'CBP3', 'CBP4', 'CBP5', 'CBP6', 'CBP7', 'CBP8'])
    assert (sc[0] == np.array([0.0144, 0.0055, 0.0001, 0.    , 0.    , 0.    , 0.    , 0.0003])).all()


def test_stack_unordered_natural_sorting_with_list():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves(['CBP13', 'CBP2003', 'CBP11', 'CBP1', 'CBP103', 'CBP543', 'CBP20', 'CBP55'])
    assert (sc[0] == np.array([0.0144, 0.0011, 0.0013, 0.002 , 0.0055, 0.0103, 0.0543, 0.2003])).all()


def test_stack_unordered_natural_no_sort_with_list():
    las = lasio.read(egfn("multi_channel_natural_sorting.las"))
    sc = las.stack_curves(['CBP13', 'CBP2003', 'CBP11', 'CBP1', 'CBP103', 'CBP543', 'CBP20', 'CBP55'],
        sort_curves=False)
    assert (sc[0] == np.array([0.0013, 0.2003, 0.0011, 0.0144, 0.0103, 0.0543, 0.002 , 0.0055])).all()