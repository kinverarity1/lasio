import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import glob
import fnmatch
import traceback
import logging

import numpy
import pytest
from numbers import Number

import lasio

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)

logger = logging.getLogger(__name__)


def test_read_v12_sample():
    l = lasio.read(stegfn("1.2", "sample.las"))


def test_read_v12_sample_curve_api():
    l = lasio.read(stegfn("1.2", "sample_curve_api.las"))


def test_read_v12_sample_minimal():
    l = lasio.read(stegfn("1.2", "sample_minimal.las"))


def test_read_v12_sample_wrapped():
    l = lasio.read(stegfn("1.2", "sample_wrapped.las"))


def test_read_v2_sample():
    l = lasio.read(stegfn("2.0", "sample_2.0.las"))


def test_read_v2_sample_based():
    l = lasio.read(stegfn("2.0", "sample_2.0_based.las"))


def test_read_v2_sample_minimal():
    l = lasio.read(stegfn("2.0", "sample_2.0_minimal.las"))


def test_read_v2_sample_wrapped():
    l = lasio.read(stegfn("2.0", "sample_2.0_wrapped.las"))


def test_dodgy_param_sect():
    with pytest.raises(lasio.exceptions.LASHeaderError):
        l = lasio.read(egfn("dodgy_param_sect.las"))


def test_ignore_header_errors():
    l = lasio.read(egfn("dodgy_param_sect.las"), ignore_header_errors=True)


def test_mnemonic_good():
    l = lasio.read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "SFLU",
        "SFLA",
        "ILM",
        "ILD",
    ]


def test_mnemonic_duplicate():
    l = lasio.read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "SFLU:1",
        "SFLU:2",
        "ILM",
        "ILD",
    ]


def test_mnemonic_leading_period():
    l = lasio.read(egfn("mnemonic_leading_period.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "SFLU",
        "SFLA",
        "ILM",
        "ILD",
    ]


def test_mnemonic_missing():
    l = lasio.read(egfn("mnemonic_missing.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "UNKNOWN",
        "SFLA",
        "ILM",
        "ILD",
    ]


def test_mnemonic_missing_multiple():
    l = lasio.read(egfn("mnemonic_missing_multiple.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "UNKNOWN:1",
        "UNKNOWN:2",
        "ILM",
        "ILD",
    ]


def test_multi_curve_mnemonics():
    l = lasio.read(egfn("sample_issue105_a.las"))
    assert (
        l.keys()
        == [c.mnemonic for c in l.curves]
        == ["DEPT", "RHO:1", "RHO:2", "RHO:3", "PHI"]
    )


def test_multi_missing_curve_mnemonics():
    l = lasio.read(egfn("sample_issue105_b.las"))
    assert (
        l.keys()
        == [c.mnemonic for c in l.curves]
        == ["DEPT", "UNKNOWN:1", "UNKNOWN:2", "UNKNOWN:3", "PHI"]
    )


def test_multi_curve_mnemonics_gr():
    l = lasio.read(egfn("sample_issue105_c.las"))
    assert (
        l.keys()
        == [c.mnemonic for c in l.curves]
        == [
            "DEPT",
            "GR:1",
            "GR:2",
            "GR[0]",
            "GR[1]",
            "GR[2]",
            "GR[3]",
            "GR[4]",
            "GR[5]",
        ]
    )


#  DEPT.M                      :  1  DEPTH
# GR.gAPI: mean gamma ray value
# GR.gAPI: corrected gamma ray value
# GR[0].gAPI: gamma ray image at angle 0 dega
# GR[1].gAPI: gamma ray image at angle 60 dega
# GR[2].gAPI: gamma ray image at angle 120 dega
# GR[3].gAPI: gamma ray image at angle 180 dega
# GR[4].gAPI: gamma ray image at angle 240 dega
# GR[5].gAPI: gamma ray image at angle 300 dega


def test_inf_uwi():
    l = lasio.read(stegfn("2.0", "sample_2.0_inf_uwi.las"))
    assert l.well["UWI"].value == "300E074350061450"


def test_v12_inf_uwi_leading_zero_value():
    las = lasio.read(stegfn("1.2", "sample_inf_uwi_leading_zero.las"))
    assert las.well["UWI"].value == "05001095820000"
    # check that numerical fields are still treated as numbers
    assert isinstance(las.well["STRT"].value, Number)


def test_v12_inf_api_leading_zero_value():
    las = lasio.read(stegfn("1.2", "sample_inf_api_leading_zero.las"))
    assert las.well["API"].value == "05001095820000"
    # check that numerical fields are still treated as numbers
    assert isinstance(las.well["STRT"].value, Number)


def test_v2_inf_uwi_leading_zero_value():
    las = lasio.read(stegfn("2.0", "sample_2.0_inf_uwi_leading_zero.las"))
    assert las.well["UWI"].value == "05001095820000"
    # check that numerical fields are still treated as numbers
    assert isinstance(las.well["STRT"].value, Number)


def test_v2_inf_api_leading_zero_value():
    las = lasio.read(stegfn("2.0", "sample_2.0_inf_api_leading_zero.las"))
    assert las.well["API"].value == "05001095820000"
    # check that numerical fields are still treated as numbers
    assert isinstance(las.well["STRT"].value, Number)


def test_missing_vers_loads():
    l = lasio.read(egfn("missing_vers.las"))


def test_missing_vers_missing_headeritem():
    l = lasio.read(egfn("missing_vers.las"))
    assert not "VERS" in l.version


def test_missing_vers_write_version_none_fails():
    l = lasio.read(egfn("missing_vers.las"))
    with pytest.raises(KeyError):
        l.write(sys.stdout, version=None)


def test_missing_vers_write_version_specified_works():
    l = lasio.read(egfn("missing_vers.las"))
    l.write(sys.stdout, version=1.2)


def test_missing_wrap_loads():
    l = lasio.read(egfn("missing_wrap.las"))


def test_missing_wrap_missing_headeritem():
    l = lasio.read(egfn("missing_wrap.las"))
    assert not "WRAP" in l.version


def test_missing_wrap_write_wrap_none_fails():
    l = lasio.read(egfn("missing_wrap.las"))
    with pytest.raises(KeyError):
        l.write(sys.stdout, wrap=None)


def test_missing_wrap_write_wrap_specified_works():
    l = lasio.read(egfn("missing_wrap.las"))
    l.write(sys.stdout, wrap=True)


def test_missing_null_loads():
    l = lasio.read(egfn("missing_null.las"))


def test_missing_null_missing_headeritem():
    l = lasio.read(egfn("missing_null.las"))
    assert not "NULL" in l.well


def test_barebones():
    las = lasio.read(egfn("barebones.las"))
    assert las["DEPT"][1] == 201


def test_barebones_missing_all_sections():
    las = lasio.read(egfn("barebones2.las"))
    assert las.curves[-1].mnemonic == "UNKNOWN:8"


def test_not_a_las_file():
    with pytest.raises(KeyError):
        las = lasio.read(egfn("not_a_las_file.las"))


def test_comma_decimal_mark_data():
    las = lasio.read(egfn("comma_decimal_mark.las"))
    assert las["SFLU"][1] == 123.42


def test_comma_decimal_mark_params():
    las = lasio.read(egfn("comma_decimal_mark.las"))
    assert las.params["MDEN"].value == 2710.1


def test_missing_a_section():
    las = lasio.read(egfn("missing_a_section.las"))
    assert not las.data


def test_blank_line_in_header():
    las = lasio.read(egfn("blank_line.las"))
    assert las.curves[0].mnemonic == "DEPT"


def test_duplicate_step():
    las = lasio.read(egfn("duplicate_step.las"))


def test_blank_line_at_start():
    las = lasio.read(egfn("blank_line_start.las"))


def test_missing_STRT_STOP():
    las = lasio.read(egfn("sample_TVD.las"))
    assert len(las.well) == 12


def test_UWI_API_leading_zero():
    las = lasio.read(egfn("UWI_API_leading_zero.las"))
    assert las.well["UWI"].value == "05123370660000"


def test_sparse_curves():
    las = lasio.read(egfn("sparse_curves.las"))
    assert las.curves.keys() == [
        "DEPT",
        "DT",
        "RHOB",
        "NPHI",
        "SFLU",
        "SFLA",
        "ILM",
        "ILD",
    ]


def test_issue92():
    las = lasio.read(egfn("issue92.las"), ignore_header_errors=True)


def test_emptyparam(capsys):
    las = lasio.read(egfn("emptyparam.las"))
    out, err = capsys.readouterr()
    msg = "Header section Parameter regexp=~P is empty."
    assert not msg in out


def test_data_characters_1():
    las = lasio.read(egfn("data_characters.las"))
    assert las["TIME"][0] == "00:00:00"


def test_data_characters_2():
    las = lasio.read(egfn("data_characters.las"))
    assert las["DATE"][0] == "01-Jan-20"


def test_data_characters_types():
    from pandas.api.types import is_object_dtype
    from pandas.api.types import is_float_dtype

    las = lasio.read(egfn("data_characters.las"))
    assert is_object_dtype(las.df().index.dtype)
    assert is_object_dtype(las.df()["DATE"].dtype)
    assert is_float_dtype(las.df()["DEPT"].dtype)
    assert is_float_dtype(las.df()["ARC_GR_UNC_RT"].dtype)


def test_strip_square_brackets():
    las = lasio.read(egfn("sample_bracketed_units.las"))
    assert las.curves[0].unit == "M"


def test_index_unit_equals_f():
    las = lasio.read(egfn("autodepthindex_M.las"), index_unit="f")
    assert (las.depth_ft == las.index).all()

def test_index_unit_equals_m():
    las = lasio.read(egfn("autodepthindex_M.las"), index_unit="m")
    assert (las.depth_ft[1:] != las.index[1:]).all()


def test_read_incorrect_shape():
    with pytest.raises(ValueError):
        lasio.read(egfn("sample_lastcolblanked.las"))
