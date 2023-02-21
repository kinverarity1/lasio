import os

from pprint import pformat

import pytest
import math

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio
import lasio.las_items
from lasio import read, exceptions

test_dir = os.path.dirname(__file__)


def egfn(fn):
    # egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    # stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)
    return os.path.join(test_dir, "examples", vers, fn)


def test_autodepthindex():
    m = read(egfn("autodepthindex_M.las"))
    m_lower = read(egfn("autodepthindex_M_lower.las"))
    f = read(egfn("autodepthindex_F.las"))
    ft = read(egfn("autodepthindex_FT.las"))
    err = read(egfn("autodepthindex_M_FT.las"))
    assert m.index_unit == "M"
    assert m_lower.index_unit == "M"
    assert f.index_unit == "FT"
    assert ft.index_unit == "FT"
    assert err.index_unit is None


def test_autodepthindex_inconsistent():
    err = read(egfn("autodepthindex_M_FT.las"))
    with pytest.raises(exceptions.LASUnknownUnitError):
        print(err.depth_m)


def test_autodepthindex_m():
    las = read(egfn("autodepthindex_M.las"))
    assert las.depth_ft[-1] * 0.3048 == las.index[-1]


def test_autodepthindex_m_lower():
    las = read(egfn("autodepthindex_M_lower.las"))
    assert las.depth_ft[-1] * 0.3048 == las.index[-1]


def test_autodepthindex_f():
    las = read(egfn("autodepthindex_F.las"))
    assert las.depth_m[-1] / 0.3048 == las.index[-1]


def test_autodepthindex_ft():
    las = read(egfn("autodepthindex_FT.las"))
    assert las.depth_m[-1] / 0.3048 == las.index[-1]


def test_autodepthindex_feet():
    las = read(egfn("autodepthindex_FEET.las"))
    assert las.depth_m[-1] / 0.3048 == las.index[-1]


def test_autodepthindex_point_one_inch():
    # Using 'las' instead of 'l' as the variable because
    # the python debugger uses 'l' to list the current code.
    las = read(egfn("autodepthindex_point_one_inch.las"))
    assert las.index_unit == ".1IN"
    assert las.depth_ft[-1] * 120 == las.index[-1]
    assert (las.depth_m[-1] / 0.3048) * 120 == las.index[-1]


def test_df_indexing():
    las = read(egfn("6038187_v1.2.las"))
    metres = 9.05
    spacing = las.well["STEP"].value
    calc_index = math.floor((metres / spacing) - (las.well["STRT"].value / spacing))
    calc_index = int(calc_index)
    assert las["GAMN"][calc_index] == las.df()["GAMN"][metres]


# TODO: make above test in reverse-ordered LAS (e.g. STRT > STOP)


def test_df_reverse():
    las = read(egfn("sample_rev.las"))
    metres = 1667
    spacing = las.well["STEP"].value
    calc_index = math.floor((metres // spacing) - (las.well["STRT"].value // spacing))
    calc_index = int(calc_index)
    assert las["DT"][calc_index] == las.df()["DT"][metres]


def test_df_curve_names():
    las = read(egfn("sample_rev.las"))
    assert las.keys()[1:] == list(las.df().columns.values)


def test_non_standard_section():
    las = read(egfn("non-standard-header-section.las"))
    assert "SPECIAL INFORMATION" in las.sections.keys()


def test_non_standard_sections():
    las = read(egfn("non-standard-header-sections.las"))
    assert "SPECIAL INFORMATION" in las.sections.keys()
    assert "extra special information" in las.sections.keys()


def test_repr():
    h = lasio.las_items.HeaderItem("MN", unit="m", value=20, descr="test testing")
    assert h.__repr__() == pformat(h)


def test_mnemonic_case_preserved():
    las = lasio.read(egfn("mnemonic_case.las"), mnemonic_case="preserve")
    assert [c.mnemonic for c in las.curves] == [
        "Dept",
        "Sflu",
        "NPHI",
        "SFLU:1",
        "SFLU:2",
        "sflu",
        "SfLu",
    ]


def test_mnemonic_case_upper():
    las = lasio.read(egfn("mnemonic_case.las"), mnemonic_case="upper")
    assert [c.mnemonic for c in las.curves] == [
        "DEPT",
        "SFLU:1",
        "NPHI",
        "SFLU:2",
        "SFLU:3",
        "SFLU:4",
        "SFLU:5",
    ]


def test_mnemonic_case_lower():
    las = lasio.read(egfn("mnemonic_case.las"), mnemonic_case="lower")
    assert [c.mnemonic for c in las.curves] == [
        "dept",
        "sflu:1",
        "nphi",
        "sflu:2",
        "sflu:3",
        "sflu:4",
        "sflu:5",
    ]


def test_duplicate_append_curve():
    las = lasio.read(egfn("sample.las"))
    las.append_curve("TEST", data=[1, 2, 3])
    las.append_curve("TEST", data=[4, 5, 6])
    assert [c.mnemonic for c in las.curves[-2:]] == ["TEST:1", "TEST:2"]


def test_lasfile_setitem_data():
    las = lasio.read(egfn("sample.las"))
    las["EXTRA"] = las["ILD"] / 2
    assert (las.curves["EXTRA"].data == [52.8, 52.8, 52.8]).all()


def test_lasfile_setitem_curveitem():
    las = lasio.read(egfn("sample.las"))
    las["EXTRA"] = lasio.las_items.CurveItem("EXTRA", data=las["ILD"] / 2)
    assert (las.curves["EXTRA"].data == [52.8, 52.8, 52.8]).all()


def test_lasfile_setitem_curveitem_mnemonic_mismatch():
    las = lasio.read(egfn("sample.las"))
    with pytest.raises(KeyError):
        las["EXTRA"] = lasio.las_items.CurveItem("EXTRA2", data=las["ILD"] / 2)
