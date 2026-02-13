#!/usr/bin/env python3
"""Simple test script for polars integration."""

import sys
import os

# Add the lasio package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lasio'))

def test_polars_integration():
    """Test basic polars integration functionality."""
    print("Testing polars integration...")
    
    # Test import
    try:
        import lasio
        print("✓ lasio imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import lasio: {e}")
        return False
    
    # Test polars import
    try:
        import polars as pl
        print("✓ polars imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import polars: {e}")
        print("  Install polars with: pip install polars")
        return False
    
    # Test basic functionality
    try:
        # Create a simple LAS file
        las = lasio.LASFile()
        las.append_curve("DEPT", [100, 101, 102])
        las.append_curve("GR", [25, 30, 35])
        las.append_curve("NPHI", [0.15, 0.18, 0.20])
        print("✓ Created LAS file with curves")
        
        # Test pl() method
        df = las.pl()
        print(f"✓ Created polars DataFrame: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Test set_data_from_pl method
        new_df = pl.DataFrame({
            "DEPT": [200, 201, 202],
            "GR": [40, 45, 50],
            "NPHI": [0.25, 0.28, 0.30]
        })
        
        las2 = lasio.LASFile()
        las2.set_data_from_pl(new_df)
        print("✓ Created LAS file from polars DataFrame")
        print(f"  Curves: {[c.mnemonic for c in las2.curves]}")
        
        # Test set_data with polars DataFrame
        las3 = lasio.LASFile()
        las3.set_data(new_df)
        print("✓ Used set_data with polars DataFrame")
        print(f"  Curves: {[c.mnemonic for c in las3.curves]}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_polars_integration()
    if success:
        print("\n🎉 All tests passed! Polars integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 