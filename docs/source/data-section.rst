Data section
============

Handling errors
~~~~~~~~~~~~~~~

``lasio`` has a flexible way of handling "errors" in the ~ASCII data section to
accommodate how strict or flexible you want to be.

Example errors
--------------

Here are some examples of errors.

* Files could contain a variety of indicators for an invalid data point other than that defined by
the NULL line in the LAS header (usually -999.25).

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

lasio detects and handles these problems by default using ``lasio.read(f, read_policy='default')``.
For example a file with this data section:

.. code-block:: none

    ~A
        7686.000    67.354     0.140     0.415     9.207  4648.011    10.609   
        7685.500    69.004     0.151     0.412     7.020101130.188    10.560   
        7685.000    68.809     0.150     0.411     7.330-19508.961    10.424   
        7684.500    68.633     0.149     0.402     7.345116238.453    10.515   
        7684.000    68.008     0.144     0.386     7.682  4182.679    10.515   

is loaded by default as the following:

.. code-block:: ipython

    In [9]: las = lasio.read('tests/examples/null_policy_runon.las')

    In [12]: las.data
    Out[12]:
    array([[7686.0, 67.354, 0.14, 0.415, 9.207, 4648.011, 10.609],
           [7685.5, 69.004, 0.151, 0.412, nan, nan, 10.56],
           [7685.0, 68.809, 0.15, 0.411, 7.33, -19508.961, 10.424],
           [7684.5, 68.633, 0.149, 0.402, nan, nan, 10.515],
           [7684.0, 68.008, 0.144, 0.386, 7.682, 4182.679, 10.515]])

Handling invalid data indicators automatically
----------------------------------------------

These are detected by lasio to a degree which you can control with the
null_policy keyword argument.

You can specify a policy of 'none', 'strict', 'common', 'aggressive', 
or 'all'. These policies all include a subset of pre-defined substitutions.
Or you can give your own list of substitutions. Here is the list of
predefined policies and substitutions from :mod:`lasio.defaults`.

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

Or substitutions you could specify with e.g. ``null_policy=['NULL', '999.25', 'INF']``:

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

Ordinarily it would raise an exception:

.. code-block:: ipython

    In [13]: las = lasio.read('tests/examples/null_policy_ERR.las')
    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
    ~\Code\lasio\lasio\reader.py in read_file_contents(file_obj, regexp_subs, value_null_subs, ignore_data)
        271                 try:
    --> 272                     data = read_data_section_iterative(file_obj, regexp_subs, value_null_subs)
        273                 except:

    ~\Code\lasio\lasio\reader.py in read_data_section_iterative(file_obj, regexp_subs, value_null_subs)
        348
    --> 349     array = np.fromiter(items(file_obj), np.float64, -1)
        350     for value in value_null_subs:

    ValueError: could not convert string to float: 'ERR'

    During handling of the above exception, another exception occurred:

    LASDataError                              Traceback (most recent call last)
    <ipython-input-13-0cb27623119d> in <module>()
    ----> 1 las = lasio.read('tests/examples/null_policy_ERR.las')

    ~\Code\lasio\lasio\__init__.py in read(file_ref, **kwargs)
         41
         42     '''
    ---> 43     return LASFile(file_ref, **kwargs)

    ~\Code\lasio\lasio\las.py in __init__(self, file_ref, **read_kwargs)
         76
         77         if not (file_ref is None):
    ---> 78             self.read(file_ref, **read_kwargs)
         79
         80     def read(self, file_ref,

    ~\Code\lasio\lasio\las.py in read(self, file_ref, ignore_data, read_policy, null_policy, ignore_header_errors, **kwargs)
        106
        107         self.raw_sections = reader.read_file_contents(
    --> 108             file_obj, regexp_subs, value_null_subs, ignore_data=ignore_data, )
        109
        110         if hasattr(file_obj, "close"):

    ~\Code\lasio\lasio\reader.py in read_file_contents(file_obj, regexp_subs, value_null_subs, ignore_data)
        274                     raise exceptions.LASDataError(
        275                         traceback.format_exc()[:-1] +
    --> 276                         ' in data section beginning line {}'.format(i + 1))
        277                 sections[line] = {
        278                     "section_type": "data",

    LASDataError: Traceback (most recent call last):
      File "C:\Users\kent\Code\lasio\lasio\reader.py", line 272, in read_file_contents
        data = read_data_section_iterative(file_obj, regexp_subs, value_null_subs)
      File "C:\Users\kent\Code\lasio\lasio\reader.py", line 349, in read_data_section_iterative
        array = np.fromiter(items(file_obj), np.float64, -1)
    ValueError: could not convert string to float: 'ERR' in data section beginning line 43

But if we specify the regular expression to use with :func:`re.sub`, we can
easily load it:

.. code-block:: ipython

    In [14]: las = lasio.read('tests/examples/null_policy_ERR.las', null_policy=[('ERR', ' NaN '), ])

    In [16]: las.data
    Out[16]:
    array([[1670.0, 9998.0, 2550.0, 0.45, 123.45, 123.45, 110.2, 105.6],
           [1669.875, 9999.0, 2550.0, 0.45, 123.45, 123.45, 110.2, 105.6],
           [1669.75, 10000.0, nan, 0.45, 123.45, -999.25, 110.2, 105.6]])

    In [17]:

See ``tests/test_null_policy.py`` (`link <https://github.com/kinverarity1/lasio/blob/master/tests/test_null_policy.py>`__) for some examples.