Basic example
=============

.. code-block:: python

    >>> import lasio

You can use :func:`lasio.read` to open any file or URL. For this tutorial I
will use the ``lasio.examples`` module to load a `LAS file`_ which is bundled
with lasio:

.. code-block:: python

    >>> import lasio.examples
    >>> las = lasio.examples.open("1001178549.las")

The :func:`lasio.read` function returns a :class:`lasio.LASFile` object. Each
of the standard LAS sections can be accessed as an attribute:

.. code-block:: python

    >>> las.version
    [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS Log ASCII Standard -V...),
     HeaderItem(mnemonic=WRAP, unit=, value=YES, descr=Multiple lines per depth step)]

Each LAS section is represented as a :class:`lasio.SectionItems` object. The
others, for LAS 2.0 files, are present as ``las.well``, ``las.curves``, and
``las.params``; the ~O section is a string accessible at ``las.other``.

You can also see the sections printed as an easier-to-read table:

.. code-block:: python

    >>> print(las.curves)
    Mnemonic  Unit    Value         Description
    --------  ----    -----         -----------
    DEPT      FT      0   1  0  0   1 DEPTH
    GSGR      API     31 310  0  0  2 GAMMA RAY
    GSTK      API     31 797  0  0  3 ????????
    GST       API     99 999 99  0  4 ????????
    GSK       PERCNT  31 721  1  0  5 ????????
    GSTH      PPM     31 790  0  0  6 THORIUM
    GSUR      PPM     31 792  0  0  7 URANIUM
    NCNPL     PERCNT  42 890  1  0  8 NEUTRON POROSITY (LIMESTONE)
    DLDPL     PERCNT  43 890 10  0  9 DENSITY POROSITY (LIMESTONE)
    DLDC      GM/CC   43 356  0  0  10 DENSITY CORRECTION
    DLPE      B/E     43 358  0  0  11 PHOTO-ELECTRIC EFFECT
    DLDN      GM/CC   43 350  0  0  12 BULK DENSITY
    DLCL      INCHES  43 280  0  0  13 CALIPER
    DLTN      LBS     43 635  0  0  14 ????????
    IDGR      API     7 310  0  0   15 GAMMA RAY
    ACCL1     INCHES  60 280  1  0  16 DENSITY CALIPER
    ACCL2     INCHES  60 280  2  0  17 NEUTRON CALIPER
    ACTC      US/FT   60 520  0  0  18 SONIC INTERVAL TRANSIT TIME (COMPENSATED)
    ACAPL     PERCNT  60 890 20  0  19 POROSITY
    IDIM      OHMM    7 120 44  0   20 MEDIUM INDUCTION
    IDID      OHMM    7 120 46  0   21 DEEP INDUCTION
    IDIDC     MMHOS   7 110 46  0   22 INDUCTION (CONDUCTIVITY UNITS)
    IDL3      OHMM    7 220  3  0   23 FOCUSSED RESISTIVITY
    IDTN      LBS     7 635  0  0   24 ????????
    IDSP      MVOLT   7  10  0  0   25 SPONTANEOUS POTENTIAL
    MEL1      OHMM    15 250  2  0  26 MICRO INVERSE 1"
    ME        OHMM    15 252  2  0  27 MICRO NORMAL 2"

The data is present as a :class:`numpy.ndarray` at ``las.data``:

.. code-block:: python

    >>> las.data.shape
    (5, 27)
    >>> las.data
    array([[1.7835000e+03,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan, 5.0646500e+01, 8.3871000e+00,
            8.4396000e+00, 5.5100000e+01, 5.6900000e-02, 5.6000000e+02,
            1.7500000e+02, 5.0000000e-02, 4.5330000e-01, 1.8930420e+03,
            9.2605000e+01,           nan,           nan],
           [1.7837500e+03,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan, 4.9676700e+01, 8.3951000e+00,
            8.4460000e+00, 5.4355500e+01, 5.9000000e-02, 5.6000000e+02,
            1.7500000e+02, 5.0000000e-02, 4.5340000e-01, 1.8523320e+03,
            9.2778000e+01,           nan,           nan],
           [1.7840000e+03,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan, 4.8631300e+01, 8.4052000e+00,
            8.4460000e+00, 5.4444400e+01, 5.8100000e-02, 5.6000000e+02,
            1.7500000e+02, 5.0000000e-02, 4.5370000e-01, 1.8319766e+03,
            9.2948200e+01,           nan,           nan],
           [1.7842500e+03,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan, 4.7771700e+01, 8.4173000e+00,
            8.4438000e+00, 5.5311100e+01, 5.7700000e-02, 5.6000000e+02,
            1.7500000e+02, 5.0000000e-02, 4.5380000e-01, 1.8319766e+03,
            9.3110300e+01,           nan,           nan],
           [1.7845000e+03,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan,           nan,           nan,
                      nan,           nan, 4.8114900e+01, 8.4253000e+00,
            8.4460000e+00, 5.6322200e+01, 5.8500000e-02, 5.6000000e+02,
            1.7500000e+02, 5.0000000e-02, 4.5390000e-01, 1.8116211e+03,
            9.3267100e+01,           nan,           nan]])

Although it might be easier for you to iterate over the curves:

.. code-block:: python

    >>> for curve in las.curves:
    ...     print(curve.mnemonic + ": " + str(curve.data))
    DEPT: [1783.5  1783.75 1784.   1784.25 1784.5 ]
    GSGR: [nan nan nan nan nan]
    GSTK: [nan nan nan nan nan]
    GST: [nan nan nan nan nan]
    GSK: [nan nan nan nan nan]
    GSTH: [nan nan nan nan nan]
    GSUR: [nan nan nan nan nan]
    NCNPL: [nan nan nan nan nan]
    DLDPL: [nan nan nan nan nan]
    DLDC: [nan nan nan nan nan]
    DLPE: [nan nan nan nan nan]
    DLDN: [nan nan nan nan nan]
    DLCL: [nan nan nan nan nan]
    DLTN: [nan nan nan nan nan]
    IDGR: [50.6465 49.6767 48.6313 47.7717 48.1149]
    ACCL1: [8.3871 8.3951 8.4052 8.4173 8.4253]
    ACCL2: [8.4396 8.446  8.446  8.4438 8.446 ]
    ACTC: [55.1    54.3555 54.4444 55.3111 56.3222]
    ACAPL: [0.0569 0.059  0.0581 0.0577 0.0585]
    IDIM: [560. 560. 560. 560. 560.]
    IDID: [175. 175. 175. 175. 175.]
    IDIDC: [0.05 0.05 0.05 0.05 0.05]
    IDL3: [0.4533 0.4534 0.4537 0.4538 0.4539]
    IDTN: [1893.042  1852.332  1831.9766 1831.9766 1811.6211]
    IDSP: [92.605  92.778  92.9482 93.1103 93.2671]
    MEL1: [nan nan nan nan nan]
    ME: [nan nan nan nan nan]

The first curve in the LAS file -- usually the depth -- is present as
``las.index``, and curves are also accessible from the LASFile object as
items. For example:

.. code-block:: python

    >>> las.index
    array([1783.5 , 1783.75, 1784.  , 1784.25, 1784.5 ])
    >>> las["IDTN"]
    array([1893.042 , 1852.332 , 1831.9766, 1831.9766, 1811.6211])

.. _python: https://python.org/
.. _LAS file: https://raw.githubusercontent.com/kinverarity1/lasio/master/tests/examples/1001178549.las