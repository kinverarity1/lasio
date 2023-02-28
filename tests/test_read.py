import os
import sys

import logging

import numpy
import pytest
from numbers import Number

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio
import lasio.examples
from lasio.las import LASFile

las_type = type(LASFile())
logger = logging.getLogger(__name__)
test_dir = os.path.dirname(__file__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def stegfn(vers, fn):
    return os.path.join(test_dir, "examples", vers, fn)


def test_read_v12_sample():
    las = lasio.read(stegfn("1.2", "sample.las"))
    assert isinstance(las, LASFile)


def test_read_v12_sample_curve_api():
    las = lasio.read(stegfn("1.2", "sample_curve_api.las"))
    assert isinstance(las, LASFile)


def test_read_v12_sample_minimal():
    las = lasio.read(stegfn("1.2", "sample_minimal.las"))
    assert isinstance(las, LASFile)


def test_read_v12_sample_wrapped():
    las = lasio.read(stegfn("1.2", "sample_wrapped.las"))
    assert isinstance(las, LASFile)


def test_read_v2_sample():
    las = lasio.read(stegfn("2.0", "sample_2.0.las"))
    assert isinstance(las, LASFile)


def test_read_v2_sample_based():
    las = lasio.read(stegfn("2.0", "sample_2.0_based.las"))
    assert isinstance(las, LASFile)


def test_read_v2_sample_minimal():
    las = lasio.read(stegfn("2.0", "sample_2.0_minimal.las"))
    assert isinstance(las, LASFile)


def test_read_v2_sample_wrapped():
    las = lasio.read(stegfn("2.0", "sample_2.0_wrapped.las"))
    assert isinstance(las, LASFile)


def test_read_v2_1_sample():
    las = lasio.read(egfn("sample_2.1.las"))
    assert isinstance(las, LASFile)


def test_dodgy_param_sect():
    with pytest.raises(lasio.exceptions.LASHeaderError):
        las = lasio.read(egfn("dodgy_param_sect.las"))
        # Should never get here because the Exception should be thrown first
        assert isinstance(las, LASFile)


def test_ignore_header_errors():
    las = lasio.read(egfn("dodgy_param_sect.las"), ignore_header_errors=True)
    assert isinstance(las, LASFile)


def test_mnemonic_good():
    las = lasio.read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in las.curves] == [
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
    las = lasio.read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in las.curves] == [
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
    las = lasio.read(egfn("mnemonic_leading_period.las"))
    assert [c.mnemonic for c in las.curves] == [
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
    las = lasio.read(egfn("mnemonic_missing.las"))
    assert [c.mnemonic for c in las.curves] == [
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
    las = lasio.read(egfn("mnemonic_missing_multiple.las"))
    assert [c.mnemonic for c in las.curves] == [
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
    las = lasio.read(egfn("sample_issue105_a.las"))
    assert (
        las.keys()
        == [c.mnemonic for c in las.curves]
        == ["DEPT", "RHO:1", "RHO:2", "RHO:3", "PHI"]
    )


def test_multi_missing_curve_mnemonics():
    las = lasio.read(egfn("sample_issue105_b.las"))
    assert (
        las.keys()
        == [c.mnemonic for c in las.curves]
        == ["DEPT", "UNKNOWN:1", "UNKNOWN:2", "UNKNOWN:3", "PHI"]
    )


def test_multi_curve_mnemonics_gr():
    las = lasio.read(egfn("sample_issue105_c.las"))
    assert (
        las.keys()
        == [c.mnemonic for c in las.curves]
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
    las = lasio.read(stegfn("2.0", "sample_2.0_inf_uwi.las"))
    assert las.well["UWI"].value == "300E074350061450"


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
    las = lasio.read(egfn("missing_vers.las"))
    assert isinstance(las, LASFile)


def test_missing_vers_missing_headeritem():
    las = lasio.read(egfn("missing_vers.las"))
    assert "VERS" not in las.version


def test_missing_vers_write_version_none_fails():
    las = lasio.read(egfn("missing_vers.las"))
    with pytest.raises(KeyError):
        las.write(sys.stdout, version=None)


def test_missing_vers_write_version_specified_works():
    las = lasio.read(egfn("missing_vers.las"))
    las.write(sys.stdout, version=1.2)


def test_missing_wrap_loads():
    las = lasio.read(egfn("missing_wrap.las"))
    assert isinstance(las, LASFile)


def test_missing_wrap_missing_headeritem():
    las = lasio.read(egfn("missing_wrap.las"))
    assert "WRAP" not in las.version


def test_missing_wrap_write_wrap_none_fails():
    las = lasio.read(egfn("missing_wrap.las"))
    with pytest.raises(KeyError):
        las.write(sys.stdout, wrap=None)


def test_missing_wrap_write_wrap_specified_works():
    las = lasio.read(egfn("missing_wrap.las"))
    las.write(sys.stdout, wrap=True)


def test_missing_null_loads():
    las = lasio.read(egfn("missing_null.las"))
    assert isinstance(las, LASFile)


def test_missing_null_missing_headeritem():
    las = lasio.read(egfn("missing_null.las"))
    assert "NULL" not in las.well


def test_barebones():
    las = lasio.read(egfn("barebones.las"))
    assert las["DEPT"][1] == 201


def test_barebones_missing_all_sections():
    las = lasio.read(egfn("barebones2.las"))
    assert las.curves[-1].mnemonic == "UNKNOWN:8"


def test_not_a_las_file():
    with pytest.raises(KeyError):
        las = lasio.read(egfn("not_a_las_file.las"))
        assert type(las) is not las_type


def test_comma_decimal_mark_data():
    las = lasio.read(egfn("comma_decimal_mark.las"))
    assert las["SFLU"][1] == 123.42


def test_comma_decimal_mark_params():
    las = lasio.read(egfn("comma_decimal_mark.las"))
    assert las.params["MDEN"].value == 2710.1


def test_missing_a_section():
    las = lasio.read(egfn("missing_a_section.las"))
    assert las.data.size == 0


def test_blank_line_in_header():
    las = lasio.read(egfn("blank_line.las"))
    assert las.curves[0].mnemonic == "DEPT"


def test_duplicate_step():
    las = lasio.read(egfn("duplicate_step.las"))
    assert isinstance(las, LASFile)


def test_blank_line_at_start():
    las = lasio.read(egfn("blank_line_start.las"))
    assert isinstance(las, LASFile)


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
    assert isinstance(las, LASFile)


def test_emptyparam(capsys):
    las = lasio.read(egfn("emptyparam.las"))
    assert las.header["Parameter"] == []
    out, err = capsys.readouterr()
    msg = "Header section Parameter regexp=~P is empty."
    assert msg not in out


def test_data_characters_1():
    las = lasio.read(egfn("data_characters.las"))
    assert las["TIME"][0] == "00:00:00"


def test_data_characters_2():
    las = lasio.read(egfn("data_characters.las"))
    assert las["DATE"][0] == "01-Jan-20"


def test_data_characters_numeric():
    las = lasio.read(egfn("data_characters_numeric.las"))
    assert las["DATE"][0] == "2020-01-01"


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


def test_dot_delimiter_issue_264():
    las = lasio.read(stegfn("1.2", "issue-264-dot-delimiter.las"))
    assert [c.mnemonic for c in las.curves] == [
        "DEPT",
        "SPEED",
        "COND.",
        "GAMMA",
        "I. RES.",
    ]
    assert [c.unit for c in las.curves] == ["FT", "M/MIN", "MS/M", "CPS", "OHM-M"]
    assert [c.value for c in las.curves] == ["", "", "", "", ""]


def test_issue_201_non_delimiter_colon_start():
    las = lasio.read(egfn("colon_pick_start.las"))
    assert las.params["TCS"].descr == "Time Circ. Stopped"
    assert las.params["TIML"].unit == "hh:mm"
    assert las.params["TIML"].value == "23:15 23-JAN-2001"
    assert las.params["TIML"].descr == "Time Logger: At Bottom"


def test_issue_201_non_delimiter_colon_end():
    las = lasio.read(egfn("colon_pick_end.las"))
    assert las.params["TCS"].descr == "Time Circ. Stopped"
    assert las.params["TIML"].unit == "hh:mm"
    assert las.params["TIML"].value == "23:15 23-JAN-2001"
    assert las.params["TIML"].descr == "Time Logger At Bottom:"


def test_header_only_file():
    las = lasio.read(egfn("header_only.las"))
    assert las.well.STRT.value == 9000.0
    assert las.well.STOP.value == 10000.0
    assert las.curves[0].mnemonic == "DEPT"
    assert las.curves[0].unit == "ft"
    assert las.curves[12].mnemonic == "WPHI_FIT[1]"
    assert len(las.curves) == 21


def test_read_cyrillic_depth_unit():
    las = lasio.read(egfn("sample_cyrillic_depth_unit.las"))
    assert las.index_unit == "M"


def test_section_parser_num_except_pass():
    sp = lasio.reader.SectionParser("~C")
    assert sp.num(None) is None


def test_skip_comments_in_data_section():
    las = lasio.read(egfn("skip_data_section_comments.las"))
    assert (las.curves[0].data == [0.3, 0.4, 0.5, 0.6]).all()


def test_quoted_substrings_in_data_section():
    las = lasio.read(egfn("lasio_issue_271.las"))
    assert (
        las.curves[2].data
        == ["pick_alpha", "pick_beta", "pick gamma", "pick delta", "pick_epsilon"]
    ).all()


def test_read_v2_sample_empty_other_section():
    las = lasio.read(stegfn("2.0", "sample_2.0_empty_other_section.las"))
    assert las.other == ""
    assert las.data[0][0] == 1670.0


def test_sample_dtypes_specified():
    las = lasio.examples.open(
        "sample_str_in_data.las", read_policy=[], dtypes=[float, str, int, float]
    )
    # DT_STR
    assert isinstance(las.curves[1].data[0], str)
    # RHOB_INT
    # assert isinstance(las.curves[2].data[0], int)
    # The above fails because dtypes are fun - instead we check the opposite:
    assert not isinstance(las.curves[2].data[0], float)
    # NPHI_FLOAT
    assert isinstance(las.curves[3].data[0], float)


def test_sample_dtypes_specified_as_dict():
    las = lasio.examples.open(
        "sample_str_in_data.las", read_policy=[], dtypes={"NPHI_FLOAT": str}
    )
    # RHOB_INT -> float by default
    assert isinstance(las.curves[2].data[0], float)
    # NPHI_FLOAT -> str by specification
    assert isinstance(las.curves[3].data[0], str)


def test_sample_dtypes_specified_as_false():
    las = lasio.examples.open("sample_str_in_data.las", read_policy=[], dtypes=False)
    assert isinstance(las.curves[0].data[0], str)
    assert isinstance(las.curves[1].data[0], str)
    assert isinstance(las.curves[2].data[0], str)
    assert isinstance(las.curves[3].data[0], str)


def test_index_null_issue227():
    las = lasio.examples.open("index_null.las")
    assert las["DEPT"].data[1] == 999.25
    assert numpy.isnan(las["DT"].data[0])


def test_excess_curves():
    las = lasio.examples.open("excess_curves.las")
    assert las.curves.keys() == ["DEPTH", "TVD", "VS", "GAMMA", "ROP", "TEMP"]
    assert las.keys() == ["DEPTH", "TVD", "VS", "GAMMA", "ROP", "TEMP"]
    assert len(las["ROP"]) == 2
    assert numpy.isnan(las["ROP"]).all()
    assert list(las.df().columns) == ["TVD", "VS", "GAMMA", "ROP", "TEMP"]


def test_tab_dlm_normal_engine():
    # GitHub Issue 554
    las = lasio.examples.open("2.0/sample_2.0_tab_dlm.las", engine="normal")
    assert las["DEPT"].data[1] == 1669.875


def test_tab_dlm_numpy_engine():
    # GitHub Issue 554
    las = lasio.examples.open("2.0/sample_2.0_tab_dlm.las", engine="numpy")
    assert las["DEPT"].data[1] == 1669.875
