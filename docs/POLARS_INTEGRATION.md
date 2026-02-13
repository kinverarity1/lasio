# Polars Integration for lasio

This pull request adds support for [Polars](https://polars.rs/) DataFrames in lasio, providing high-performance data manipulation capabilities for well log data.

## Features Added

### 1. `LASFile.pl()` Method
Convert LAS file data to a Polars DataFrame:

```python
import lasio
import polars as pl

# Read a LAS file
las = lasio.read("well_data.las")

# Convert to Polars DataFrame
df = las.pl()
print(df)
```

### 2. `LASFile.set_data_from_pl()` Method
Create LAS files from Polars DataFrames:

```python
import polars as pl
import lasio

# Create a Polars DataFrame
df = pl.DataFrame({
    "DEPT": [100, 101, 102, 103, 104],
    "GR": [25, 30, 35, 40, 45],
    "NPHI": [0.15, 0.18, 0.20, 0.22, 0.25],
    "RHOB": [2.65, 2.68, 2.70, 2.72, 2.75]
})

# Create LAS file from DataFrame
las = lasio.LASFile()
las.set_data_from_pl(df)

# Add header information
las.well.WELL = "Example Well"
las.well.COMP = "Example Company"

# Write to file
las.write("example_well.las")
```

### 3. Enhanced `set_data()` Method
The existing `set_data()` method now automatically detects and handles Polars DataFrames:

```python
las = lasio.LASFile()
las.set_data(df)  # Automatically detects polars DataFrame
```

## Installation

Polars is included as an optional dependency. Install it with:

```bash
pip install polars
```

Or install lasio with all optional dependencies:

```bash
pip install lasio[all]
```

## Performance Benefits

Polars is designed for high-performance data manipulation and can be significantly faster than pandas for large datasets. Key benefits include:

- **Memory efficiency**: Polars uses Apache Arrow for memory layout
- **Lazy evaluation**: Operations are optimized and executed efficiently
- **Rust backend**: Fast, safe, and concurrent data processing
- **Type safety**: Strong typing prevents runtime errors

## Error Handling

If Polars is not installed, the methods will raise a helpful ImportError:

```python
try:
    df = las.pl()
except ImportError as e:
    print("Install polars: pip install polars")
```

## Testing

Comprehensive tests are included in `tests/test_polars_integration.py` covering:

- Basic DataFrame conversion
- Data creation from Polars DataFrames
- Error handling for missing dependencies
- Consistency with pandas integration
- Edge cases (empty data, type errors)

## Documentation

Full documentation is available in `docs/source/polars.rst` with examples and performance comparisons.

## Backward Compatibility

This integration is fully backward compatible:
- Existing pandas functionality remains unchanged
- Polars is an optional dependency
- No breaking changes to existing APIs

## Files Modified

- `lasio/las.py`: Added `pl()` and `set_data_from_pl()` methods
- `pyproject.toml`: Added polars to optional dependencies
- `tests/test_polars_integration.py`: Comprehensive test suite
- `docs/source/polars.rst`: Complete documentation
- `docs/source/index.rst`: Added polars to documentation index

## Example Usage

```python
import lasio
import polars as pl

# Read LAS file and convert to Polars
las = lasio.read("well_data.las")
df = las.pl()

# High-performance operations
filtered = df.filter(pl.col("DEPT") > 1000)
stats = df.select([
    pl.col("GR").mean().alias("GR_mean"),
    pl.col("NPHI").std().alias("NPHI_std")
])

# Create new LAS file from processed data
new_las = lasio.LASFile()
new_las.set_data_from_pl(filtered)
new_las.write("filtered_well.las")
```

This integration provides geoscientists with a powerful, high-performance alternative to pandas for well log data analysis while maintaining full compatibility with existing lasio workflows. 