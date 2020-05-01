Header section metadata
=======================

Tutorial
--------

One of the primary motivations in writing lasio was to be able to reliably
parse LAS header sections. This is working fairly well for LAS 1.2 and 2.0
files, and lasio does not require LAS files to be strictly compliant with
either standard.

.. code-block:: python

    >>> import lasio.examples
    >>> las = lasio.examples.open('6038187_v1.2_short.las')

The header sections are stored in the dictionary ``las.sections``:

.. code-block:: python

    >>> type(las.sections)
    dict
    >>> las.sections.keys()
    dict_keys(['Version', 'Well', 'Curves', 'Parameter', 'Other'])

These are special names reserved for LAS 1.2 and 2.0 files, as defined by the
standard. Non-standard header sections are also allowed but not fully parsed.

==============================  =======================================  ===================================================================
LAS file                        Read in as                               References in ``LASFile``
==============================  =======================================  ===================================================================
``~v`` or ``~V``                :class:`lasio.SectionItems`              ``LASFile.version`` and ``LASFile.sections['Version']``
``~w`` or ``~W``                :class:`lasio.SectionItems`              ``LASFile.well`` and ``LASFile.sections['Well']``
``~c`` or ``~C``                :class:`lasio.SectionItems`              ``LASFile.curves`` and ``LASFile.sections['Curves']``
``~p`` or ``~P``                :class:`lasio.SectionItems`              ``LASFile.params`` and ``LASFile.sections['Parameter']``
``~o`` or ``~O``                ``str``                                  ``LASFile.other`` and ``LASFile.sections['Other']``
``~extra section``              ``str``                                  ``LASFile.sections['extra section']``
``~a`` or ``~A``                :class:`numpy.ndarray`                   ``LASFile.data`` or each column is in ``LASFile.curves[...].data``
==============================  =======================================  ===================================================================

For example:

.. code-block:: python

    >>> las.sections['Version']
    [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS),
     HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=ONE LINE PER DEPTH STEP, original_mnemonic=WRAP)]

    >>> las.version
    [HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS),
     HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=ONE LINE PER DEPTH STEP, original_mnemonic=WRAP)]

Sections themselves are represented by :class:`lasio.SectionItems`
objects. This is a ``list`` which has been extended to allow you to access the
items within by their mnemonic:

.. code-block:: python

    >>> las.version.VERS
    HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)
    >>> las.version['VERS']
    HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)
    >>> las.version[0]
    HeaderItem(mnemonic=VERS, unit=, value=2.0, descr=CWLS LOG ASCII STANDARD - VERSION 2.0, original_mnemonic=VERS)
    >>> id(Out[209]), id(Out[210]), id(Out[211])
    (250964032, 250964032, 250964032)

As you can see, either attribute-style or item-style access is fine.

Let's take a look at the next special section, ``~W``:

.. code-block:: python

    >>> las.well
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

.. code-block:: python

    >>> las.well.CTRY = 'Australia'
    >>> las.well.CTRY
    HeaderItem(mnemonic=CTRY, unit=, value=Australia, descr=, original_mnemonic=CTRY)

Notice that :class:`lasio.SectionItems` plays a little trick here. It actually
sets the ``header_item.value`` attribute, instead of replacing the entire
:class:`lasio.HeaderItem` object.

You can set any of the attributes directly. Let's take an example from the ``~C`` section:

.. code-block:: python

    >>> las.curves
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=DEPTH, original_mnemonic=DEPT, data.shape=(121,)),
     CurveItem(mnemonic=CALI, unit=MM, value=, descr=CALI, original_mnemonic=CALI, data.shape=(121,)),
     CurveItem(mnemonic=DFAR, unit=G/CM3, value=, descr=DFAR, original_mnemonic=DFAR, data.shape=(121,)),
     CurveItem(mnemonic=DNEAR, unit=G/CM3, value=, descr=DNEAR, original_mnemonic=DNEAR, data.shape=(121,)),
     CurveItem(mnemonic=GAMN, unit=GAPI, value=, descr=GAMN, original_mnemonic=GAMN, data.shape=(121,)),
     CurveItem(mnemonic=NEUT, unit=CPS, value=, descr=NEUT, original_mnemonic=NEUT, data.shape=(121,)),
     CurveItem(mnemonic=PR, unit=OHM/M, value=, descr=PR, original_mnemonic=PR, data.shape=(121,)),
     CurveItem(mnemonic=SP, unit=MV, value=, descr=SP, original_mnemonic=SP, data.shape=(121,)),
     CurveItem(mnemonic=COND, unit=MS/M, value=, descr=COND, original_mnemonic=COND, data.shape=(121,))]
    >>> las.curves.PR.unit = 'ohmm'
    >>> las.curves.PR
    CurveItem(mnemonic=PR, unit=ohmm, value=, descr=PR, original_mnemonic=PR, data.shape=(121,))

Now let's look more closely at how to manipulate and add or remove items from
a section.

.. code-block:: python

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

.. code-block:: python

    >>> las.params.DREF.mnemonic = 'LMF'
    >>> las.params
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

And now we need to add a new mnemonic.

.. code-block:: python

    >>> las.params.DRILL = lasio.HeaderItem(mnemonic='DRILL', value='John Smith', descr='Driller on site')
    >>> las.params
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

What if we want to delete or remove an item? You can delete items the same way you
would remove an item from a dictionary. Let's remove the item we just added (DRILL):

.. code-block:: python

    >>> del las.well["DRILL"]
    
There are methods intended for removing curves. Say you want to remove the PR curve:

.. code-block:: python

    >>> las.delete_curve("PR")
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=DEPTH, original_mnemonic=DEPT, data.shape=(121,)),
     CurveItem(mnemonic=CALI, unit=MM, value=, descr=CALI, original_mnemonic=CALI, data.shape=(121,)),
     CurveItem(mnemonic=DFAR, unit=G/CM3, value=, descr=DFAR, original_mnemonic=DFAR, data.shape=(121,)),
     CurveItem(mnemonic=DNEAR, unit=G/CM3, value=, descr=DNEAR, original_mnemonic=DNEAR, data.shape=(121,)),
     CurveItem(mnemonic=GAMN, unit=GAPI, value=, descr=GAMN, original_mnemonic=GAMN, data.shape=(121,)),
     CurveItem(mnemonic=NEUT, unit=CPS, value=, descr=NEUT, original_mnemonic=NEUT, data.shape=(121,)),
     CurveItem(mnemonic=SP, unit=MV, value=, descr=SP, original_mnemonic=SP, data.shape=(121,)),
     CurveItem(mnemonic=COND, unit=MS/M, value=, descr=COND, original_mnemonic=COND, data.shape=(121,))]

.. warning:: Common mistake!

A common job is to iterate through the curves and remove all but a few that you are
interested in. When doing this, be careful to iterate over a **copy** of the curves
section:

.. code-block:: python

    >>> keep_curves = ['DEPT', 'DFAR', 'DNEAR']
    >>> for curve in las.curves[:]:
    ...     if curve.mnemonic not in keep_curves:
    ...        las.delete_curve(curve.mnemonic)
    ... 
    >>> las.curves
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=DEPTH, original_mnemonic=DEPT, data.shape=(121,)),
     CurveItem(mnemonic=DFAR, unit=G/CM3, value=, descr=DFAR, original_mnemonic=DFAR, data.shape=(121,)),
     CurveItem(mnemonic=DNEAR, unit=G/CM3, value=, descr=DNEAR, original_mnemonic=DNEAR, data.shape=(121,))]
    
Handling errors
---------------

lasio will do its best to read every line from the header section. If it can
make sense of it, it will parse it into a mnemonic, unit, value, and
description. However often there are problems in LAS files. For example, a
header section might contain something like:

.. code-block:: none

    COUNTY: RUSSELL

This line is missing a period. It should be ``COUNTY.    : RUSSELL``. Or
another example:

.. code-block:: none

    API       .                                          : API Number     (required if CTRY = US)
    "# Surface Coords: 1,000' FNL & 2,000' FWL"
    LATI      .DEG                                       : Latitude  - see Surface Coords comment above
    LONG      .DEG                                       : Longitude - see Surface Coords comment above

Obviously the line with " causes an error.

All these (and any other kind of error in the header section) can be turned
from LASHeaderError exceptions into :func:`logger.warning` calls instead by
using ``lasio.read(..., ignore_header_errors=True)``. Here is an example.
First we try reading a file without this argument:

.. code-block:: python

    >>> las = lasio.examples.open('dodgy_param_sect.las', ignore_header_errors=False)
    Unable to parse line as LAS header: DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD
    Traceback (most recent call last):
      File "C:\Users\kinve\code\lasio\lasio\reader.py", line 525, in parse_header_section
        values = read_line(line, section_name=parser.section_name2)
      File "C:\Users\kinve\code\lasio\lasio\reader.py", line 711, in read_line
        return read_header_line(*args, **kwargs)
      File "C:\Users\kinve\code\lasio\lasio\reader.py", line 780, in read_header_line
        mdict = m.groupdict()
    AttributeError: 'NoneType' object has no attribute 'groupdict'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\kinve\code\lasio\lasio\examples.py", line 46, in open
        return open_local_example(filename, **kwargs)
      File "C:\Users\kinve\code\lasio\lasio\examples.py", line 106, in open_local_example
        return LASFile(os.path.join(examples_path, *filename.split("/")), **kwargs)
      File "C:\Users\kinve\code\lasio\lasio\las.py", line 84, in __init__
        self.read(file_ref, **read_kwargs)
      File "C:\Users\kinve\code\lasio\lasio\las.py", line 222, in read
        mnemonic_case=mnemonic_case,
      File "C:\Users\kinve\code\lasio\lasio\las.py", line 142, in add_section
        raw_section, **sect_kws
      File "C:\Users\kinve\code\lasio\lasio\reader.py", line 536, in parse_header_section
        raise exceptions.LASHeaderError(message)
    lasio.exceptions.LASHeaderError: line 31 (section ~PARAMETER INFORMATION): "DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD"

Now if we use ``ignore_header_errors=True``:

.. code-block:: python

    >>> las = lasio.examples.open('dodgy_param_sect.las', ignore_header_errors=True)
    Unable to parse line as LAS header: DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD
    line 31 (section ~PARAMETER INFORMATION): "DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD"

Only a warning is issued, and the rest of the LAS file loads OK:

.. code-block:: python

    >>> las.params
    []
    >>> las.curves
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
     CurveItem(mnemonic=DT, unit=US/M, value=, descr=2  SONIC TRANSIT TIME, original_mnemonic=DT, data.shape=(3,)),
     CurveItem(mnemonic=RHOB, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=RHOB, data.shape=(3,)),
     CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
     CurveItem(mnemonic=SFLU, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=SFLA, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLA, data.shape=(3,)),
     CurveItem(mnemonic=ILM, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=ILM, data.shape=(3,)),
     CurveItem(mnemonic=ILD, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=ILD, data.shape=(3,))
    ]

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

Notice there are three curves with the mnemonic RES. When we load the file in,
lasio distinguishes between these duplicates:

.. code-block:: python

    >>> las = lasio.read('tests/examples/mnemonic_duplicate2.las')
    >>> las.curves
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
     CurveItem(mnemonic=DT, unit=US/M, value=, descr=2  SONIC TRANSIT TIME, original_mnemonic=DT, data.shape=(3,)),
     CurveItem(mnemonic=RHOB, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=RHOB, data.shape=(3,)),
     CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
     CurveItem(mnemonic=RXO, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=RXO, data.shape=(3,)),
     CurveItem(mnemonic=RES:1, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=RES, data.shape=(3,)),
     CurveItem(mnemonic=RES:2, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=RES, data.shape=(3,)),
     CurveItem(mnemonic=RES:3, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=RES, data.shape=(3,))
    ]
    >>> las.curves['RES:2']
    CurveItem(mnemonic=RES:2, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=RES, data.shape=(3,))

It remembers the original mnemonic, so when you write the file back out, they come back:

.. code-block:: python

    >>> from sys import stdout
    >>> las.write(stdout)
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

If there is a mix of upper and lower case characters in the mnemonics, by
default lasio will convert all mnemonics to uppercase to avoid problems with
producing the :1, :2, :3, and so on. There is a keyword argument which will
preserve the original formatting if that is what you prefer.

.. code-block:: python

    >>> las = lasio.read('tests/examples/mnemonic_case.las')
    >>> las.curves
    [CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:1, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:2, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:3, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:4, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:5, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,))
    ]
    >>> las = lasio.read('tests/examples/mnemonic_case.las', mnemonic_case='preserve')
    >>> las.curves
    [CurveItem(mnemonic=Dept, unit=M, value=, descr=1  DEPTH, original_mnemonic=Dept, data.shape=(3,)),
     CurveItem(mnemonic=Sflu, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=Sflu, data.shape=(3,)),
     CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:1, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=SFLU:2, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLU, data.shape=(3,)),
     CurveItem(mnemonic=sflu, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=sflu, data.shape=(3,)),
     CurveItem(mnemonic=SfLu, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=SfLu, data.shape=(3,))
    ]

