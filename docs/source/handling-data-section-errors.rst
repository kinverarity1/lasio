Handling data section errors
============================

lasio has a flexible way of handling "errors" in the ~ASCII data section to
accommodate how strict or flexible you want to be.

This is handled by the keyword arguments ``lasio.read(f, read_policy=..., null_policy=...)``.

These keywords work in two ways:

* You specify a policy, which then includes a variety of substitutions. For
  example there is only one ``read_policy`` of 'default'. There are several
  ``null_policy`` choices: 'none', 'strict', 'common', 'aggressive', or 'all'.

  Each of this policies implements a list of substitutions. See
  :mod:`lasio.defaults` for the list. For example, ``null_policy='common'``
  implements these substitutions:

  ``['NULL', '9999.25', '999.25', 'NA', 'INF', 'IO', 'IND']``

  Each of these substitutions are defined in :var:`lasio.defaults.NULL_SUBS`.
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
  :var:`lasio.defaults.NULL_SUBS`, numeric values, or pairs of 
  regular expression arguments for :func:`re.sub`.

``read_policy=``
----------------

The primary use of this is to handle "run-on" errors which were often caused by
large values overflowing the width of a fixed-length formatting field:

.. code-block:: 

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