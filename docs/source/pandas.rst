Integration with pandas.DataFrame
=================================

The :meth:`lasio.LASFile.df` method converts the LAS data to a
:class:`pandas.DataFrame`.

Any changes that you make to the DataFrame can be brought back into the
LASFile object with :meth:`lasio.LASFile.set_data`.

.. code-block:: ipython

    In [168]: las = lasio.read('tests/examples/6038187_v1.2.las')

    In [169]: df = las.df()

There are some summary methods handy for data exploration:

.. code-block:: ipython

    In [170]: df.head(10)
    Out[170]:
            CALI   DFAR  DNEAR     GAMN  NEUT       PR     SP     COND
    DEPT
    0.05  49.765  4.587  3.382      NaN   NaN      NaN    NaN      NaN
    0.10  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.15  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.20  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.25  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.30  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.35  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.40  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.45  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998
    0.50  49.765  4.587  3.382 -2324.28   NaN  115.508 -3.049 -116.998

    In [171]: df.tail(40)
    Out[171]:
               CALI   DFAR  DNEAR     GAMN   NEUT       PR     SP     COND
    DEPT
    134.65  100.983  1.563  1.357 -2324.28  158.0  115.508 -3.049  578.643
    134.70  100.833  1.570  1.357      NaN    NaN      NaN    NaN  571.233
    134.75   93.760  1.582  1.378      NaN    NaN      NaN    NaN  565.552
    134.80   88.086  1.561  1.361      NaN    NaN      NaN    NaN  570.490
    134.85   86.443  1.516  1.338      NaN    NaN      NaN    NaN  574.937
    134.90   79.617  5.989  1.356      NaN    NaN      NaN    NaN  579.137
    134.95   65.236  4.587  1.397      NaN    NaN      NaN    NaN      NaN
    135.00   55.833  4.587  1.351      NaN    NaN      NaN    NaN      NaN
    135.05   49.061  4.587  1.329      NaN    NaN      NaN    NaN      NaN
    135.10   49.036    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.15   49.024    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.20   49.005    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.25   48.999    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.30   48.987    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.35   48.980    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.40   48.962    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.45   48.962    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.50   48.925    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.55   48.931    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.60   48.919    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.65   48.900    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.70   48.882    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.75   48.863    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.80   48.857    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.85   48.839    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.90   48.808    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    135.95   48.802    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.00   48.789    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.05   48.771    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.10   48.765    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.15   48.752    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.20   48.734    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.25   48.684    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.30   48.666    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.35   48.647    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.40   48.604    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.45   48.555    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.50   48.555    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.55   48.438    NaN    NaN      NaN    NaN      NaN    NaN      NaN
    136.60  -56.275    NaN    NaN      NaN    NaN      NaN    NaN      NaN

    In [172]: df.describe()
    Out[172]:
                  CALI         DFAR        DNEAR         GAMN         NEUT  \
    count  2732.000000  2701.000000  2701.000000  2691.000000  2492.000000
    mean     97.432002     1.767922     1.729209  -102.330033   441.600013
    std      13.939547     0.480333     0.372412   630.106420   370.138208
    min     -56.275000     0.725000     0.657001 -2324.280000    81.001800
    25%     101.077500     1.526000     1.535000    55.783000   158.002000
    50%     101.426000     1.758000     1.785000    74.376900   256.501500
    75%     101.582000     1.993000     1.948000    88.326900   680.500250
    max     103.380000     5.989000     3.382000   169.672000  1665.990000

                     PR           SP         COND
    count   2692.000000  2692.000000  2697.000000
    mean   17940.522307    90.393464   478.670791
    std    22089.297212    26.725547   753.869866
    min      115.508000    -3.049000  -116.998000
    25%     2652.470000    93.495500   200.981000
    50%     2709.345000    99.994000   266.435000
    75%    50499.900000   100.623000   505.530000
    max    50499.900000   102.902000  4978.160000

There's obviously a problem with the GAMN log: -2324.28 is not a valid value.
Let's fix that.

.. code-block:: ipython

    In [44]: import numpy as np

    In [173]: df['GAMN'][df['GAMN'] == -2324.28] = np.nan

    In [174]: df.describe()['GAMN']
    Out[174]:
    count    2491.000000
    mean       76.068198
    std        23.120160
    min        13.946000
    25%        60.434100
    50%        76.700700
    75%        90.647500
    max       169.672000
    Name: GAMN, dtype: float64

Let's create a new log with the moving average of the GAMN log, over
1 m. This is easy enough to do with the pandas :meth:`pandas.Series.rolling`
method and the LAS file's STEP value:

.. code-block:: ipython

    In [175]: df['GAMN_avg'] = df['GAMN'].rolling(int(1 / las.well.STEP.value), center=True).mean()

Now we want to apply this DataFrame ``df`` back to the ``las`` LASFile object,
and check that it's all there:

.. code-block:: ipython

    In [176]: las.set_data(df)

    In [177]: las.curves
    Out[177]:
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=DEPTH, original_mnemonic=DEPT, data.shape=(2732,)),
     CurveItem(mnemonic=CALI, unit=MM, value=, descr=CALI, original_mnemonic=CALI, data.shape=(2732,)),
     CurveItem(mnemonic=DFAR, unit=G/CM3, value=, descr=DFAR, original_mnemonic=DFAR, data.shape=(2732,)),
     CurveItem(mnemonic=DNEAR, unit=G/CM3, value=, descr=DNEAR, original_mnemonic=DNEAR, data.shape=(2732,)),
     CurveItem(mnemonic=GAMN, unit=GAPI, value=, descr=GAMN, original_mnemonic=GAMN, data.shape=(2732,)),
     CurveItem(mnemonic=NEUT, unit=CPS, value=, descr=NEUT, original_mnemonic=NEUT, data.shape=(2732,)),
     CurveItem(mnemonic=PR, unit=OHM/M, value=, descr=PR, original_mnemonic=PR, data.shape=(2732,)),
     CurveItem(mnemonic=SP, unit=MV, value=, descr=SP, original_mnemonic=SP, data.shape=(2732,)),
     CurveItem(mnemonic=COND, unit=MS/M, value=, descr=COND, original_mnemonic=COND, data.shape=(2732,)),
     CurveItem(mnemonic=GAMN_avg, unit=, value=, descr=, original_mnemonic=GAMN_avg, data.shape=(2732,))]

    In [178]: las.df().describe()
    Out[178]:
                  CALI         DFAR        DNEAR         GAMN         NEUT  \
    count  2732.000000  2701.000000  2701.000000  2491.000000  2492.000000
    mean     97.432002     1.767922     1.729209    76.068198   441.600013
    std      13.939547     0.480333     0.372412    23.120160   370.138208
    min     -56.275000     0.725000     0.657001    13.946000    81.001800
    25%     101.077500     1.526000     1.535000    60.434100   158.002000
    50%     101.426000     1.758000     1.785000    76.700700   256.501500
    75%     101.582000     1.993000     1.948000    90.647500   680.500250
    max     103.380000     5.989000     3.382000   169.672000  1665.990000

                     PR           SP         COND     GAMN_avg
    count   2692.000000  2692.000000  2697.000000  2472.000000
    mean   17940.522307    90.393464   478.670791    76.326075
    std    22089.297212    26.725547   753.869866    18.208038
    min      115.508000    -3.049000  -116.998000    24.753655
    25%     2652.470000    93.495500   200.981000    64.848379
    50%     2709.345000    99.994000   266.435000    77.747517
    75%    50499.900000   100.623000   505.530000    88.323376
    max    50499.900000   102.902000  4978.160000   120.049300

All good, the new curve is in there.

See the `pandas documentation <http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe>`__
for more information!