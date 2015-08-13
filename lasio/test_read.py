import fnmatch
import os

from . import read

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "test_examples", vers, fn)


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


def test_read_v3_sample():
    l = read(stegfn("3.0", "sample_3.0.las"))


def test_read_v3_sample_spec():
    l = read(stegfn("3.0", "sample_las3.0_spec.las"))


def test_dodgy_param_sect():
    l = read(egfn("dodgy_param_sect.las"))


def test_mnemonic_good():
    l = read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]


def test_mnemonic_duplicate():
    l = read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU[0]", "SFLU[1]", "ILM", "ILD"]


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
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN[0]", "UNKNOWN[1]", "ILM", "ILD"]
