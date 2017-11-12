Handling data section errors
============================

``lasio`` has a flexible way of handling "errors" in the ~ASCII data section to
accommodate how strict or flexible you want to be.

Example errors
--------------

Here are some examples of errors.

Fixed-width columns running into each other:

.. highlight:: none

    7690.000    67.930     0.144     0.406     7.491  2312.429    10.386     0.023  3933.536  4697.728    -0.035     4.331     2.056    19.630
    7689.500    67.695     0.142     0.368     8.005  2632.364    10.339     0.017  2748.889  3173.198    -0.046     4.233     2.118    32.280
    7689.000    66.953     0.137     0.286    10.920   500.294    10.388     0.022   524.575   675.178    -0.043     4.100     2.249    41.565
    7688.500    66.035     0.130     0.180    15.736   100.798    10.196     0.035   107.640   144.964    -0.022     3.987     2.420    22.323
    7688.000    64.277     0.118     0.146    22.688    51.593     9.965     0.031    51.131    68.895     0.006     3.957     2.475    22.118
    7687.500    62.832     0.108     0.207    23.239    43.447     9.964     0.016    44.684    62.518     0.047     4.101     2.376    15.425
    7687.000    63.633     0.113     0.322    18.866    59.974    10.659    -0.001    61.304    95.710     0.046     4.325     2.192    23.342
    7686.500    64.932     0.123     0.395    12.403   156.271    10.649    -0.005   193.223   327.902    -0.023     4.491     2.074    29.652
    7686.000    67.354     0.140     0.415     9.207  4648.011    10.609    -0.004  3778.709  1893.751    -0.048     4.513     2.041   291.910
    7685.500    69.004     0.151     0.412     7.020101130.188    10.560    -0.004 60000.000  2901.317    -0.047     4.492     2.046   310.119
    7685.000    68.809     0.150     0.411     7.330109508.961    10.424    -0.005 60000.000  2846.619    -0.042     4.538     2.049   376.968
    7684.500    68.633     0.149     0.402     7.345116238.453    10.515    -0.005 60000.000  2290.275    -0.051     4.543     2.063   404.972
    7684.000    68.008     0.144     0.386     7.682  4182.679    10.515    -0.004  3085.681  1545.842    -0.046     4.484     2.089   438.195
    7683.500    67.695     0.142     0.368     7.859  1340.012    10.555    -0.002  1147.204  1075.280    -0.036     4.382     2.118   330.848

Odd text such as ``(null)``:

8090.000            2.82         -999.25         -999.25         -999.25         -999.25         -999.25               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0             100               0               0               0               0               0               0               0               0               0               0               0               0               0               0           92.17           89.21            1.79            0.80            0.40
8091.000            3.68         -999.25         8090.11            0.70          337.70          (null)               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0             100               0               0               0               0               0               0               0               0               0               0               0               0               0               0           91.67           88.74            1.78            0.80            0.40
8092.000            3.52         -999.25         -999.25         -999.25         -999.25         -999.25               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0               0             100               0               0               0               0               0               0               0               0               0               0               0               0               0               0           91.81           88.87            1.78            0.80            0.40

Often a wide variety of numerical values can also be used as placeholders for invalid values, apart from the NULL value defined in the LAS header section.


This is handled by the keyword arguments ``lasio.read(f, read_policy=..., null_policy=...)``.

These keywords work in two ways:

* You specify a policy, which then includes a variety of substitutions. For
  example there is only one ``read_policy`` of 'default'. There are several
  ``null_policy`` choices: 'none', 'strict', 'common', 'aggressive', or 'all'.

  Each of this policies implements a list of substitutions. See
  :mod:`lasio.defaults` for the list. For example, ``null_policy='common'``
  implements these substitutions:

  ``['NULL', '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND']``

  Each of these substitutions are defined in :``lasio.defaults.NULL_SUBS``.
  They will take one of three forms for now:

  - None - a special value which only applies for the substitution 'NULL' - this
    replaces the value specified by the NULL field in the LAS file header.
  - any numeric value - this will replace the value with ``numpy.nan``.
  - a pair of two strings - used with :func:`re.sub` - the first is a regular
    expression, the second is the string substituted back in. The string
    to be matched against is each line of the LAS file's data section(s).

* Or instead of specifying a policy, you can pass a list of the substitutions
  themselves. In this way you get fine control of what you consider an "error".
  These can be strings referring to pre-defined substitutions from 
  ``lasio.defaults.NULL_SUBS``, numeric values, or pairs of 
  regular expression arguments for :func:`re.sub`.

``read_policy=``
----------------

The primary use of this is to handle "run-on" errors which were often caused by
large values overflowing the width of a fixed-length formatting field:

.. code-block:: none

    150.05   13.2  -945.23   3.12
    150.06   54.8 -1583.01   2.42
    150.07   27.1 -9782.25   4.21
    150.08   89.0-10248.37   1.82
    150.09   35.2 -8871.24   0.14

``read_policy='default'`` (which is the default setting) will use the
substitutions ``'run-on(-)'``, ``'run-on(.)'``, and ``'run-on(NaN.)'`` to fix 
these errors wherever possible. (In the specific example above it will be able
to recover both true values 89.0 and -10248.37, but in other examples they
will be unrecoverable and replaced with ``NaN``.)

``null_policy``
---------------

These are the pre-defined null substitutions:

.. code-block:: python

    NULL_SUBS = {
        'NULL': [None, ],                       # special case to be handled
        '999.25': [-999.25, 999.25],
        '9999.25': [-9999.25, 9999.25],
        '999.99': [-999.99, 999.99],
        '9999.99': [-9999.99, 9999.99],
        '999': [-999, 999],
        '9999': [-9999, 9999],
        '2147483647': [-2147483647, 2147483647],
        '32767': [-32767, 32767],
        'NA': [(re.compile(r'(#N/A)[ ]'), ' NaN '),
               (re.compile(r'[ ](#N/A)'), ' NaN '), ],
        'INF': [(re.compile(r'(-?1\.#INF)[ ]'), ' NaN '),
                (re.compile(r'[ ](-?1\.#INF)'), ' NaN '), ],
        'IO': [(re.compile(r'(-?1\.#IO)[ ]'), ' NaN '),
               (re.compile(r'[ ](-?1\.#IO)'), ' NaN '), ],
        'IND': [(re.compile(r'(-?1\.#IND)[ ]'), ' NaN '),
                (re.compile(r'[ ](-?1\.#IND)'), ' NaN '), ],
        '-0.0': [(re.compile(r'(-?0\.0+)[ ]'), ' NaN '),
                 (re.compile(r'[ ](-?0\.0+)'), ' NaN '), ],
        'numbers-only': [(re.compile(r'([^ 0-9.\-+]+)[ ]'), ' NaN '),
                         (re.compile(r'[ ]([^ 0-9.\-+]+)'), ' NaN '), ],
        }

As described above, you don't actually need to specify these individually
unless you want to. These are the predefined policies that you can pass easily
as e.g. ``lasio.read(f, null_policy='strict')``. See:

.. code-block:: python

    NULL_POLICIES = {
        'none': [],
        'strict': ['NULL', ],
        'common': ['NULL', 
                   '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND'],
        'aggressive': ['NULL',
                       '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND', 
                       '999', '999.99', '9999', '9999.99' '2147483647', '32767',
                       '-0.0', ],
        'all': ['NULL',
                '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND', 
                '999', '999.99', '9999', '9999.99' '2147483647', '32767', '-0.0', 
                'numbers-only', ]
        }

See ``tests/test_null_policy.py`` (`link <>`__) for more examples.