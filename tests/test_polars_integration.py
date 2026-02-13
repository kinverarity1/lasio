"""Test polars integration functionality."""

import numpy as np
import pytest

import lasio


class TestPolarsIntegration:
    """Test polars DataFrame integration."""

    def test_pl_method_import_error(self):
        """Test that pl() method raises ImportError when polars is not available."""
        # Create a simple LAS file
        las = lasio.LASFile()
        las.append_curve("DEPT", [100, 101, 102])
        las.append_curve("GR", [25, 30, 35])
        
        # Mock the import to fail
        import sys
        from unittest.mock import patch
        
        with patch.dict(sys.modules, {"polars": None}):
            with pytest.raises(ImportError, match="polars is required"):
                las.pl()

    def test_pl_method_basic(self):
        """Test basic polars DataFrame creation."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create a simple LAS file
        las = lasio.LASFile()
        las.append_curve("DEPT", [100, 101, 102])
        las.append_curve("GR", [25, 30, 35])
        las.append_curve("NPHI", [0.15, 0.18, 0.20])
        
        # Convert to polars DataFrame
        df = las.pl()
        
        # Check that it's a polars DataFrame
        assert isinstance(df, pl.DataFrame)
        
        # Check columns
        expected_cols = ["DEPT", "GR", "NPHI"]
        assert list(df.columns) == expected_cols
        
        # Check data
        assert df.shape == (3, 3)
        assert df["DEPT"].to_list() == [100, 101, 102]
        assert df["GR"].to_list() == [25, 30, 35]
        assert df["NPHI"].to_list() == [0.15, 0.18, 0.20]

    def test_set_data_from_pl_basic(self):
        """Test setting data from polars DataFrame."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create a polars DataFrame
        df = pl.DataFrame({
            "DEPT": [100, 101, 102],
            "GR": [25, 30, 35],
            "NPHI": [0.15, 0.18, 0.20]
        })
        
        # Create LAS file and set data
        las = lasio.LASFile()
        las.set_data_from_pl(df)
        
        # Check that data was set correctly
        assert len(las.curves) == 3
        assert las.curves[0].mnemonic == "DEPT"
        assert las.curves[1].mnemonic == "GR"
        assert las.curves[2].mnemonic == "NPHI"
        
        assert np.array_equal(las.curves[0].data, np.array([100, 101, 102]))
        assert np.array_equal(las.curves[1].data, np.array([25, 30, 35]))
        assert np.array_equal(las.curves[2].data, np.array([0.15, 0.18, 0.20]))

    def test_set_data_from_pl_with_names(self):
        """Test setting data from polars DataFrame with custom names."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create a polars DataFrame
        df = pl.DataFrame({
            "col1": [100, 101, 102],
            "col2": [25, 30, 35],
            "col3": [0.15, 0.18, 0.20]
        })
        
        # Create LAS file and set data with custom names
        las = lasio.LASFile()
        las.set_data_from_pl(df, names=["DEPTH", "GAMMA", "NEUTRON"])
        
        # Check that data was set correctly with custom names
        assert len(las.curves) == 3
        assert las.curves[0].mnemonic == "DEPTH"
        assert las.curves[1].mnemonic == "GAMMA"
        assert las.curves[2].mnemonic == "NEUTRON"

    def test_set_data_polars_dataframe(self):
        """Test that set_data handles polars DataFrames correctly."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create a polars DataFrame
        df = pl.DataFrame({
            "DEPT": [100, 101, 102],
            "GR": [25, 30, 35]
        })
        
        # Create LAS file and set data using set_data
        las = lasio.LASFile()
        las.set_data(df)
        
        # Check that data was set correctly
        assert len(las.curves) == 2
        assert las.curves[0].mnemonic == "DEPT"
        assert las.curves[1].mnemonic == "GR"

    def test_pl_vs_df_consistency(self):
        """Test that pl() and df() methods produce consistent results."""
        try:
            import polars as pl
            import pandas as pd
        except ImportError:
            pytest.skip("polars or pandas not available")
        
        # Create a simple LAS file
        las = lasio.LASFile()
        las.append_curve("DEPT", [100, 101, 102])
        las.append_curve("GR", [25, 30, 35])
        las.append_curve("NPHI", [0.15, 0.18, 0.20])
        
        # Get both pandas and polars DataFrames
        df_pandas = las.df()
        df_polars = las.pl()
        
        # Check that data is consistent
        assert df_pandas.shape == df_polars.shape
        
        # Check column names (pandas will have index, polars won't)
        pandas_cols = list(df_pandas.columns)
        polars_cols = list(df_polars.columns)
        assert pandas_cols == polars_cols
        
        # Check data values
        for col in pandas_cols:
            pandas_values = df_pandas[col].values
            polars_values = df_polars[col].to_numpy()
            np.testing.assert_array_equal(pandas_values, polars_values)

    def test_pl_method_empty_curves(self):
        """Test pl() method with empty curves."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create LAS file with no curves
        las = lasio.LASFile()
        
        # Convert to polars DataFrame
        df = las.pl()
        
        # Should return empty DataFrame
        assert isinstance(df, pl.DataFrame)
        assert df.shape == (0, 0)

    def test_set_data_from_pl_type_error(self):
        """Test that set_data_from_pl raises TypeError for non-polars DataFrames."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not available")
        
        # Create a regular list instead of polars DataFrame
        data = [[100, 25], [101, 30], [102, 35]]
        
        las = lasio.LASFile()
        with pytest.raises(TypeError, match="df must be a polars.DataFrame"):
            las.set_data_from_pl(data) 