import os


import lasio

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(test_dir, "examples", fn)


def test_dodgy_param_sect():
    l = lasio.read(egfn("dodgy_param_sect.las"))


def test_mnemonic_good():
    l = lasio.read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]


def test_mnemonic_duplicate():
    l = lasio.read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU[0]", "SFLU[1]", "ILM", "ILD"]


def test_mnemonic_leading_period():
    l = lasio.read(egfn("mnemonic_leading_period.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing():
    l = lasio.read(egfn("mnemonic_missing.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing_multiple():
    l = lasio.read(egfn("mnemonic_missing_multiple.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN[0]", "UNKNOWN[1]", "ILM", "ILD"]
