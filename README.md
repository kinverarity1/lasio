las_reader
==========

This is a Python package to read in Log ASCII Standard (LAS) files, used in geophysical 
logging. The file format is specified by the 
[Canadian Well Logging Society](http://cwls.org/las_info.php). It works fine for 1.2 and
2.0 files, but not for 3.0 yet.

It isn't intended to make every little bit of information from the LAS file available --
this would be fairly straightforward for 1.2 and 2.0, but a bit of a headache for 3.0. The
intention is simply to get it in a useful format for ``numpy``.

The below exmaple is yet to be fully implemented (see [readme-driven development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)). 

```python
>>> import las_reader
>>> l = las_reader.read('/path/to/example.las')
>>> type(l)
<las_reader.Las object>
```

The curves in the LAS file are available as items of the ``Las`` object:

```python
>>> l.keys()
['DEPT', 'GAPI', 'CALI', 'NEUT']
>>> type(l['CALI'])
<numpy.ndarray>
```

You can also access the curves by their index:

```python
>>> id(l['GAPI'])
12342345
>>> id(l[1])                                    # index 1 is the second curve
12342345
>>> id(l[-2]) == id(l['CALI'])
True
```

The first curve in a LAS file is special, and usually either depth or time. You can
get to it by ``l[0]``, or ``l.index``.

Each of the metadata sections of the LAS file are shown as dictionaries 
(the ~Curves section is an OrderedDict) under their title as an attribute.
The value for each entry in the dictionary depends on the section. The
~Version, ~Well, and ~Other sections are simple:

```python
>>> from pprint import pprint
>>> pprint(l.version)
{'VERS': 1.2,
 'WRAP': 'NO'}
>>> pprint(l.well)
{'STRT': 1670.0,
 'STOP': 1660.0,
 'STEP': -0.125,
 'NULL': -999.25
 'COMP': 'ANY OIL COMPANY LTD.',
 'WELL': 'ANY ET AL OIL WELL #12',
 'FLD': 'EDAM',
 'LOC': 'A9-16-49-20W3M',
 'PROV': 'SASKATCHEWAN',
 'SRVC': 'ANY LOGGING COMPANY LTD.',
 'DATE': '25-DEC-1988',
 'UWI': '100091604920W300'}
```

The ~Curve and ~Parameter sections are a bit different. For each mnemonic it returns a
named tuple of the unit, API code/value, and description:

```python
>>> type(l.curves)
<collections.OrderedDict object>
>>> pprint(l.curves)
{'DEPT': Curve(unit='M', API_code='', descr='1  DEPTH'),
 'DT': Curve(unit='US/M', API_code='', descr='2  SONIC TRANSIT TIME'),
 'RHOB': Curve(unit='K/M3', API_code='', descr='3  BULK DENSITY')}
>>> type(l.params)
<dict>
>>> pprint(l.params)
{'BHT': Param(unit='DEGC', value=35.5, descr='BOTTOM HOLE TEMPERATURE'),
 ...}
```

The ~Other section depends on what it finds. Some software writes LAS files with key:value
pairs in the ~Other section, when they should really be in the ~Well section. Of course
the Log ASCII Standard allows free text in the ~Other section though. The way I
handle this is to have a dictionary with an attribute "text" for any free text, with any
key:values separately in the dictionary:

```python
>>> pprint(l.other)
{'text': '     Note: The logging tools became stuck at 625 meters causing the data\n       between 625 meters and 615 meters to be invalid.',
 'ENGI': 'R. Givens',
 'LUN': 'T3363',
 'LATI': '39DEG12.248',
 'LONG': '124DEG41.091'}
 ```

Note that ``l.metadata`` is a single dictionary which combines the ~Version, ~Well, ~Parameters, 
and ~Other sections, and returns the "value" attribute for each of the items in the ~Parameters section. 
Also depending on how you opened the file there could be useful information
inside ``l.provenance``:

```python
>>> pprint(l.provenance)
{}
```

