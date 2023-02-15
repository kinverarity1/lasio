"""Should be in test_write"""

import pytest

import os

import lasio

from test_write import egfn

import numpy as np

def test_write_changed_file(tmp_path):
    las = lasio.read(egfn("logging_levels.las"))

    df = las.df()
    new_df = df.drop([df.index[-1]])

    assert len(new_df) + 1 == len(df)

    las.set_data_from_df(new_df)

    out_file = str(tmp_path / "logging_levels_clipped.las")

    las.write(out_file)

    las2 = lasio.read(out_file)

    assert np.allclose(new_df, las2.df(), equal_nan=True)
