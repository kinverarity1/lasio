Header section metadata
=======================

Tutorial
--------

One of the primary motivations in writing lasio was to be able to reliably
parse LAS header sections. This is working fairly well for LAS 1.2 and 2.0
files, and lasio does not require LAS files to be strictly compliant with
either standard.

.. code-block:: ipython

    In [179]: import lasio

    In [180]: las = lasio.read('tests/examples/6038187_v1.2_short.las')

The header sections are stored in the dictionary ``las.sections``:

.. code-block:: ipython

    In [206]: type(las.sections)
    Out[206]: dict

    In [207]: las.sections.keys()
    Out[207]: dict_keys(['Version', 'Well', 'Curves', 'Parameter', 'Other'])

These are special names reserved for LAS 1.2 and 2.0 files, as defined by the
standard. Non-standard header sections are also allowed but not fully parsed.

==============================  =======================================  ===================================================================
LAS file                        Read in as                               References in ``LASFile``
==============================  =======================================  ===================================================================
``~v`` or ``~V``                :class:`lasio.las_items.SectionItems`    ``LASFile.version`` and ``LASFile.sections['Version']``
``~w`` or ``~W``                :class:`lasio.las_items.SectionItems`    ``LASFile.well`` and ``LASFile.sections['Well']``
``~c`` or ``~C``                :class:`lasio.las_items.SectionItems`    ``LASFile.curves`` and ``LASFile.sections['Curves']``
``~p`` or ``~P``                :class:`lasio.las_items.SectionItems`    ``LASFile.params`` and ``LASFile.sections['Parameter']``
``~o`` or ``~O``                ``str``                                  ``LASFile.other`` and ``LASFile.sections['Other']``
``~extra section``              ``str``                                  ``LASFile.sections['extra section']``
``~a`` or ``~A``                :class:`numpy.ndarray`                   ``LASFile.data`` or each column is in ``LASFile.curves[...].data``
==============================  =======================================  ===================================================================

For example:

.. code-block:: ipython

    In [208]: las.sections['Version']
    Out[208]:
    [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS),
     HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=ONE LINE PER DEPTH STEP, original_mnemonic=WRAP)]

    In [182]: las.version
    Out[182]:
    [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS),
     HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=ONE LINE PER DEPTH STEP, original_mnemonic=WRAP)]

Sections themselves are represented by :class:`lasio.las_items.SectionItems` objects.
This is a ``list`` which has been extended to allow you to access the items within
by their mnemonic:

.. code-block:: ipython

    In [209]: las.version.VERS
    Out[209]: HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)

    In [210]: las.version['VERS']
    Out[210]: HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)

    In [211]: las.version[0]
    Out[211]: HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)

    In [212]: id(Out[209]), id(Out[210]), id(Out[211])
    Out[212]: (250964032, 250964032, 250964032)

As you can see, either attribute-style or item-style access is fine - with one exception, see below.

Let's take a look at the next special section, ``~W``:

.. code-block:: ipython

    In [188]: las.well
    Out[188]:
    [HeaderItem(mnemonic=STRT, unit=M, value=0.05, descr=FIRST INDEX VALUE, original_mnemonic=STRT),
     HeaderItem(mnemonic=STOP, unit=M, value=136.6, descr=LAST INDEX VALUE, original_mnemonic=STOP),
     HeaderItem(mnemonic=STEP, unit=M, value=0.05, descr=STEP, original_mnemonic=STEP),
     HeaderItem(mnemonic=NULL, unit=, value=-99999, descr=NULL VALUE, original_mnemonic=NULL),
     HeaderItem(mnemonic=COMP, unit=, value=, descr=COMP, original_mnemonic=COMP),
     HeaderItem(mnemonic=WELL, unit=, value=Scorpio E1, descr=WELL, original_mnemonic=WELL),
     HeaderItem(mnemonic=FLD, unit=, value=, descr=, original_mnemonic=FLD),
     HeaderItem(mnemonic=LOC, unit=, value=Mt Eba, descr=LOC, original_mnemonic=LOC),
     HeaderItem(mnemonic=SRVC, unit=, value=, descr=, original_mnemonic=SRVC),
     HeaderItem(mnemonic=CTRY, unit=, value=, descr=, original_mnemonic=CTRY),
     HeaderItem(mnemonic=STAT, unit=, value=SA, descr=STAT, original_mnemonic=STAT),
     HeaderItem(mnemonic=CNTY, unit=, value=, descr=, original_mnemonic=CNTY),
     HeaderItem(mnemonic=DATE, unit=, value=15/03/2015, descr=DATE, original_mnemonic=DATE),
     HeaderItem(mnemonic=UWI, unit=, value=6038-187, descr=WUNT, original_mnemonic=UWI)]

The CTRY item is blank. We will set it:

.. code-block:: ipython

    In [190]: las.well.CTRY = 'Australia'

    In [191]: las.well.CTRY
    Out[191]: HeaderItem(mnemonic=CTRY, unit=, value=Australia, descr=, original_mnemonic=CTRY)

Notice that ``SectionItems`` plays a little trick here. It actually sets the ``header_item.value``
attribute, instead of replacing the entire ``HeaderItem`` object.

You can set any of the attributes directly. Let's take an example from the ``~C`` section:

.. code-block:: ipython

    In [192]: las.curves
    Out[192]:
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=DEPTH, original_mnemonic=DEPT, data.shape=(121,)),
     CurveItem(mnemonic=CALI, unit=MM, value=, descr=CALI, original_mnemonic=CALI, data.shape=(121,)),
     CurveItem(mnemonic=DFAR, unit=G/CM3, value=, descr=DFAR, original_mnemonic=DFAR, data.shape=(121,)),
     CurveItem(mnemonic=DNEAR, unit=G/CM3, value=, descr=DNEAR, original_mnemonic=DNEAR, data.shape=(121,)),
     CurveItem(mnemonic=GAMN, unit=GAPI, value=, descr=GAMN, original_mnemonic=GAMN, data.shape=(121,)),
     CurveItem(mnemonic=NEUT, unit=CPS, value=, descr=NEUT, original_mnemonic=NEUT, data.shape=(121,)),
     CurveItem(mnemonic=PR, unit=OHM/M, value=, descr=PR, original_mnemonic=PR, data.shape=(121,)),
     CurveItem(mnemonic=SP, unit=MV, value=, descr=SP, original_mnemonic=SP, data.shape=(121,)),
     CurveItem(mnemonic=COND, unit=MS/M, value=, descr=COND, original_mnemonic=COND, data.shape=(121,))]

    In [193]: las.curves.PR.unit = 'ohmm'

    In [194]: las.curves.PR
    Out[194]: CurveItem(mnemonic=PR, unit=ohmm, value=, descr=PR, original_mnemonic=PR, data.shape=(121,))

Now let's look more closely at how to manipulate and add or remove items from a
section.

.. code-block:: ipython

    In [195]: las.params
    Out[195]:
    [HeaderItem(mnemonic=BS, unit=, value=216 mm, descr=BS, original_mnemonic=BS),
     HeaderItem(mnemonic=JOBN, unit=, value=, descr=JOBN, original_mnemonic=JOBN),
     HeaderItem(mnemonic=WPMT, unit=, value=, descr=WPMT, original_mnemonic=WPMT),
     HeaderItem(mnemonic=AGL, unit=, value=, descr=AGL, original_mnemonic=AGL),
     HeaderItem(mnemonic=PURP, unit=, value=Cased hole stratigraphy, descr=PURP, original_mnemonic=PURP),
     HeaderItem(mnemonic=X, unit=, value=560160, descr=X, original_mnemonic=X),
     HeaderItem(mnemonic=CSGL, unit=, value=0 m - 135 m, descr=CSGL, original_mnemonic=CSGL),
     HeaderItem(mnemonic=UNIT, unit=, value=, descr=UNIT, original_mnemonic=UNIT),
     HeaderItem(mnemonic=Y, unit=, value=6686430, descr=Y, original_mnemonic=Y),
     HeaderItem(mnemonic=TDL, unit=, value=135.2 m, descr=TDL, original_mnemonic=TDL),
     HeaderItem(mnemonic=PROD, unit=, value=, descr=PROD, original_mnemonic=PROD),
     HeaderItem(mnemonic=MUD, unit=, value=Water, descr=MUD, original_mnemonic=MUD),
     HeaderItem(mnemonic=CSGS, unit=, value=100 mm, descr=CSGS, original_mnemonic=CSGS),
     HeaderItem(mnemonic=ENG, unit=, value=, descr=ENG, original_mnemonic=ENG),
     HeaderItem(mnemonic=STEP, unit=, value=5 cm, descr=STEP, original_mnemonic=STEP),
     HeaderItem(mnemonic=FluidLevel, unit=, value=54 m, descr=FluidLevel, original_mnemonic=FluidLevel),
     HeaderItem(mnemonic=CSGT, unit=, value=PVC, descr=CSGT, original_mnemonic=CSGT),
     HeaderItem(mnemonic=WIT, unit=, value=, descr=WIT, original_mnemonic=WIT),
     HeaderItem(mnemonic=EREF, unit=, value=, descr=EREF, original_mnemonic=EREF),
     HeaderItem(mnemonic=PROJ, unit=, value=, descr=PROJ, original_mnemonic=PROJ),
     HeaderItem(mnemonic=ZONE, unit=, value=53J, descr=ZONE, original_mnemonic=ZONE),
     HeaderItem(mnemonic=DREF, unit=, value=GL, descr=DREF, original_mnemonic=DREF),
     HeaderItem(mnemonic=TDD, unit=, value=136 m, descr=TDD, original_mnemonic=TDD)]

We want to rename the DREF mnemonic as LMF. We can do so by changing the 
``header_item.mnemonic`` attribute.

.. code-block:: ipython

    In [197]: las.params.DREF.mnemonic = 'LMF'

    In [198]: las.params
    Out[198]:
    [HeaderItem(mnemonic=BS, unit=, value=216 mm, descr=BS, original_mnemonic=BS),
     HeaderItem(mnemonic=JOBN, unit=, value=, descr=JOBN, original_mnemonic=JOBN),
     HeaderItem(mnemonic=WPMT, unit=, value=, descr=WPMT, original_mnemonic=WPMT),
     HeaderItem(mnemonic=AGL, unit=, value=, descr=AGL, original_mnemonic=AGL),
     HeaderItem(mnemonic=PURP, unit=, value=Cased hole stratigraphy, descr=PURP, original_mnemonic=PURP),
     HeaderItem(mnemonic=X, unit=, value=560160, descr=X, original_mnemonic=X),
     HeaderItem(mnemonic=CSGL, unit=, value=0 m - 135 m, descr=CSGL, original_mnemonic=CSGL),
     HeaderItem(mnemonic=UNIT, unit=, value=, descr=UNIT, original_mnemonic=UNIT),
     HeaderItem(mnemonic=Y, unit=, value=6686430, descr=Y, original_mnemonic=Y),
     HeaderItem(mnemonic=TDL, unit=, value=135.2 m, descr=TDL, original_mnemonic=TDL),
     HeaderItem(mnemonic=PROD, unit=, value=, descr=PROD, original_mnemonic=PROD),
     HeaderItem(mnemonic=MUD, unit=, value=Water, descr=MUD, original_mnemonic=MUD),
     HeaderItem(mnemonic=CSGS, unit=, value=100 mm, descr=CSGS, original_mnemonic=CSGS),
     HeaderItem(mnemonic=ENG, unit=, value=, descr=ENG, original_mnemonic=ENG),
     HeaderItem(mnemonic=STEP, unit=, value=5 cm, descr=STEP, original_mnemonic=STEP),
     HeaderItem(mnemonic=FluidLevel, unit=, value=54 m, descr=FluidLevel, original_mnemonic=FluidLevel),
     HeaderItem(mnemonic=CSGT, unit=, value=PVC, descr=CSGT, original_mnemonic=CSGT),
     HeaderItem(mnemonic=WIT, unit=, value=, descr=WIT, original_mnemonic=WIT),
     HeaderItem(mnemonic=EREF, unit=, value=, descr=EREF, original_mnemonic=EREF),
     HeaderItem(mnemonic=PROJ, unit=, value=, descr=PROJ, original_mnemonic=PROJ),
     HeaderItem(mnemonic=ZONE, unit=, value=53J, descr=ZONE, original_mnemonic=ZONE),
     HeaderItem(mnemonic=LMF, unit=, value=GL, descr=DREF, original_mnemonic=LMF),
     HeaderItem(mnemonic=TDD, unit=, value=136 m, descr=TDD, original_mnemonic=TDD)]

And now we need to add a new mnemonic. Adding via an attribute **will not work**. You need to
use the item-style access.

.. code-block:: ipython

    In [201]: las.params['DRILL'] = lasio.HeaderItem(mnemonic='DRILL', value='John Smith', descr='Driller on site')

    In [202]: las.params
    Out[202]:
    [HeaderItem(mnemonic=BS, unit=, value=216 mm, descr=BS, original_mnemonic=BS),
     HeaderItem(mnemonic=JOBN, unit=, value=, descr=JOBN, original_mnemonic=JOBN),
     HeaderItem(mnemonic=WPMT, unit=, value=, descr=WPMT, original_mnemonic=WPMT),
     HeaderItem(mnemonic=AGL, unit=, value=, descr=AGL, original_mnemonic=AGL),
     HeaderItem(mnemonic=PURP, unit=, value=Cased hole stratigraphy, descr=PURP, original_mnemonic=PURP),
     HeaderItem(mnemonic=X, unit=, value=560160, descr=X, original_mnemonic=X),
     HeaderItem(mnemonic=CSGL, unit=, value=0 m - 135 m, descr=CSGL, original_mnemonic=CSGL),
     HeaderItem(mnemonic=UNIT, unit=, value=, descr=UNIT, original_mnemonic=UNIT),
     HeaderItem(mnemonic=Y, unit=, value=6686430, descr=Y, original_mnemonic=Y),
     HeaderItem(mnemonic=TDL, unit=, value=135.2 m, descr=TDL, original_mnemonic=TDL),
     HeaderItem(mnemonic=PROD, unit=, value=, descr=PROD, original_mnemonic=PROD),
     HeaderItem(mnemonic=MUD, unit=, value=Water, descr=MUD, original_mnemonic=MUD),
     HeaderItem(mnemonic=CSGS, unit=, value=100 mm, descr=CSGS, original_mnemonic=CSGS),
     HeaderItem(mnemonic=ENG, unit=, value=, descr=ENG, original_mnemonic=ENG),
     HeaderItem(mnemonic=STEP, unit=, value=5 cm, descr=STEP, original_mnemonic=STEP),
     HeaderItem(mnemonic=FluidLevel, unit=, value=54 m, descr=FluidLevel, original_mnemonic=FluidLevel),
     HeaderItem(mnemonic=CSGT, unit=, value=PVC, descr=CSGT, original_mnemonic=CSGT),
     HeaderItem(mnemonic=WIT, unit=, value=, descr=WIT, original_mnemonic=WIT),
     HeaderItem(mnemonic=EREF, unit=, value=, descr=EREF, original_mnemonic=EREF),
     HeaderItem(mnemonic=PROJ, unit=, value=, descr=PROJ, original_mnemonic=PROJ),
     HeaderItem(mnemonic=ZONE, unit=, value=53J, descr=ZONE, original_mnemonic=ZONE),
     HeaderItem(mnemonic=LMF, unit=, value=GL, descr=DREF, original_mnemonic=LMF),
     HeaderItem(mnemonic=TDD, unit=, value=136 m, descr=TDD, original_mnemonic=TDD),
     HeaderItem(mnemonic=DRILL, unit=, value=John Smith, descr=Driller on site, original_mnemonic=DRILL)]

Bingo.

Handling errors
---------------

lasio will do its best to read every line from the header section. If it can make sense of it,
it will parse it into a mnemonic, unit, value, and description.

However often there are problems in LAS files. For example, a header section might contain something like:

.. code-block:: none

    COUNTY: RUSSELL

(missing period, should be ``COUNTY.    : RUSSELL``). Or:

.. code-block:: none

    API       .                                          : API Number     (required if CTRY = US)   
    "# Surface Coords: 1,000' FNL & 2,000' FWL" 
    LATI      .DEG                                       : Latitude  - see Surface Coords comment above 
    LONG      .DEG                                       : Longitude - see Surface Coords comment above

Obviously the line with " causes an error.

All these (and any other kind of error in the header section) can be turned from LASHeaderError exceptions into :func:`logger.warning` calls instead by using ``lasio.read(..., ignore_header_errors=True)``. 

Here is an example. First we try reading a file without this argument:

.. code-block:: ipython

    In [2]: las = lasio.read('tests/examples/dodgy_param_sect.las', ignore_header_errors=False)
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    ~\Code\lasio\lasio\reader.py in parse_header_section(sectdict, version, ignore_header_errors, mnemonic_case)
        458         try:
    --> 459             values = read_line(line)
        460         except:

    ~\Code\lasio\lasio\reader.py in read_line(*args, **kwargs)
        625     '''
    --> 626     return read_header_line(*args, **kwargs)
        627

    ~\Code\lasio\lasio\reader.py in read_header_line(line, pattern)
        656     m = re.match(pattern, line)
    --> 657     mdict = m.groupdict()
        658     for key, value in mdict.items():

    AttributeError: 'NoneType' object has no attribute 'groupdict'

    During handling of the above exception, another exception occurred:

    LASHeaderError                            Traceback (most recent call last)
    <ipython-input-2-3c0606fe7dc1> in <module>()
    ----> 1 las = lasio.read('tests/examples/dodgy_param_sect.las', ignore_header_errors=False)

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

    ~\Code\lasio\lasio\las.py in read(self, file_ref, ignore_data, read_policy, null_policy, ignore_header_errors, mnemonic_case, **kwargs)
        185         add_section("~P", "Parameter", version=version,
        186                     ignore_header_errors=ignore_header_errors,
    --> 187                     mnemonic_case=mnemonic_case)
        188         s = self.match_raw_section("~O")
        189

    ~\Code\lasio\lasio\las.py in add_section(pattern, name, **sect_kws)
        122             if raw_section:
        123                 self.sections[name] = reader.parse_header_section(raw_section,
    --> 124                                                                   **sect_kws)
        125                 drop.append(raw_section["title"])
        126             else:

    ~\Code\lasio\lasio\reader.py in parse_header_section(sectdict, version, ignore_header_errors, mnemonic_case)
        465                 logger.warning(message)
        466             else:
    --> 467                 raise exceptions.LASHeaderError(message)
        468         else:
        469             if mnemonic_case == 'upper':

    LASHeaderError: line 31 (section ~PARAMETER INFORMATION): "DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD"

Now if we use ignore_header_errors=True:

.. code-block:: IPython

    In [3]: las = lasio.read('tests/examples/dodgy_param_sect.las', ignore_header_errors=True)
    line 31 (section ~PARAMETER INFORMATION): "DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD"

    In [4]: las.params
    []

    In [5]: las.curves
    Out[5]:
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
    CurveItem(mnemonic=DT, unit=US/M, value=, descr=2  SONIC TRANSIT TIME, original_mnemonic=DT, data.shape=(3,)),
    CurveItem(mnemonic=RHOB, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=RHOB, data.shape=(3,)),
    CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
    CurveItem(mnemonic=SFLU, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=SFLA, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLA, data.shape=(3,)),
    CurveItem(mnemonic=ILM, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=ILM, data.shape=(3,)),
    CurveItem(mnemonic=ILD, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=ILD, data.shape=(3,))]

Only a warning is issued, and the rest of the LAS file loads OK.

Handling duplicate mnemonics 
----------------------------

Take this LAS file as an example, containing this ~C section:

.. code-block:: none

    ~CURVE INFORMATION
    DEPT.M                     :  1  DEPTH
    DT  .US/M     		        :  2  SONIC TRANSIT TIME
    RHOB.K/M3                  :  3  BULK DENSITY
    NPHI.V/V                   :  4   NEUTRON POROSITY
    RXO.OHMM                   :  5  RXO RESISTIVITY
    RES.OHMM                   :  6  SHALLOW RESISTIVITY
    RES.OHMM                   :  7  MEDIUM RESISTIVITY
    RES.OHMM                   :  8  DEEP RESISTIVITY

Notice there are three curves with the mnemonic RES.

When we load the file in, lasio distinguishes between these duplicates:

.. code-block:: IPython

    In [2]: las = lasio.read('tests/examples/mnemonic_duplicate2.las')

    In [3]: las.curves
    Out[3]:
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
    CurveItem(mnemonic=DT, unit=US/M, value=, descr=2  SONIC TRANSIT TIME, original_mnemonic=DT, data.shape=(3,)),
    CurveItem(mnemonic=RHOB, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=RHOB, data.shape=(3,)),
    CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
    CurveItem(mnemonic=RXO, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=RXO, data.shape=(3,)),
    CurveItem(mnemonic=RES:1, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=RES, data.shape=(3,)),
    CurveItem(mnemonic=RES:2, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=RES, data.shape=(3,)),
    CurveItem(mnemonic=RES:3, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=RES, data.shape=(3,))]

    In [4]: las.curves['RES:2']
    Out[4]: CurveItem(mnemonic=RES:2, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=RES, data.shape=(3,))

It remembers the original mnemonic, so when you write the file back out, they come back:

.. code-block:: IPython

    In [6]: import sys

    In [7]: las.write(sys.stdout)
    ~Version ---------------------------------------------------
    VERS. 1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
    WRAP.  NO : ONE LINE PER DEPTH STEP
    ~Well ------------------------------------------------------
    STRT.M         1670.0 :
    STOP.M        1669.75 :
    STEP.M         -0.125 :
    NULL.         -999.25 :
    COMP.         COMPANY : # ANY OIL COMPANY LTD.
    WELL.            WELL : ANY ET AL OIL WELL #12
    FLD .           FIELD : EDAM
    LOC .        LOCATION : A9-16-49-20W3M
    PROV.        PROVINCE : SASKATCHEWAN
    SRVC. SERVICE COMPANY : ANY LOGGING COMPANY LTD.
    DATE.        LOG DATE : 25-DEC-1988
    UWI .  UNIQUE WELL ID : 100091604920W300
    ~Curves ----------------------------------------------------
    DEPT.M     : 1  DEPTH
    DT  .US/M  : 2  SONIC TRANSIT TIME
    RHOB.K/M3  : 3  BULK DENSITY
    NPHI.V/V   : 4   NEUTRON POROSITY
    RXO .OHMM  : 5  RXO RESISTIVITY
    RES .OHMM  : 6  SHALLOW RESISTIVITY
    RES .OHMM  : 7  MEDIUM RESISTIVITY
    RES .OHMM  : 8  DEEP RESISTIVITY
    ~Params ----------------------------------------------------
    BHT .DEGC   35.5 : BOTTOM HOLE TEMPERATURE
    BS  .MM    200.0 : BIT SIZE
    FD  .K/M3 1000.0 : FLUID DENSITY
    MATR.        0.0 : NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)
    MDEN.     2710.0 : LOGGING MATRIX DENSITY
    RMF .OHMM  0.216 : MUD FILTRATE RESISTIVITY
    DFD .K/M3 1525.0 : DRILL FLUID DENSITY
    ~Other -----------------------------------------------------
    Note: The logging tools became stuck at 625 meters causing the data
    between 625 meters and 615 meters to be invalid.
    ~ASCII -----------------------------------------------------
        1670     123.45       2550       0.45     123.45     123.45      110.2      105.6
        1669.9     123.45       2550       0.45     123.45     123.45      110.2      105.6
        1669.8     123.45       2550       0.45     123.45     123.45      110.2      105.6

Normalising mnemonic case 
~~~~~~~~~~~~~~~~~~~~~~~~~

If there is a mix of upper and lower case characters in the mnemonics, by default lasio will convert all mnemonics to uppercase to avoid problems with producing the :1, :2, :3, and so on. There is a keyword argument which will preserve the original formatting if that is what you prefer.

.. code-block:: IPython

    In [8]: las = lasio.read('tests/examples/mnemonic_case.las')

    In [9]: las.curves
    Out[9]:
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:1, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:2, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:3, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:4, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:5, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,))]

    In [10]: las = lasio.read('tests/examples/mnemonic_case.las', mnemonic_case='preserve')

    In [11]: las.curves
    Out[11]:
    [CurveItem(mnemonic=Dept, unit=M, value=, descr=1  DEPTH, original_mnemonic=Dept, data.shape=(3,)),
    CurveItem(mnemonic=Sflu, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=Sflu, data.shape=(3,)),
    CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:1, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=SFLU:2, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
    CurveItem(mnemonic=sflu, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=sflu, data.shape=(3,)),
    CurveItem(mnemonic=SfLu, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=SfLu, data.shape=(3,))]

