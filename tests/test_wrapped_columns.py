"""Regression tests for wrapped records with equally sized physical lines."""

from io import StringIO

import numpy as np
import pytest

import lasio


def make_las(version, wrap, n_curves, values, width):
    header = [
        "~Version",
        f"VERS. {version} : LAS version",
        f"WRAP. {wrap} : wrapping",
        "~Well",
        "STRT.M 1000 : start",
        "STOP.M 1002 : stop",
        "STEP.M 1 : step",
        "NULL. -999.25 : null",
        "~Curve",
        "DEPT.M : depth",
    ]
    header += [f"C{i}.V : synthetic curve {i}" for i in range(1, n_curves)]
    header += ["~ASCII"]
    lines = []
    for row in values:
        for start in range(0, len(row), width):
            lines.append(" ".join(str(v) for v in row[start : start + width]))
    return "\n".join(header + lines) + "\n"


@pytest.mark.parametrize("version", ["1.2", "2.0"])
@pytest.mark.parametrize("n_curves,width", [(6, 3), (8, 2), (56, 8)])
@pytest.mark.parametrize("recommendations", [True, False])
def test_equal_width_wrapped_records(version, n_curves, width, recommendations):
    values = np.arange(3 * n_curves, dtype=float).reshape(3, n_curves)
    values[:, 0] = [1000, 1001, 1002]
    values[0, -1] = -999.25
    values[1, -1] = -12.5
    las = lasio.read(
        StringIO(make_las(version, "YES", n_curves, values, width)),
        accept_regexp_sub_recommendations=recommendations,
    )
    expected = values.copy()
    expected[0, -1] = np.nan
    np.testing.assert_allclose(las.data, expected, equal_nan=True)
    assert las.curves[0].mnemonic == "DEPT"
    assert las.curves[0].unit == "M"
    assert las.curves[-1].mnemonic == f"C{n_curves - 1}"


@pytest.mark.parametrize("wrap,width", [("YES", 4), ("YES", 6), ("NO", 6)])
def test_other_record_layouts(wrap, width):
    values = np.arange(18, dtype=float).reshape(3, 6)
    values[:, 0] = [1000, 1001, 1002]
    las = lasio.read(StringIO(make_las("2.0", wrap, 6, values, width)))
    np.testing.assert_allclose(las.data, values)


def test_unwrapped_missing_curves_are_not_combined_into_records():
    values = np.array([[1000.0, 1.0, 2.0], [1001.0, 3.0, 4.0], [1002.0, 5.0, 6.0]])
    las = lasio.read(StringIO(make_las("2.0", "NO", 6, values, 3)))
    np.testing.assert_allclose(las.data[:, :3], values)
    assert len(las.index) == 3
