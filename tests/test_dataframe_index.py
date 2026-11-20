"""DataFrame index naming and LAS round-trip regressions (#463)."""

from io import StringIO

import numpy as np
import pandas as pd
import pytest

import lasio


@pytest.mark.parametrize("method", ["set_data_from_df", "set_data"])
@pytest.mark.parametrize("existing", [None, ("DEPT", "M"), ("TIME", "S")])
def test_unnamed_index_roundtrip(method, existing):
    las = lasio.LASFile()
    if existing is not None:
        las.append_curve(existing[0], [0, 1], unit=existing[1], descr="Index")
        las.append_curve("GR", [1, 2], unit="API", descr="Gamma ray")
    las.other = "Synthetic test note."
    df = pd.DataFrame({"GR": [10.0, np.nan, 30.0]}, index=[100.0, 100.5, 101.0])
    original = df.copy(deep=True)

    getattr(las, method)(df)

    expected_name = existing[0] if existing else "UNKNOWN"
    assert las.curves[0].mnemonic == expected_name
    assert las.curves[0].original_mnemonic == (existing[0] if existing else "")
    assert las.curves[0].unit == (existing[1] if existing else "")
    if existing:
        assert las.curves[0].descr == "Index"
        assert las.curves[1].unit == "API"
        assert las.curves[1].descr == "Gamma ray"
    np.testing.assert_array_equal(las.index, df.index.values)
    np.testing.assert_allclose(las["GR"], df["GR"], equal_nan=True)
    pd.testing.assert_frame_equal(df, original)

    stream = StringIO()
    las.write(stream, version=2.0, wrap=False)
    stream.seek(0)
    restored = lasio.read(stream)
    assert restored.curves[0].mnemonic == expected_name
    assert restored.curves[0].unit == las.curves[0].unit
    assert restored.curves[1].unit == las.curves[1].unit
    assert restored.other.strip() == "Synthetic test note."
    np.testing.assert_array_equal(restored.index, df.index.values)
    np.testing.assert_allclose(restored["GR"], df["GR"], equal_nan=True)


@pytest.mark.parametrize("method", ["set_data_from_df", "set_data"])
@pytest.mark.parametrize("index_name", [None, "DEPTH"])
def test_explicit_names_override_dataframe_index(method, index_name):
    las = lasio.LASFile()
    df = pd.DataFrame({"GR": [10.0, 20.0]}, index=[100.0, 101.0])
    df.index.name = index_name
    getattr(las, method)(df, names=["CUSTOM", "GAMMA"])
    assert las.curves.keys() == ["CUSTOM", "GAMMA"]
    assert df.index.name == index_name
    np.testing.assert_array_equal(las.index, df.index.values)


@pytest.mark.parametrize("method", ["set_data_from_df", "set_data"])
def test_named_index_overrides_existing_curve_name(method):
    las = lasio.LASFile()
    las.append_curve("DEPT", [0, 1], unit="M")
    df = pd.DataFrame({"GR": [10.0, 20.0]}, index=[100.0, 101.0])
    df.index.name = "DEPTH"
    getattr(las, method)(df)
    assert las.curves.keys() == ["DEPTH", "GR"]
    assert las.curves[0].unit == "M"
    assert df.index.name == "DEPTH"
