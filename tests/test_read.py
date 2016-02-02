import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy as np
import pytest

from lasio import read

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

NaN = np.nan

def test_read_v12_sample():
    l = read(stegfn("1.2", "sample.las"))


def test_read_v12_sample_big():
    l = read(stegfn("1.2", "sample_big.las"))


def test_read_v12_sample_curve_api():
    l = read(stegfn("1.2", "sample_curve_api.las"))


def test_read_v12_sample_minimal():
    l = read(stegfn("1.2", "sample_minimal.las"))


def test_read_v12_sample_wrapped():
    l = read(stegfn("1.2", "sample_wrapped.las"))


def test_read_v2_sample():
    l = read(stegfn("2.0", "sample_2.0.las"))


def test_read_v2_sample_based():
    l = read(stegfn("2.0", "sample_2.0_based.las"))


def test_read_v2_sample_minimal():
    l = read(stegfn("2.0", "sample_2.0_minimal.las"))


def test_read_v2_sample_wrapped():
    l = read(stegfn("2.0", "sample_2.0_wrapped.las"))


def test_dodgy_param_sect():
    l = read(egfn("dodgy_param_sect.las"))


def test_mnemonic_good():
    l = read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]


def test_mnemonic_duplicate():
    l = read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU:1", "SFLU:2", "ILM", "ILD"]


def test_mnemonic_leading_period():
    l = read(egfn("mnemonic_leading_period.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing():
    l = read(egfn("mnemonic_missing.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing_multiple():
    l = read(egfn("mnemonic_missing_multiple.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN:1", "UNKNOWN:2", "ILM", "ILD"]

# ~A DEPTH     DT  RHOB    NPHI     SFLU   SFLA
# 1.000   -999.25 -9999    0.450  123.450  1
# 2.000   -999.25 -9999    0.460  123.460  2
# 3.000   1       -9999    0.47   123.45   3
# 4.000   2       3        0.48   123.46   4
# 5.000   3       4        231.2  123.45   5
# 6.000   4       5        231.2  1        6
# 7.000   5       6        231.2  1        7
# 8.000   6       7        231.2  1        8
# 9.000   6       32767    231.2  -999.25  9

def test_null_policy_numeric_None():
    l = read(egfn("null_policy_numeric.las"), null_policy=None)
    assert np.all(l['DT'] == [-999.25, -999.25, 1, 2, 3, 4, 5, 6, 6])
    assert np.all(l['RHOB'] == [-9999, -9999, -9999, 3, 4, 5, 6, 7, 32767])
    assert np.all(l['NPHI'] == [.45, .46, .47, .48, 231.2, 231.2, 231.2, 231.2, 231.2])
    assert np.all(l['SFLU'] == [123.45, 123.46, 123.45, 123.46, 123.45, 1, 1, 1, -999.25])
    assert np.all(l['SFLA'] == [1, 2, 3, 4, 5, 6, 7, 8, 9])

def test_null_policy_numeric_NULL():
    l = read(egfn("null_policy_numeric.las"), null_policy='NULL')
    assert np.all(np.isnan(l['DT']) == [True, True, False, False, False, False, False, False, False])
    assert np.isfinite(l['RHOB']).all()
    assert np.isfinite(l['NPHI']).all()
    assert np.all(np.isnan(l['SFLU']) == [False, False, False, False, False, False, False, False, True])
    assert np.isfinite(l['SFLA']).all()

def test_null_policy_numeric_common():
    l = read(egfn("null_policy_numeric.las"), null_policy='common')
    assert np.all(np.isnan(l['DT']) == [True, True, False, False, False, False, False, False, False])
    assert np.all(np.isnan(l['RHOB']) == [True, True, True, False, False, False, False, False, True])
    assert np.isfinite(l['NPHI']).all()
    assert np.all(np.isnan(l['SFLU']) == [False, False, False, False, False, False, False, False, True])
    assert np.isfinite(l['SFLA']).all()

def test_null_policy_numeric_aggressive():
    l = read(egfn("null_policy_numeric.las"), null_policy='aggressive')
    assert np.all(np.isnan(l['DT']) == [True, True, False, False, False, False, False, True, True])
    assert np.all(np.isnan(l['RHOB']) == [True, True, True, False, False, False, False, False, True])
    assert np.all(np.isnan(l['NPHI']) == [False, False, False, False, True, True, True, True, True])
    assert np.all(np.isnan(l['SFLU']) == [False, False, False, False, False, True, True, True, True])
    assert np.isfinite(l['SFLA']).all()

def test_multi_curve_mnemonics():
    l = read(egfn('sample_issue105_a.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'RHO:1', 'RHO:2', 'RHO:3', 'PHI']


def test_multi_missing_curve_mnemonics():
    l = read(egfn('sample_issue105_b.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'UNKNOWN:1', 'UNKNOWN:2', 'UNKNOWN:3', 'PHI']


def test_multi_curve_mnemonics_gr():
    l = read(egfn('sample_issue105_c.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'GR:1', 'GR:2', 'GR[0]', 'GR[1]', 'GR[2]', 'GR[3]', 'GR[4]', 'GR[5]']

#  DEPT.M                      :  1  DEPTH
# GR.gAPI: mean gamma ray value
# GR.gAPI: corrected gamma ray value
# GR[0].gAPI: gamma ray image at angle 0 dega
# GR[1].gAPI: gamma ray image at angle 60 dega
# GR[2].gAPI: gamma ray image at angle 120 dega
# GR[3].gAPI: gamma ray image at angle 180 dega
# GR[4].gAPI: gamma ray image at angle 240 dega
# GR[5].gAPI: gamma ray image at angle 300 dega