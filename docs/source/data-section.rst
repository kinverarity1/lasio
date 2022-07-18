Data section
============

Handling text, dates, timestamps, or any non-numeric characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, lasio will attempt to convert each column of the data section
into floating-point numbers. If that fails, as it will for non-numeric
characters, then the column will be returned as text (``str``). The behavour
can be controlled by specifing the data type as either ``int``, ``float`` or
``str`` per column using the ``dtypes`` keyword argument to
:meth:`lasio.LASFile.read`.

See the example ``data_characters.las``:

.. code-block:: none

    ~A TIME       DATE       DEPT ARC_GR_UNC_RT
    00:00:00 01-Jan-20  1500.2435        126.56
    00:00:01 01-Jan-20  1500.3519        126.56

.. code-block:: python

    >>> import lasio.examples
    >>> las = lasio.examples.open("data_characters.las")
    >>> las["TIME"]
    array(['00:00:00', '00:00:01'], dtype='<U32')
    >>> las["DATE"]
    array(['01-Jan-20', '01-Jan-20'], dtype='<U32')
    >>> las["DEPT"]
    array([1500.2435, 1500.3519])
    >>> las["ARC_GR_UNC_RT"]
    array([126.56, 126.56])
    >>> las.df().reset_index().info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2 entries, 0 to 1
    Data columns (total 4 columns):
     #   Column         Non-Null Count  Dtype
    ---  ------         --------------  -----
     0   TIME           2 non-null      object
     1   DATE           2 non-null      object
     2   DEPT           2 non-null      float64
     3   ARC_GR_UNC_RT  2 non-null      float64
    dtypes: float64(2), object(2)
    memory usage: 192.0+ bytes

lasio doesn't yet understand dates and timestamps natively, but you
can do these conversions with pandas:

    >>> las["DATE_DT"] = pd.to_datetime(las["DATE"]).values

Repeated/duplicate curve mnemonics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LAS files don't always have unique mnemonics for each curve, but that
makes it difficult to retrieve curves by their mnemonic! lasio handles this
by appending ``:1``, ``:2``, etc. to the end of repeat/duplicate mnemonics.
For an example, see a LAS file with this ~C section, with "SFLU" duplicated:

.. code-block:: none

    ~CURVE INFORMATION
    #MNEM.UNIT      API CODE      CURVE DESCRIPTION
    #---------    -------------   ------------------------------
    DEPT.M                      :  1  DEPTH
    DT  .US/M     		     :  2  SONIC TRANSIT TIME
    RHOB.K/M3                   :  3  BULK DENSITY
    NPHI.V/V                    :  4   NEUTRON POROSITY
    SFLU.OHMM                   :  5  RXO RESISTIVITY
    SFLU.OHMM                   :  6  SHALLOW RESISTIVITY
    ILM .OHMM                   :  7  MEDIUM RESISTIVITY
    ILD .OHMM                   :  8  DEEP RESISTIVITY

This is represented in the following way:

    >>> import lasio.examples
    >>> las = lasio.examples.open("mnemonic_duplicate.las")
    >>> print(las.curves)
    Mnemonic  Unit  Value  Description
    --------  ----  -----  -----------
    DEPT      M            1  DEPTH
    DT        US/M         2  SONIC TRANSIT TIME
    RHOB      K/M3         3  BULK DENSITY
    NPHI      V/V          4   NEUTRON POROSITY
    SFLU:1    OHMM         5  RXO RESISTIVITY
    SFLU:2    OHMM         6  SHALLOW RESISTIVITY
    ILM       OHMM         7  MEDIUM RESISTIVITY
    ILD       OHMM         8  DEEP RESISTIVITY
    >>> las["SFLU:1"]
    array([123.45, 123.45, 123.45])
    >>> las["SFLU:2"]
    array([125.45, 125.45, 125.45])

Note that the actual mnemonic is not present, to avoid ambiguity about
which curve would be expected to be returned:

.. code-block:: python

    >>> las["SFLU"]

.. code-block:: console

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "C:\devapps\kinverarity\projects\lasio\lasio\las.py", line 661, in __getitem__
        raise KeyError("{} not found in curves ({})".format(key, curve_mnemonics))
    KeyError: "SFLU not found in curves (['DEPT', 'DT', 'RHOB', 'NPHI', 'SFLU:1', 'SFLU:2', 'ILM', 'ILD'])"

Note also that lasio remembers the original mnemonic so that on writing the file
out, the original mnemonics are replicated:

.. code-block:: python

    >>> import sys
    >>> las.write(sys.stdout)
    ...
    ~Curve Information -----------------------------------------
    DEPT.M     : 1  DEPTH
    DT  .US/M  : 2  SONIC TRANSIT TIME
    RHOB.K/M3  : 3  BULK DENSITY
    NPHI.V/V   : 4   NEUTRON POROSITY
    SFLU.OHMM  : 5  RXO RESISTIVITY
    SFLU.OHMM  : 6  SHALLOW RESISTIVITY
    ILM .OHMM  : 7  MEDIUM RESISTIVITY
    ILD .OHMM  : 8  DEEP RESISTIVITY
    ...

Ignoring commented-out lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes data sections have comment line inside them. By default lasio will ignore
any lines starting with the "#" character within the data section. You can
control this using the ``remove_data_line_filter='#'`` argument to
:meth:`lasio.LASFile.read`.

Ignoring the data section
~~~~~~~~~~~~~~~~~~~~~~~~~

Lasio can ignore the data section by setting ignore_data to true:
  ``lasio.read(file, ignore_date=True)``

This will completely skip reading the data section and the returned object will just contain the header metadata section.

A quick way to see the expected column names is:
  ``lasio.read(file, ignore_data=True).keys()``

To re-run without ignore_data: 
  ``lasio.read(file).keys()``

If this returns a different set of columns then there may be a data parsing
error.  In this case, if incorrect parsing causes lasio to create extra columns
they will be named 'UKNOWN:1', 'UNKNOWN:2', 'UNKNOWN:<n>'...  This can usually
be fixed by tuning lasio.read()'s read_policy or null_policy options.

Handling errors with read_policy and null_policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lasio has a flexible way of handling "errors" in the ~ASCII data section to
accommodate how strict or flexible you want to be. The two main tools are 
``read_policy`` and ``null_policy``.  These are optional arguments to
:meth:`lasio.LASFile.read`.  Each defaults to common options which can be
overridden either by other pre-set options or by a list of specific options.
These policy settings are configured in ``lasio/defaults.py``.

By default, ``lasio.read(f)`` runs as if explicitly set to ``lasio.read(f,
read_policy='default', null_policy='common')``.


Examples of policy override syntax
----------------------------------
Change only read_policy with one of the builtin policy sets:
  ``lasio.read(f, read_policy='comma-delimiter')``
Change only null_policy with one of the builtin policy sets:
  ``lasio.read(f, null_policy='aggressive')``
Change both read_policy and null_policy with builtin policies:
  ``lasio.read(f, read_policy='comma-delimiter', null_policy='none')``
Change read_policy with specific policies (found in defaults.py):
  ``lasio.read(f, read_policy=["comma-decimal-mark", "run-on(.)"])``
Change null_policy with your own hard-coded options:
  ``lasio.read(f, null_policy=["9999.25", "999.25", "NA", "INF", "IO", "IND"])``


Example errors
--------------

Here are some examples of errors.

* Files could contain a variety of indicators for an invalid data point other
  than that defined by the NULL line in the LAS header (usually -999.25).

* Fixed-width columns could run into each other:

.. code-block:: none

    7686.500    64.932     0.123     0.395    12.403   156.271    10.649    -0.005   193.223   327.902    -0.023     4.491     2.074    29.652
    7686.000    67.354     0.140     0.415     9.207  4648.011    10.609    -0.004  3778.709  1893.751    -0.048     4.513     2.041   291.910
    7685.500    69.004     0.151     0.412     7.020101130.188    10.560    -0.004 60000.000  2901.317    -0.047     4.492     2.046   310.119
    7685.000    68.809     0.150     0.411     7.330109508.961    10.424    -0.005 60000.000  2846.619    -0.042     4.538     2.049   376.968
    7684.500    68.633     0.149     0.402     7.345116238.453    10.515    -0.005 60000.000  2290.275    -0.051     4.543     2.063   404.972
    7684.000    68.008     0.144     0.386     7.682  4182.679    10.515    -0.004  3085.681  1545.842    -0.046     4.484     2.089   438.195

* Odd text such as ``(null)``:

.. code-block:: none

    8090.00         -999.25         -999.25         -999.25               0               0               0               0               0               0               0               0
    8091.000          0.70          337.70          (null)               0               0               0               0               0               0               0               0
    8092.000        -999.25         -999.25         -999.25               0               0               0               0               0              0               0               0

Handling run-on errors
----------------------

lasio detects and handles these problems by default using ``lasio.read(f,
read_policy='default')``. For example a file with this data section:

.. code-block:: none

    ~A
        7686.000    67.354     0.140     0.415     9.207  4648.011    10.609
        7685.500    69.004     0.151     0.412     7.020101130.188    10.560
        7685.000    68.809     0.150     0.411     7.330-19508.961    10.424
        7684.500    68.633     0.149     0.402     7.345116238.453    10.515
        7684.000    68.008     0.144     0.386     7.682  4182.679    10.515

is loaded by default as the following:

.. code-block:: python

    >>> import lasio.examples
    >>> las = lasio.examples.open('null_policy_runon.las')
    >>> las.data
    array([[7686.0, 67.354, 0.14, 0.415, 9.207, 4648.011, 10.609],
           [7685.5, 69.004, 0.151, 0.412, nan, nan, 10.56],
           [7685.0, 68.809, 0.15, 0.411, 7.33, -19508.961, 10.424],
           [7684.5, 68.633, 0.149, 0.402, nan, nan, 10.515],
           [7684.0, 68.008, 0.144, 0.386, 7.682, 4182.679, 10.515]])

Handling invalid data indicators automatically
----------------------------------------------

These are detected by lasio to a degree which you can control with the
null_policy keyword argument.

You can specify a policy of 'none', 'strict', 'common', 'aggressive', or
'all'. These policies all include a subset of pre-defined substitutions. Or
you can give your own list of substitutions. Here is the list of predefined
policies and substitutions from :mod:`lasio.defaults`.

Policies that you can pick with e.g. ``null_policy='common'``:

.. code-block:: python

    NULL_POLICIES = {
        'none': [],
        'strict': ['NULL', ],
        'common': ['NULL', '(null)', '-',
                   '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND'],
        'aggressive': ['NULL', '(null)', '--',
                       '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND',
                       '999', '999.99', '9999', '9999.99' '2147483647', '32767',
                       '-0.0', ],
        'all': ['NULL', '(null)', '-',
                '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND',
                '999', '999.99', '9999', '9999.99' '2147483647', '32767', '-0.0',
                'numbers-only', ],
        'numbers-only': ['numbers-only', ]
        }

Or substitutions you could specify with e.g. ``null_policy=['NULL', '999.25',
'INF']``:

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

You can also specify substitutions directly. E.g. for a file with this
data section:

.. code-block:: none

    ~A  DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD
    1670.000    9998  2550.000    0.450  123.450  123.450  110.200  105.600
    1669.875    9999  2550.000    0.450  123.450  123.450  110.200  105.600
    1669.750   10000       ERR    0.450  123.450  -999.25  110.200  105.600

By default, it will read all data as a string due to the presence of "ERR":

.. code-block:: python

    >>> las = lasio.examples.open('null_policy_ERR.las')
    >>> las.data
    array([['1670.0', '9998.0', '2550.0', '0.45', '123.45', '123.45',
            '110.2', '105.6'],
           ['1669.875', '9999.0', '2550.0', '0.45', '123.45', '123.45',
            '110.2', '105.6'],
           ['1669.75', '10000.0', 'ERR', '0.45', '123.45', '-999.25',
            '110.2', '105.6']], dtype='<U32')

We can fix it by using an explicit NULL policy.

.. code-block:: python

    >>> las = lasio.examples.open('null_policy_ERR.las', null_policy=[('ERR', ' NaN ')])
    >>> las.data
    array([[ 1.670000e+03,  9.998000e+03,  2.550000e+03,  4.500000e-01,
             1.234500e+02,  1.234500e+02,  1.102000e+02,  1.056000e+02],
           [ 1.669875e+03,  9.999000e+03,  2.550000e+03,  4.500000e-01,
             1.234500e+02,  1.234500e+02,  1.102000e+02,  1.056000e+02],
           [ 1.669750e+03,  1.000000e+04,           nan,  4.500000e-01,
             1.234500e+02, -9.992500e+02,  1.102000e+02,  1.056000e+02]])

See ``tests/test_null_policy.py`` (`link
<https://github.com/kinverarity1/lasio/blob/main/tests/test_null_policy.py>`__)
for some examples.
