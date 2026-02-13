Integration with polars.DataFrame
=================================

The :meth:`lasio.LASFile.pl` method converts the LAS data to a
:class:`polars.DataFrame`. The first curve in the LAS file is used
for the dataframe's index. See below for an example using this LAS file:

.. code-block::

    ~CURVE INFORMATION
    DEPT.M                   :DEPTH
    CALI.MM                  :CALI
    DFAR.G/CM3               :DFAR
    DNEAR.G/CM3              :DNEAR
    GAMN.GAPI                :GAMN
    NEUT.CPS                 :NEUT
    PR.OHM/M                 :PR
    SP.MV                    :SP
    COND.MS/M                :COND
    ...
    ~A   DEPT[M]        CALI        DFAR       DNEAR        GAMN        NEUT          PR          SP        COND
        0.050000     49.7650     4.58700     3.38200    -99999.0    -99999.0    -99999.0    -99999.0    -99999.0
        0.100000     49.7650     4.58700     3.38200    -2324.28    -99999.0     115.508    -3.04900    -116.998
        0.150000     49.7650     4.58700     3.38200    -2324.28    -99999.0     115.508    -3.04900    -116.998

.. code-block:: python

    >>> import lasio.examples
    >>> las = lasio.examples.open('6038187_v1.2.las')
    >>> df = las.pl()
    >>> print(df)
    shape: (2732, 9)
    ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
    │ DEPT    ┆ CALI    ┆ DFAR    ┆ DNEAR   ┆ GAMN    ┆ NEUT    ┆ PR      ┆ SP      ┆ COND    │
    │ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
    │ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     │
    ╞═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
    │ 0.05    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 0.1     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.15    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.2     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ …       ┆ …       ┆ …       ┆ …       ┆ …       ┆ …       ┆ …       ┆ …       ┆ …       │
    │ 136.4   ┆ 48.604  ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 136.45  ┆ 48.555  ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 136.5   ┆ 48.555  ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 136.55  ┆ 48.438  ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 136.6   ┆ -56.275 ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Polars provides excellent performance for data manipulation and analysis. Here are some useful operations:

.. code-block:: python

    >>> # Get the first 10 rows
    >>> df.head(10)
    shape: (10, 9)
    ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
    │ DEPT    ┆ CALI    ┆ DFAR    ┆ DNEAR   ┆ GAMN    ┆ NEUT    ┆ PR      ┆ SP      ┆ COND    │
    │ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
    │ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     │
    ╞═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
    │ 0.05    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ null    ┆ null    ┆ null    ┆ null    ┆ null    │
    │ 0.1     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.15    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.2     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.25    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.3     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.35    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.4     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.45    ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    │ 0.5     ┆ 49.765  ┆ 4.587   ┆ 3.382   ┆ -2324.28┆ null    ┆ 115.508 ┆ -3.049  ┆ -116.998│
    └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

    >>> # Filter data based on depth
    >>> filtered_df = df.filter(pl.col("DEPT") > 100)
    >>> print(f"Filtered data shape: {filtered_df.shape}")
    Filtered data shape: (1464, 9)

    >>> # Calculate statistics
    >>> stats = df.select([
    ...     pl.col("CALI").mean().alias("CALI_mean"),
    ...     pl.col("GAMN").mean().alias("GAMN_mean"),
    ...     pl.col("PR").mean().alias("PR_mean")
    ... ])
    >>> print(stats)
    shape: (1, 3)
    ┌──────────┬──────────┬──────────┐
    │ CALI_mean┆ GAMN_mean┆ PR_mean  │
    │ ---      ┆ ---      ┆ ---      │
    │ f64      ┆ f64      ┆ f64      │
    ╞══════════╪══════════╪══════════╡
    │ 49.765   ┆ -2324.28 ┆ 115.508  │
    └──────────┴──────────┴──────────┘

Creating LAS files from polars DataFrames
----------------------------------------

You can also create LAS files from polars DataFrames using the :meth:`lasio.LASFile.set_data_from_pl` method:

.. code-block:: python

    >>> import polars as pl
    >>> import lasio
    
    >>> # Create a polars DataFrame
    >>> df = pl.DataFrame({
    ...     "DEPT": [100, 101, 102, 103, 104],
    ...     "GR": [25, 30, 35, 40, 45],
    ...     "NPHI": [0.15, 0.18, 0.20, 0.22, 0.25],
    ...     "RHOB": [2.65, 2.68, 2.70, 2.72, 2.75]
    ... })
    
    >>> # Create a new LAS file
    >>> las = lasio.LASFile()
    
    >>> # Set the data from the polars DataFrame
    >>> las.set_data_from_pl(df)
    
    >>> # Add header information
    >>> las.well.WELL = "Example Well"
    >>> las.well.COMP = "Example Company"
    >>> las.well.LOC = "Example Location"
    
    >>> # Add curve information
    >>> las.curves[0].unit = "M"
    >>> las.curves[0].descr = "Depth"
    >>> las.curves[1].unit = "GAPI"
    >>> las.curves[1].descr = "Gamma Ray"
    >>> las.curves[2].unit = "V/V"
    >>> las.curves[2].descr = "Neutron Porosity"
    >>> las.curves[3].unit = "G/CM3"
    >>> las.curves[3].descr = "Bulk Density"
    
    >>> # Write to file
    >>> las.write("example_well.las")

You can also use the :meth:`lasio.LASFile.set_data` method directly with a polars DataFrame:

.. code-block:: python

    >>> las = lasio.LASFile()
    >>> las.set_data(df)  # polars DataFrame is automatically detected
    >>> print(las.curves)
    [CurveItem(mnemonic=DEPT, unit=, value=, descr=, original_mnemonic=DEPT, data.shape=(5,)),
     CurveItem(mnemonic=GR, unit=, value=, descr=, original_mnemonic=GR, data.shape=(5,)),
     CurveItem(mnemonic=NPHI, unit=, value=, descr=, original_mnemonic=NPHI, data.shape=(5,)),
     CurveItem(mnemonic=RHOB, unit=, value=, descr=, original_mnemonic=RHOB, data.shape=(5,))]

Performance Comparison
---------------------

Polars is designed for high-performance data manipulation and can be significantly faster than pandas for large datasets. Here's a simple comparison:

.. code-block:: python

    >>> import time
    >>> import lasio.examples
    
    >>> las = lasio.examples.open('6038187_v1.2.las')
    
    >>> # Time pandas conversion
    >>> start_time = time.time()
    >>> df_pandas = las.df()
    >>> pandas_time = time.time() - start_time
    
    >>> # Time polars conversion
    >>> start_time = time.time()
    >>> df_polars = las.pl()
    >>> polars_time = time.time() - start_time
    
    >>> print(f"Pandas conversion time: {pandas_time:.4f} seconds")
    >>> print(f"Polars conversion time: {polars_time:.4f} seconds")
    >>> print(f"Polars is {pandas_time/polars_time:.1f}x faster")

Installation
-----------

To use polars integration, install polars:

.. code-block:: bash

    pip install polars

Or install lasio with all optional dependencies:

.. code-block:: bash

    pip install lasio[all]

Note that polars is an optional dependency, so if it's not installed, the :meth:`lasio.LASFile.pl` and :meth:`lasio.LASFile.set_data_from_pl` methods will raise an ImportError with instructions to install polars. 