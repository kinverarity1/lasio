Building a LAS file from scratch
================================

When you create a :class:`lasio.LASFile` from scratch, it comes with some
default metadata:

.. code-block:: python

    >>> import lasio
    >>> las = lasio.LASFile()
    >>> las.header
    {'Version': [HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS log ASCII Standa"),
     HeaderItem(mnemonic="WRAP", unit="", value="NO", descr="One line per depth ste"),
     HeaderItem(mnemonic="DLM", unit="", value="SPACE", descr="Column Data Section ")], 
    'Well': [HeaderItem(mnemonic="STRT", unit="m", value="nan", descr="START DEPTH"),
     HeaderItem(mnemonic="STOP", unit="m", value="nan", descr="STOP DEPTH"),
     HeaderItem(mnemonic="STEP", unit="m", value="nan", descr="STEP"),
     HeaderItem(mnemonic="NULL", unit="", value="-9999.25", descr="NULL VALUE"),
     HeaderItem(mnemonic="COMP", unit="", value="", descr="COMPANY"),
     HeaderItem(mnemonic="WELL", unit="", value="", descr="WELL"),
     HeaderItem(mnemonic="FLD", unit="", value="", descr="FIELD"),
     HeaderItem(mnemonic="LOC", unit="", value="", descr="LOCATION"),
     HeaderItem(mnemonic="PROV", unit="", value="", descr="PROVINCE"),
     HeaderItem(mnemonic="CNTY", unit="", value="", descr="COUNTY"),
     HeaderItem(mnemonic="STAT", unit="", value="", descr="STATE"),
     HeaderItem(mnemonic="CTRY", unit="", value="", descr="COUNTRY"),
     HeaderItem(mnemonic="SRVC", unit="", value="", descr="SERVICE COMPANY"),
     HeaderItem(mnemonic="DATE", unit="", value="", descr="DATE"),
     HeaderItem(mnemonic="UWI", unit="", value="", descr="UNIQUE WELL ID"),
     HeaderItem(mnemonic="API", unit="", value="", descr="API NUMBER")], 
    'Curves': [], 
    'Parameter': [], 
    'Other': ''}

In our case, let's set the correct date:

.. code-block:: python

    >>> from datetime import datetime
    >>> las.well.DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

And add some new header fields:

.. code-block:: python

    >>> las.params['ENG'] = lasio.HeaderItem('ENG', value='Kent Inverarity')
    >>> las.params['LMF'] = lasio.HeaderItem('LMF', value='GL')
    >>> las.other = 'Example of how to create a LAS file from scratch using lasio'

We will invent some data for a curve:

.. code-block:: python

    >>> import numpy as np
    >>> depths = np.arange(10, 50, 0.5)
    >>> synth = np.log10(depths)*5+np.random.random(len(depths))
    >>> synth[:8] = np.nan

\...add these to the LASFile object:

.. code-block:: python

    >>> las.append_curve('DEPT', depths, unit='m')
    >>> las.append_curve('SYNTH', synth, descr='fake data')

And write the result to files:

.. code-block:: python

    >>> las.write('scratch_v1.2.las', version=1.2)
    >>> las.write('scratch_v2.las', version=2)

Here is the resulting scratch_v1.2.las:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS.   1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
    WRAP.    NO : One line per depth step
    DLM . SPACE : Column Data Section Delimiter
    ~Well ------------------------------------------------------
    STRT.m       10.00000 : START DEPTH
    STOP.m       49.50000 : STOP DEPTH
    STEP.m        0.50000 : STEP
    NULL.        -9999.25 : NULL VALUE
    COMP.         COMPANY :
    WELL.            WELL :
    FLD .           FIELD :
    LOC .        LOCATION :
    PROV.        PROVINCE :
    CNTY.          COUNTY :
    STAT.           STATE :
    CTRY.         COUNTRY :
    SRVC. SERVICE COMPANY :
    DATE.            DATE : 2023-01-26 14:58:21
    UWI .  UNIQUE WELL ID :
    API .      API NUMBER :
    ~Curve Information -----------------------------------------
    DEPT .m  :
    SYNTH.   : fake data
    ~Params ----------------------------------------------------
    ENG. Kent Inverarity :
    LMF.              GL :
    ~Other -----------------------------------------------------
    Example of how to create a LAS file from scratch using lasio
    ~ASCII -----------------------------------------------------
       10.00000   -9999.25
       10.50000   -9999.25
       11.00000   -9999.25
       11.50000   -9999.25
       12.00000   -9999.25
       12.50000   -9999.25
       13.00000   -9999.25
       13.50000   -9999.25
       14.00000    6.32656
       14.50000    6.32279
       15.00000    6.24716
       15.50000    6.07168
       16.00000    6.40693
       16.50000    6.74994
       17.00000    6.16163
       17.50000    7.08836
       18.00000    6.31721
       18.50000    7.19034
       19.00000    6.72278
       19.50000    7.01719
       20.00000    7.49475
       20.50000    6.92995
       21.00000    7.44739
       21.50000    7.55360
       22.00000    6.94753
       22.50000    7.64236
       23.00000    7.74817
       23.50000    7.23852
       24.00000    7.88034
       24.50000    7.07664
       25.00000    7.19182
       25.50000    7.62403
       26.00000    7.80678
       26.50000    7.93082
       27.00000    8.08903
       27.50000    7.81581
       28.00000    8.08901
       28.50000    7.60532
       29.00000    7.86530
       29.50000    7.72080
       30.00000    7.74472
       30.50000    7.68292
       31.00000    8.00722
       31.50000    8.12406
       32.00000    7.60265
       32.50000    7.73699
       33.00000    7.72325
       33.50000    8.02248
       34.00000    8.04029
       34.50000    8.65056
       35.00000    8.30488
       35.50000    8.59884
       36.00000    7.83725
       36.50000    8.72173
       37.00000    7.95948
       37.50000    8.12969
       38.00000    8.75692
       38.50000    8.73753
       39.00000    8.22793
       39.50000    8.86533
       40.00000    8.56819
       40.50000    9.00213
       41.00000    8.51844
       41.50000    8.81121
       42.00000    8.51106
       42.50000    8.28359
       43.00000    8.65719
       43.50000    8.33235
       44.00000    8.52983
       44.50000    9.04601
       45.00000    8.53333
       45.50000    9.20433
       46.00000    8.60132
       46.50000    8.94629
       47.00000    8.60415
       47.50000    8.56460
       48.00000    9.35277
       48.50000    8.65887
       49.00000    9.33907
       49.50000    9.30430


and scratch_v2.las:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS.   2.0 : CWLS log ASCII Standard -VERSION 2.0
    WRAP.    NO : One line per depth step
    DLM . SPACE : Column Data Section Delimiter
    ~Well ------------------------------------------------------
    STRT.m           10.00000 : START DEPTH
    STOP.m           49.50000 : STOP DEPTH
    STEP.m            0.50000 : STEP
    NULL.            -9999.25 : NULL VALUE
    COMP.                     : COMPANY
    WELL.                     : WELL
    FLD .                     : FIELD
    LOC .                     : LOCATION
    PROV.                     : PROVINCE
    CNTY.                     : COUNTY
    STAT.                     : STATE
    CTRY.                     : COUNTRY
    SRVC.                     : SERVICE COMPANY
    DATE. 2023-01-26 14:58:21 : DATE
    UWI .                     : UNIQUE WELL ID
    API .                     : API NUMBER
    ~Curve Information -----------------------------------------
    DEPT .m  :
    SYNTH.   : fake data
    ~Params ----------------------------------------------------
    ENG. Kent Inverarity :
    LMF.              GL :
    ~Other -----------------------------------------------------
    Example of how to create a LAS file from scratch using lasio
    ~ASCII -----------------------------------------------------
       10.00000   -9999.25
       10.50000   -9999.25
       11.00000   -9999.25
       11.50000   -9999.25
       12.00000   -9999.25
       12.50000   -9999.25
       13.00000   -9999.25
       13.50000   -9999.25
       14.00000    6.32656
       14.50000    6.32279
       15.00000    6.24716
       15.50000    6.07168
       16.00000    6.40693
       16.50000    6.74994
       17.00000    6.16163
       17.50000    7.08836
       18.00000    6.31721
       18.50000    7.19034
       19.00000    6.72278
       19.50000    7.01719
       20.00000    7.49475
       20.50000    6.92995
       21.00000    7.44739
       21.50000    7.55360
       22.00000    6.94753
       22.50000    7.64236
       23.00000    7.74817
       23.50000    7.23852
       24.00000    7.88034
       24.50000    7.07664
       25.00000    7.19182
       25.50000    7.62403
       26.00000    7.80678
       26.50000    7.93082
       27.00000    8.08903
       27.50000    7.81581
       28.00000    8.08901
       28.50000    7.60532
       29.00000    7.86530
       29.50000    7.72080
       30.00000    7.74472
       30.50000    7.68292
       31.00000    8.00722
       31.50000    8.12406
       32.00000    7.60265
       32.50000    7.73699
       33.00000    7.72325
       33.50000    8.02248
       34.00000    8.04029
       34.50000    8.65056
       35.00000    8.30488
       35.50000    8.59884
       36.00000    7.83725
       36.50000    8.72173
       37.00000    7.95948
       37.50000    8.12969
       38.00000    8.75692
       38.50000    8.73753
       39.00000    8.22793
       39.50000    8.86533
       40.00000    8.56819
       40.50000    9.00213
       41.00000    8.51844
       41.50000    8.81121
       42.00000    8.51106
       42.50000    8.28359
       43.00000    8.65719
       43.50000    8.33235
       44.00000    8.52983
       44.50000    9.04601
       45.00000    8.53333
       45.50000    9.20433
       46.00000    8.60132
       46.50000    8.94629
       47.00000    8.60415
       47.50000    8.56460
       48.00000    9.35277
       48.50000    8.65887
       49.00000    9.33907
       49.50000    9.30430
