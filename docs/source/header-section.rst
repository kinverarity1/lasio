Header section metadata
=======================

Tutorial
--------

One of the primary motivations in writing lasio was to be able to reliably
parse LAS header sections. This is working well for LAS 1.2 and 2.0
files, and partially for LAS 3.0 files. 

.. note::

   lasio does not require LAS files to be strictly compliant with the standards,
   and you should not expect lasio to raise an exception or error for files which
   are clearly not conforming to the standards. The goal of lasio is to parse
   metadata and data quietly, not to fail unnecessarily.

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
    [HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS LOG ASCII STANDA"),
     HeaderItem(mnemonic="WRAP", unit="", value="NO", descr="ONE LINE PER DEPTH STE")]

    >>> las.version
    [HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS LOG ASCII STANDA"),
     HeaderItem(mnemonic="WRAP", unit="", value="NO", descr="ONE LINE PER DEPTH STE")]

Sections themselves are represented by :class:`lasio.SectionItems`
objects. This is a ``list`` which has been extended to allow you to access the
items within by their mnemonic:

.. code-block:: python

    >>> las.version.VERS
    HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS LOG ASCII STANDA")
    >>> las.version['VERS']
    HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS LOG ASCII STANDA")
    >>> las.version[0]
    HeaderItem(mnemonic="VERS", unit="", value="2.0", descr="CWLS LOG ASCII STANDA")

As you can see, either attribute-style or item-style access is fine.

Let's take a look at the next special section, ``~W``:

.. code-block:: python

    >>> las.well
     [HeaderItem(mnemonic="STRT", unit="M", value="0.05", descr="FIRST INDEX VALUE"),
      HeaderItem(mnemonic="STOP", unit="M", value="136.6", descr="LAST INDEX VALUE"),
      HeaderItem(mnemonic="STEP", unit="M", value="0.05", descr="STEP"),
      HeaderItem(mnemonic="NULL", unit="", value="-99999", descr="NULL VALUE"),
      HeaderItem(mnemonic="COMP", unit="", value="", descr="COMP"),
      HeaderItem(mnemonic="WELL", unit="", value="Scorpio E1", descr="WELL"),
      HeaderItem(mnemonic="FLD", unit="", value="", descr=""),
      HeaderItem(mnemonic="LOC", unit="", value="Mt Eba", descr="LOC"),
      HeaderItem(mnemonic="SRVC", unit="", value="", descr=""),
      HeaderItem(mnemonic="CTRY", unit="", value="", descr=""),
      HeaderItem(mnemonic="STAT", unit="", value="SA", descr="STAT"),
      HeaderItem(mnemonic="CNTY", unit="", value="", descr=""),
      HeaderItem(mnemonic="DATE", unit="", value="15/03/2015", descr="DATE"),
      HeaderItem(mnemonic="UWI", unit="", value="6038-187", descr="WUNT")]

The CTRY item is blank. We will set it:

.. code-block:: python

    >>> las.well.CTRY = 'Australia'
    >>> las.well.CTRY
    HeaderItem(mnemonic="CTRY", unit="", value="Australia", descr="")

Notice that :class:`lasio.SectionItems` plays a little trick here. It actually
sets the ``header_item.value`` attribute, instead of replacing the entire
:class:`lasio.HeaderItem` object.

You can set any of the attributes directly. Let's take an example from the ``~C`` section:

.. code-block:: python

    >>> las.curves
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="DEPTH", original_mnemonic="DEPT", data.shape=(121,)),
     CurveItem(mnemonic="CALI", unit="MM", value="", descr="CALI", original_mnemonic="CALI", data.shape=(121,)),
     CurveItem(mnemonic="DFAR", unit="G/CM3", value="", descr="DFAR", original_mnemonic="DFAR", data.shape=(121,)),
     CurveItem(mnemonic="DNEAR", unit="G/CM3", value="", descr="DNEAR", original_mnemonic="DNEAR", data.shape=(121,)),
     CurveItem(mnemonic="GAMN", unit="GAPI", value="", descr="GAMN", original_mnemonic="GAMN", data.shape=(121,)),
     CurveItem(mnemonic="NEUT", unit="CPS", value="", descr="NEUT", original_mnemonic="NEUT", data.shape=(121,)),
     CurveItem(mnemonic="PR", unit="OHM/M", value="", descr="PR", original_mnemonic="PR", data.shape=(121,)),
     CurveItem(mnemonic="SP", unit="MV", value="", descr="SP", original_mnemonic="SP", data.shape=(121,)),
     CurveItem(mnemonic="COND", unit="MS/M", value="", descr="COND", original_mnemonic="COND", data.shape=(121,))]
    >>> las.curves.PR.unit = 'ohmm'
    >>> las.curves.PR
    CurveItem(mnemonic="PR", unit="ohmm", value="", descr="PR", original_mnemonic="PR", data.shape=(121,))

Now let's look more closely at how to manipulate and add or remove items from
a section.

.. code-block:: python

    In [195]: las.params
    Out[195]:
    [HeaderItem(mnemonic="BS", unit="", value="216 mm", descr="BS"),
     HeaderItem(mnemonic="JOBN", unit="", value="", descr="JOBN"),
     HeaderItem(mnemonic="WPMT", unit="", value="", descr="WPMT"),
     HeaderItem(mnemonic="AGL", unit="", value="", descr="AGL"),
     HeaderItem(mnemonic="PURP", unit="", value="Cased hole stratigraphy", descr="P"),
     HeaderItem(mnemonic="X", unit="", value="560160", descr="X"),
     HeaderItem(mnemonic="CSGL", unit="", value="0 m - 135 m", descr="CSGL"),
     HeaderItem(mnemonic="UNIT", unit="", value="", descr="UNIT"),
     HeaderItem(mnemonic="Y", unit="", value="6686430", descr="Y"),
     HeaderItem(mnemonic="TDL", unit="", value="135.2 m", descr="TDL"),
     HeaderItem(mnemonic="PROD", unit="", value="", descr="PROD"),
     HeaderItem(mnemonic="MUD", unit="", value="Water", descr="MUD"),
     HeaderItem(mnemonic="CSGS", unit="", value="100 mm", descr="CSGS"),
     HeaderItem(mnemonic="ENG", unit="", value="", descr="ENG"),
     HeaderItem(mnemonic="STEP", unit="", value="5 cm", descr="STEP"),
     HeaderItem(mnemonic="FLUIDLEVEL", unit="", value="54 m", descr="FluidLevel"),
     HeaderItem(mnemonic="CSGT", unit="", value="PVC", descr="CSGT"),
     HeaderItem(mnemonic="WIT", unit="", value="", descr="WIT"),
     HeaderItem(mnemonic="EREF", unit="", value="", descr="EREF"),
     HeaderItem(mnemonic="PROJ", unit="", value="", descr="PROJ"),
     HeaderItem(mnemonic="ZONE", unit="", value="53J", descr="ZONE"),
     HeaderItem(mnemonic="DREF", unit="", value="GL", descr="DREF"),
     HeaderItem(mnemonic="TDD", unit="", value="136 m", descr="TDD")]

We want to rename the DREF mnemonic as LMF. We can do so by changing the
``header_item.mnemonic`` attribute.

.. code-block:: python

    >>> las.params.DREF.mnemonic = 'LMF'
    >>> las.params
    [HeaderItem(mnemonic="BS", unit="", value="216 mm", descr="BS"),
     HeaderItem(mnemonic="JOBN", unit="", value="", descr="JOBN"),
     HeaderItem(mnemonic="WPMT", unit="", value="", descr="WPMT"),
     HeaderItem(mnemonic="AGL", unit="", value="", descr="AGL"),
     HeaderItem(mnemonic="PURP", unit="", value="Cased hole stratigraphy", descr="P"),
     HeaderItem(mnemonic="X", unit="", value="560160", descr="X"),
     HeaderItem(mnemonic="CSGL", unit="", value="0 m - 135 m", descr="CSGL"),
     HeaderItem(mnemonic="UNIT", unit="", value="", descr="UNIT"),
     HeaderItem(mnemonic="Y", unit="", value="6686430", descr="Y"),
     HeaderItem(mnemonic="TDL", unit="", value="135.2 m", descr="TDL"),
     HeaderItem(mnemonic="PROD", unit="", value="", descr="PROD"),
     HeaderItem(mnemonic="MUD", unit="", value="Water", descr="MUD"),
     HeaderItem(mnemonic="CSGS", unit="", value="100 mm", descr="CSGS"),
     HeaderItem(mnemonic="ENG", unit="", value="", descr="ENG"),
     HeaderItem(mnemonic="STEP", unit="", value="5 cm", descr="STEP"),
     HeaderItem(mnemonic="FLUIDLEVEL", unit="", value="54 m", descr="FluidLevel"),
     HeaderItem(mnemonic="CSGT", unit="", value="PVC", descr="CSGT"),
     HeaderItem(mnemonic="WIT", unit="", value="", descr="WIT"),
     HeaderItem(mnemonic="EREF", unit="", value="", descr="EREF"),
     HeaderItem(mnemonic="PROJ", unit="", value="", descr="PROJ"),
     HeaderItem(mnemonic="ZONE", unit="", value="53J", descr="ZONE"),
     HeaderItem(mnemonic="LMF", unit="", value="GL", descr="DREF"),
     HeaderItem(mnemonic="TDD", unit="", value="136 m", descr="TDD")]

And now we need to add a new mnemonic.

.. code-block:: python

    >>> las.params.DRILL = lasio.HeaderItem(mnemonic='DRILL', value='John Smith', descr='Driller on site')
    >>> las.params
    [HeaderItem(mnemonic="BS", unit="", value="216 mm", descr="BS"),
     HeaderItem(mnemonic="JOBN", unit="", value="", descr="JOBN"),
     HeaderItem(mnemonic="WPMT", unit="", value="", descr="WPMT"),
     HeaderItem(mnemonic="AGL", unit="", value="", descr="AGL"),
     HeaderItem(mnemonic="PURP", unit="", value="Cased hole stratigraphy", descr="P"),
     HeaderItem(mnemonic="X", unit="", value="560160", descr="X"),
     HeaderItem(mnemonic="CSGL", unit="", value="0 m - 135 m", descr="CSGL"),
     HeaderItem(mnemonic="UNIT", unit="", value="", descr="UNIT"),
     HeaderItem(mnemonic="Y", unit="", value="6686430", descr="Y"),
     HeaderItem(mnemonic="TDL", unit="", value="135.2 m", descr="TDL"),
     HeaderItem(mnemonic="PROD", unit="", value="", descr="PROD"),
     HeaderItem(mnemonic="MUD", unit="", value="Water", descr="MUD"),
     HeaderItem(mnemonic="CSGS", unit="", value="100 mm", descr="CSGS"),
     HeaderItem(mnemonic="ENG", unit="", value="", descr="ENG"),
     HeaderItem(mnemonic="STEP", unit="", value="5 cm", descr="STEP"),
     HeaderItem(mnemonic="FLUIDLEVEL", unit="", value="54 m", descr="FluidLevel"),
     HeaderItem(mnemonic="CSGT", unit="", value="PVC", descr="CSGT"),
     HeaderItem(mnemonic="WIT", unit="", value="", descr="WIT"),
     HeaderItem(mnemonic="EREF", unit="", value="", descr="EREF"),
     HeaderItem(mnemonic="PROJ", unit="", value="", descr="PROJ"),
     HeaderItem(mnemonic="ZONE", unit="", value="53J", descr="ZONE"),
     HeaderItem(mnemonic="LMF", unit="", value="GL", descr="DREF"),
     HeaderItem(mnemonic="TDD", unit="", value="136 m", descr="TDD"),
     HeaderItem(mnemonic="DRILL", unit="", value="John Smith", descr="Driller on si")]

Bingo.

What if we want to delete or remove an item? You can delete items the same way you
would remove an item from a dictionary. Let's remove the item we just added (DRILL):

.. code-block:: python

    >>> del las.well["DRILL"]
    
There are methods intended for removing curves. Say you want to remove the PR curve:

.. code-block:: python

    >>> las.delete_curve("PR")
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="DEPTH", original_mnemonic="DEPT", data.shape=(121,)),
     CurveItem(mnemonic="CALI", unit="MM", value="", descr="CALI", original_mnemonic="CALI", data.shape=(121,)),
     CurveItem(mnemonic="DFAR", unit="G/CM3", value="", descr="DFAR", original_mnemonic="DFAR", data.shape=(121,)),
     CurveItem(mnemonic="DNEAR", unit="G/CM3", value="", descr="DNEAR", original_mnemonic="DNEAR", data.shape=(121,)),
     CurveItem(mnemonic="GAMN", unit="GAPI", value="", descr="GAMN", original_mnemonic="GAMN", data.shape=(121,)),
     CurveItem(mnemonic="NEUT", unit="CPS", value="", descr="NEUT", original_mnemonic="NEUT", data.shape=(121,)),
     CurveItem(mnemonic="SP", unit="MV", value="", descr="SP", original_mnemonic="SP", data.shape=(121,)),
     CurveItem(mnemonic="COND", unit="MS/M", value="", descr="COND", original_mnemonic="COND", data.shape=(121,))]


.. warning:: 

    Common mistake!

    A common job is to iterate through the curves and remove all but a few that you are
    interested in. When doing this, be careful to iterate over a **copy** of the curves
    section. See example below.

.. code-block:: python

    >>> keep_curves = ['DEPT', 'DFAR', 'DNEAR']
    >>> for curve in las.curves[:]:
    ...     if curve.mnemonic not in keep_curves:
    ...        las.delete_curve(curve.mnemonic)
    ... 
    >>> las.curves
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="DEPTH", original_mnemonic="DEPT", data.shape=(121,)),
     CurveItem(mnemonic="DFAR", unit="G/CM3", value="", descr="DFAR", original_mnemonic="DFAR", data.shape=(121,)),
     CurveItem(mnemonic="DNEAR", unit="G/CM3", value="", descr="DNEAR", original_mnemonic="DNEAR", data.shape=(121,))]

Another common task is to retrieve a header item that may or may not be in the
file. If you try ordinary item-style access,
as is normal in Python, a KeyError exception will be raised if it is missing:

.. code-block:: python

    >>> permit = las.well['PRMT']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "c:\devapps\kinverarity\projects\lasio\lasio\las_items.py", line 313, in __getitem__
        raise KeyError("%s not in %s" % (key, self.keys()))
    KeyError: "PRMT not in ['STRT', 'STOP', 'STEP', 'NULL', 'COMP', 'WELL', 'FLD', 'LOC', 'PROV', 'SRVC', 'DATE', 'UWI']"

A better pattern is to use the :meth:`lasio.SectionItems.get` method, which
allows you to specify a default value in the case of it missing:

.. code-block:: python

    >>> permit = las.well.get('PRMT', 'unknown')
    >>> permit
    HeaderItem(mnemonic="PRMT", unit="", value="unknown", descr="")

You can use the ``add=True`` keyword argument if you would like this 
header item to be added, as well as returned:

.. code-block:: python

    >>> permit = las.well.get('PRMT', 'unknown', add=True)
    >>> las.well
    [HeaderItem(mnemonic="STRT", unit="M", value="0.05", descr="FIRST INDEX VALUE"),
    HeaderItem(mnemonic="STOP", unit="M", value="136.6", descr="LAST INDEX VALUE"),
    HeaderItem(mnemonic="STEP", unit="M", value="0.05", descr="STEP"),
    HeaderItem(mnemonic="NULL", unit="", value="-99999", descr="NULL VALUE"),
    HeaderItem(mnemonic="COMP", unit="", value="", descr="COMP"),
    HeaderItem(mnemonic="WELL", unit="", value="Scorpio E1", descr="WELL"),
    HeaderItem(mnemonic="FLD", unit="", value="", descr=""),
    HeaderItem(mnemonic="LOC", unit="", value="Mt Eba", descr="LOC"),
    HeaderItem(mnemonic="SRVC", unit="", value="", descr=""),
    HeaderItem(mnemonic="CTRY", unit="", value="", descr=""),
    HeaderItem(mnemonic="STAT", unit="", value="SA", descr="STAT"),
    HeaderItem(mnemonic="CNTY", unit="", value="", descr=""),
    HeaderItem(mnemonic="DATE", unit="", value="15/03/2015", descr="DATE"),
    HeaderItem(mnemonic="UWI", unit="", value="6038-187", descr="WUNT"),
    HeaderItem(mnemonic="PRMT", unit="", value="unknown", descr="")]

Handling special cases of header lines
--------------------------------------

lasio will do its best to read every line from the header section. Some examples
follow for unusual formattings:

Comment lines mixed with header lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lasio will, by default, treat header lines starting with a "#" hash string as a
comment line and ignore it. Spaces before the "#" are stripped off before
checking for the "#".

To modify which strings indicate comment lines to ignore pass an
ignore_comments tuple to ``lasio.read()`` or ``lasio.examples.open()``.

Example:
  ``lasio.read(file, ignore_comments=("#", "%MyComment")``

Lines without periods
~~~~~~~~~~~~~~~~~~~~~

For example take these lines from a LAS file header section:

.. code-block:: none

              DRILLED  :12/11/2010
              PERM DAT :1
              TIME     :14:00:32
              HOLE DIA :85.7

These lines are missing periods between the mnemonic and colon, e.g. a properly
formatted version would be ``DRILLED. :12/11/2010``.

However, lasio will parse them silently, and correctly, e.g. for the last
line the mnemonic will be ``HOLE DIA`` and the value will be ``85.7``, with the
description blank.

Lines with colons in the mnemonic and description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Colons are used as a delimiter, but colons can also occur inside the unit, value, and
description fields in a LAS file header. Take this line as an example:

.. code-block:: none

    TIML.hh:mm 23:15 23-JAN-2001:   Time Logger: At Bottom

lasio will parse this correctly such that the unit is ``hh:mm``, the value is
``23:15 21-JAN-2001``, and the description is ``Time Logger: At Bottom``.

Units containing periods
~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly, periods are used as delimiters, but can also occur as part of the
unit field's value, such as in the case of a unit of tenths of an inch (``.1IN``):

.. code-block:: none

    TDEP  ..1IN                      :  0.1-in

lasio will parse the mnemonic as ``TDEP`` and the unit as ``.1IN``.

If there are two adjoining periods, the same behaviour applies:

.. code-block:: none

    TDEP..1IN                      :  0.1-in

lasio parses this line as having mnemonic ``TDEP`` and unit ``.1IN``.

Special case for units which contain spaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normally, any whitespace following the unit in a LAS header line delimits
the unit from the value. lasio has a special exception for units which may
appear with a space. Currently the only one recognised is ``1000 lbf``:

.. code-block:: none

    HKLA            .1000 lbf                                  :(RT)

This is parsed as mnemonic ``HKLA``, unit ``1000 lbf``, and value blank, contrary
to the usual behaviour which would result in unit ``1000`` and value ``lbf``.

Please raise a `GitHub issue <https://github.com/kinverarity1/lasio/issues/new/choose>`__ 
for any other units which should be handled in this way.

Mnemonics which contain a period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with other LAS file parsers, lasio does not parse mnemonics which contain
a period - instead, anything after the period will be parsed as the unit:

.. code-block:: none

    SP.COND .US/M                      :  EC at 25 deg C

results in mnemonic ``SP``, unit ``COND``, and value ``.US/CM``.

.. warning::

    These files are non-conforming, and difficult to anticipate.

Handling errors silently (``ignore_header_errors=True``)
--------------------------------------------------------

Sometimes lasio cannot make sense of a header line at all. For example:

.. code-block:: none

    API       .                                          : API Number     (required if CTRY = US)
    "# Surface Coords: 1,000' FNL & 2,000' FWL"
    LATI      .DEG                                       : Latitude  - see Surface Coords comment above
    LONG      .DEG                                       : Longitude - see Surface Coords comment above

The line with ``"`` causes an exception to be raised by default. 

Another example is this ~Param section in a LAS file:

.. code-block:: none

   ~PARAMETER INFORMATION
   DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD

This isn't a header line, and cannot be parsed as such. It results in a
``LASHeaderError`` exception being raised:

.. code-block:: python

    >>> las = lasio.examples.open('dodgy_param_sect.las', ignore_header_errors=False)

.. code-block:: console

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

However, these can be converted from ``LASHeaderError`` exceptions into 
``logger.warning()`` calls instead by using 
``lasio.read(..., ignore_header_errors=True)``:

.. code-block:: python

    >>> las = lasio.examples.open('dodgy_param_sect.las', ignore_header_errors=True)
    Unable to parse line as LAS header: DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD
    line 31 (section ~PARAMETER INFORMATION): "DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD"

Only a warning is issued, and the rest of the LAS file loads OK:

.. code-block:: python

    >>> las.params
    []
    >>> las.curves
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="1  DEPTH", original_mnemonic="DEPT", data.shape=(3,)),
     CurveItem(mnemonic="DT", unit="US/M", value="", descr="2  SONIC TRANSIT TIME", original_mnemonic="DT", data.shape=(3,)),
     CurveItem(mnemonic="RHOB", unit="K/M3", value="", descr="3  BULK DENSITY", original_mnemonic="RHOB", data.shape=(3,)),
     CurveItem(mnemonic="NPHI", unit="V/V", value="", descr="4   NEUTRON POROSITY", original_mnemonic="NPHI", data.shape=(3,)),
     CurveItem(mnemonic="SFLU", unit="OHMM", value="", descr="5  RXO RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="SFLA", unit="OHMM", value="", descr="6  SHALLOW RESISTIVITY", original_mnemonic="SFLA", data.shape=(3,)),
     CurveItem(mnemonic="ILM", unit="OHMM", value="", descr="7  MEDIUM RESISTIVITY", original_mnemonic="ILM", data.shape=(3,)),
     CurveItem(mnemonic="ILD", unit="OHMM", value="", descr="8  DEEP RESISTIVITY", original_mnemonic="ILD", data.shape=(3,))
    ]

If you are dealing with "messy" LAS data, it might be good to consider using
``ignore_header_errors=True``.

Handling duplicate mnemonics
----------------------------

Take this LAS file as an example, containing this ~C section:

.. code-block:: none

    ~CURVE INFORMATION
    DEPT.M                     :  1  DEPTH
    DT  .US/M                  :  2  SONIC TRANSIT TIME
    RHOB.K/M3                  :  3  BULK DENSITY
    NPHI.V/V                   :  4   NEUTRON POROSITY
    RXO.OHMM                   :  5  RXO RESISTIVITY
    RES.OHMM                   :  6  SHALLOW RESISTIVITY
    RES.OHMM                   :  7  MEDIUM RESISTIVITY
    RES.OHMM                   :  8  DEEP RESISTIVITY

Notice there are three curves with the mnemonic RES. When we load the file in,
lasio distinguishes between these duplicates by appending ``:1``, ``:2``, and
so on, to the duplicated mnemonic:

.. code-block:: python

    >>> las = lasio.read('tests/examples/mnemonic_duplicate2.las')
    >>> las.curves
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="1  DEPTH", original_mnemonic="DEPT", data.shape=(3,)),
     CurveItem(mnemonic="DT", unit="US/M", value="", descr="2  SONIC TRANSIT TIME", original_mnemonic="DT", data.shape=(3,)),
     CurveItem(mnemonic="RHOB", unit="K/M3", value="", descr="3  BULK DENSITY", original_mnemonic="RHOB", data.shape=(3,)),
     CurveItem(mnemonic="NPHI", unit="V/V", value="", descr="4   NEUTRON POROSITY", original_mnemonic="NPHI", data.shape=(3,)),
     CurveItem(mnemonic="RXO", unit="OHMM", value="", descr="5  RXO RESISTIVITY", original_mnemonic="RXO", data.shape=(3,)),
     CurveItem(mnemonic="RES:1", unit="OHMM", value="", descr="6  SHALLOW RESISTIVITY", original_mnemonic="RES", data.shape=(3,)),
     CurveItem(mnemonic="RES:2", unit="OHMM", value="", descr="7  MEDIUM RESISTIVITY", original_mnemonic="RES", data.shape=(3,)),
     CurveItem(mnemonic="RES:3", unit="OHMM", value="", descr="8  DEEP RESISTIVITY", original_mnemonic="RES", data.shape=(3,))
    ]
    >>> las.curves['RES:2']
    CurveItem(mnemonic="RES:2", unit="OHMM", value="", descr="7  MEDIUM RESISTIVITY", original_mnemonic="RES", data.shape=(3,))

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
    [CurveItem(mnemonic="DEPT", unit="M", value="", descr="1  DEPTH", original_mnemonic="DEPT", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:1", unit="K/M3", value="", descr="3  BULK DENSITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="NPHI", unit="V/V", value="", descr="4   NEUTRON POROSITY", original_mnemonic="NPHI", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:2", unit="OHMM", value="", descr="5  RXO RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:3", unit="OHMM", value="", descr="6  SHALLOW RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:4", unit="OHMM", value="", descr="7  MEDIUM RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:5", unit="OHMM", value="", descr="8  DEEP RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,))
    ]
    >>> las = lasio.read('tests/examples/mnemonic_case.las', mnemonic_case='preserve')
    >>> las.curves
    [CurveItem(mnemonic="Dept", unit="M", value="", descr="1  DEPTH", original_mnemonic="Dept", data.shape=(3,)),
     CurveItem(mnemonic="Sflu", unit="K/M3", value="", descr="3  BULK DENSITY", original_mnemonic="Sflu", data.shape=(3,)),
     CurveItem(mnemonic="NPHI", unit="V/V", value="", descr="4   NEUTRON POROSITY", original_mnemonic="NPHI", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:1", unit="OHMM", value="", descr="5  RXO RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="SFLU:2", unit="OHMM", value="", descr="6  SHALLOW RESISTIVITY", original_mnemonic="SFLU", data.shape=(3,)),
     CurveItem(mnemonic="sflu", unit="OHMM", value="", descr="7  MEDIUM RESISTIVITY", original_mnemonic="sflu", data.shape=(3,)),
     CurveItem(mnemonic="SfLu", unit="OHMM", value="", descr="8  DEEP RESISTIVITY", original_mnemonic="SfLu", data.shape=(3,))
    ]

