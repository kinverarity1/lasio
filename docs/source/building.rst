Building a LAS file from scratch
================================

When you create a LASFile from scratch, it comes with some default metadata:

.. code-block:: ipython

    In [5]: import lasio

    In [6]: las = lasio.LASFile()

    In [7]: las.header
    Out[7]:
    {'Curves': [],
     'Other': '',
     'Parameter': [],
     'Version': [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS log ASCII Standard -VERSION 2.0, original_mnemonic=VERS),
      HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=One line per depth step, original_mnemonic=WRAP),
      HeaderItem(mnemonic=DLM, unit=, value=SPACE, descr=Column Data Section Delimiter, original_mnemonic=DLM)],
     'Well': [HeaderItem(mnemonic=STRT, unit=m, value=nan, descr=START DEPTH, original_mnemonic=STRT),
      HeaderItem(mnemonic=STOP, unit=m, value=nan, descr=STOP DEPTH, original_mnemonic=STOP),
      HeaderItem(mnemonic=STEP, unit=m, value=nan, descr=STEP, original_mnemonic=STEP),
      HeaderItem(mnemonic=NULL, unit=, value=-9999.25, descr=NULL VALUE, original_mnemonic=NULL),
      HeaderItem(mnemonic=COMP, unit=, value=, descr=COMPANY, original_mnemonic=COMP),
      HeaderItem(mnemonic=WELL, unit=, value=, descr=WELL, original_mnemonic=WELL),
      HeaderItem(mnemonic=FLD, unit=, value=, descr=FIELD, original_mnemonic=FLD),
      HeaderItem(mnemonic=LOC, unit=, value=, descr=LOCATION, original_mnemonic=LOC),
      HeaderItem(mnemonic=PROV, unit=, value=, descr=PROVINCE, original_mnemonic=PROV),
      HeaderItem(mnemonic=CNTY, unit=, value=, descr=COUNTY, original_mnemonic=CNTY),
      HeaderItem(mnemonic=STAT, unit=, value=, descr=STATE, original_mnemonic=STAT),
      HeaderItem(mnemonic=CTRY, unit=, value=, descr=COUNTRY, original_mnemonic=CTRY),
      HeaderItem(mnemonic=SRVC, unit=, value=, descr=SERVICE COMPANY, original_mnemonic=SRVC),
      HeaderItem(mnemonic=DATE, unit=, value=, descr=DATE, original_mnemonic=DATE),
      HeaderItem(mnemonic=UWI, unit=, value=, descr=UNIQUE WELL ID, original_mnemonic=UWI),
      HeaderItem(mnemonic=API, unit=, value=, descr=API NUMBER, original_mnemonic=API)]}

In our case, let's set the correct date:

.. code-block:: ipython

    In [8]: from datetime import datetime

    In [9]: las.well.DATE = str(datetime.today())

And add some new header fields:

.. code-block:: ipython

    In [10]: las.params['ENG'] = lasio.HeaderItem('ENG', value='Kent Inverarity')

    In [11]: las.params['LMF'] = lasio.HeaderItem('LMF', value='GL')

    In [12]: las.other = 'Example of how to create a LAS file from scratch using lasio'

We will invent some data for a curve:

.. code-block:: ipython

    In [1]: import numpy as np

    In [2]: depths = np.arange(10, 50, 0.5)

    In [3]: synth = np.log10(depths)*5+np.random.random(len(depths))

    In [4]: synth[:8] = np.nan

\...add these to the LASFile object:

.. code-block:: ipython

    In [13]: las.add_curve('DEPT', depths, unit='m')

    In [14]: las.add_curve('SYNTH', synth, descr='fake data')

And write the result to files:

.. code-block:: ipython

    In [16]: las.write('scratch_v1.2.las', version=1.2)

    In [15]: las.write('scratch_v2.las', version=2)

Here is the resulting scratch_v1.2.las:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS.   1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
    WRAP.    NO : One line per depth step
    DLM . SPACE : Column Data Section Delimiter
    ~Well ------------------------------------------------------
    STRT.m           10.0 : START DEPTH
    STOP.m           49.5 : STOP DEPTH
    STEP.m            0.5 : STEP
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
    DATE.            DATE : 2017-11-04 15:33:20.963287
    UWI .  UNIQUE WELL ID : 
    API .      API NUMBER : 
    ~Curves ----------------------------------------------------
    DEPT .m  : 
    SYNTH.   : fake data
    ~Params ----------------------------------------------------
    ENG. Kent Inverarity : 
    LMF.              GL : 
    ~Other -----------------------------------------------------
    Example of how to create a LAS file from scratch using lasio
    ~ASCII -----------------------------------------------------
             10   -9999.25
           10.5   -9999.25
             11   -9999.25
           11.5   -9999.25
             12   -9999.25
           12.5   -9999.25
             13   -9999.25
           13.5   -9999.25
             14      5.799
           14.5     6.3938
             15     6.4122
           15.5     6.4605
             16     6.9518
           16.5      6.567
             17     6.3816
           17.5     6.2872
             18     6.4336
           18.5     7.0252
             19     6.7988
           19.5     6.7172
             20     6.6929
           20.5     7.0971
             21      7.145
           21.5     6.7192
             22     7.6034
           22.5     7.3078
             23     7.2213
           23.5      7.668
             24      7.853
           24.5     7.4073
             25     7.4238
           25.5     7.9173
             26     7.1282
           26.5     7.4131
             27     7.8014
           27.5      7.348
             28        7.9
           28.5     7.6294
             29     8.1244
           29.5     7.9835
             30     7.4759
           30.5     8.3766
             31     7.4717
           31.5     7.6432
             32     8.2327
           32.5     7.6541
             33     8.4481
           33.5     7.8811
             34     8.2332
           34.5     8.4302
             35     7.7218
           35.5       8.71
             36     8.3965
           36.5     8.4355
             37     8.6836
           37.5     8.2236
             38     8.4997
           38.5     8.6656
             39     8.8295
           39.5     8.1707
             40     8.9034
           40.5      8.681
             41     8.1698
           41.5     8.3001
             42     9.0266
           42.5     8.4398
             43     8.7562
           43.5     8.2673
             44     8.4682
           44.5     8.5801
             45     8.9065
           45.5     8.8392
             46      8.661
           46.5     9.2355
             47     9.0468
           47.5     8.8249
             48     9.0298
           48.5     8.6864
             49     8.5745
           49.5     8.6143

and scratch_v2.las:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS.   2.0 : CWLS log ASCII Standard -VERSION 2.0
    WRAP.    NO : One line per depth step
    DLM . SPACE : Column Data Section Delimiter
    ~Well ------------------------------------------------------
    STRT.m                      10.0 : START DEPTH
    STOP.m                      49.5 : STOP DEPTH
    STEP.m                       0.5 : STEP
    NULL.                   -9999.25 : NULL VALUE
    COMP.                            : COMPANY
    WELL.                            : WELL
    FLD .                            : FIELD
    LOC .                            : LOCATION
    PROV.                            : PROVINCE
    CNTY.                            : COUNTY
    STAT.                            : STATE
    CTRY.                            : COUNTRY
    SRVC.                            : SERVICE COMPANY
    DATE. 2017-11-04 15:33:20.963287 : DATE
    UWI .                            : UNIQUE WELL ID
    API .                            : API NUMBER
    ~Curves ----------------------------------------------------
    DEPT .m  : 
    SYNTH.   : fake data
    ~Params ----------------------------------------------------
    ENG. Kent Inverarity : 
    LMF.              GL : 
    ~Other -----------------------------------------------------
    Example of how to create a LAS file from scratch using lasio
    ~ASCII -----------------------------------------------------
             10   -9999.25
           10.5   -9999.25
             11   -9999.25
           11.5   -9999.25
             12   -9999.25
           12.5   -9999.25
             13   -9999.25
           13.5   -9999.25
             14      5.799
           14.5     6.3938
             15     6.4122
           15.5     6.4605
             16     6.9518
           16.5      6.567
             17     6.3816
           17.5     6.2872
             18     6.4336
           18.5     7.0252
             19     6.7988
           19.5     6.7172
             20     6.6929
           20.5     7.0971
             21      7.145
           21.5     6.7192
             22     7.6034
           22.5     7.3078
             23     7.2213
           23.5      7.668
             24      7.853
           24.5     7.4073
             25     7.4238
           25.5     7.9173
             26     7.1282
           26.5     7.4131
             27     7.8014
           27.5      7.348
             28        7.9
           28.5     7.6294
             29     8.1244
           29.5     7.9835
             30     7.4759
           30.5     8.3766
             31     7.4717
           31.5     7.6432
             32     8.2327
           32.5     7.6541
             33     8.4481
           33.5     7.8811
             34     8.2332
           34.5     8.4302
             35     7.7218
           35.5       8.71
             36     8.3965
           36.5     8.4355
             37     8.6836
           37.5     8.2236
             38     8.4997
           38.5     8.6656
             39     8.8295
           39.5     8.1707
             40     8.9034
           40.5      8.681
             41     8.1698
           41.5     8.3001
             42     9.0266
           42.5     8.4398
             43     8.7562
           43.5     8.2673
             44     8.4682
           44.5     8.5801
             45     8.9065
           45.5     8.8392
             46      8.661
           46.5     9.2355
             47     9.0468
           47.5     8.8249
             48     9.0298
           48.5     8.6864
             49     8.5745
           49.5     8.6143
