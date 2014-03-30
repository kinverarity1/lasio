LAS Reader
==========

``las_reader`` is a Python package to read in Log ASCII Standard (LAS) files, used in geophysical 
logging. The file format is specified by the 
[Canadian Well Logging Society](http://cwls.org/las_info.php). 

It works fine for 1.2 and 2.0 files, but not for 3.0 yet.

It isn't intended to make every little bit of information from the LAS file available --
this would be fairly straightforward for 1.2 and 2.0, but a bit of a headache for 3.0. The
intention is simply to get it in a useful format for numpy.

```python
>>> import las_reader
>>> l = las_reader.read('https://raw.githubusercontent.com/kinverarity1/las-reader/unstable/standards/examples/1.2/sample.las')
>>> type(l)
<class 'las_reader.las.Las'>
```

The curves in the LAS file are available as items of the ``Las`` object:

```python
>>> l.keys()
['DEPT', 'DT', 'RHOB', 'NPHI', 'SFLU', 'SFLA', 'ILM', 'ILD']
>>> type(l['DT'])
<type 'numpy.ndarray'>
```

You can also access the curves by their index:

```python
>>> id(l['RHOB'])
31526568
>>> id(l[2])
31526568
>>> id(l['ILM']) == id(l[-2])
True
```

The first curve in a LAS file is special, and usually either depth or time. You can
get to it by ``l[0]``.

Each of the metadata sections of the LAS file are shown as dictionaries 
(the ~Curves section is an OrderedDict) under their title as an attribute.
The value for each entry in the dictionary depends on the section. The
~Version, ~Well, and ~Other sections are simple:

```python
>>> l.version
{'VERS': 1.2,
 'WRAP': NO}
>>> l.well
{'STRT': 1670.0,
 'STOP': 1660.0,
 'STEP': -0.125,
 'NULL': -999.25,
 'COMP': # ANY OIL COMPANY LTD.,
 'WELL': ANY ET AL OIL WELL #12,
 'FLD': EDAM,
 'LOC': A9-16-49-20W3M,
 'PROV': SASKATCHEWAN,
 'SRVC': ANY LOGGING COMPANY LTD.,
 'DATE': 25-DEC-1988,
 'UWI': 100091604920W300}
```

The ~Curve and ~Parameter sections are a bit different. For each mnemonic it returns a
named tuple of the unit, API code/value, and description:

```python
{'DEPT': Curve(unit='M', API_code='', descr='1  DEPTH'),
 'DT': Curve(unit='US/M', API_code='', descr='2  SONIC TRANSIT TIME'),
 'RHOB': Curve(unit='K/M3', API_code='', descr='3  BULK DENSITY'),
 'NPHI': Curve(unit='V/V', API_code='', descr='4   NEUTRON POROSITY'),
 'SFLU': Curve(unit='OHMM', API_code='', descr='5  RXO RESISTIVITY'),
 'SFLA': Curve(unit='OHMM', API_code='', descr='6  SHALLOW RESISTIVITY'),
 'ILM': Curve(unit='OHMM', API_code='', descr='7  MEDIUM RESISTIVITY'),
 'ILD': Curve(unit='OHMM', API_code='', descr='8  DEEP RESISTIVITY')}
>>> l.params
{'BHT': Parameter(unit='DEGC', value='35.5000', descr='BOTTOM HOLE TEMPERATURE'),
 'BS': Parameter(unit='MM', value='200.0000', descr='BIT SIZE'),
 'FD': Parameter(unit='K/M3', value='1000.0000', descr='FLUID DENSITY'),
 'MATR': Parameter(unit=None, value='0.0000', descr='NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)'),
 'MDEN': Parameter(unit=None, value='2710.0000', descr='LOGGING MATRIX DENSITY'),
 'RMF': Parameter(unit='OHMM', value='0.2160', descr='MUD FILTRATE RESISTIVITY'),
 'DFD': Parameter(unit='K/M3', value='1525.0000', descr='DRILL FLUID DENSITY')}
```

The ~Other section is free text.

```python
>>> l.other
'Note: The logging tools became stuck at 625 meters causing the data\nbetween 625 meters and 615 meters to be invalid.'
 ```

Note that ``l.metadata`` is a single dictionary which combines the ~Version, ~Well, ~Parameters, 
and ~Other sections, and returns the "value" attribute for each of the items in the ~Parameters section. 
Also depending on how you opened the file there could be useful information
inside ``l.provenance``:

```python
>>> l.provenance
{'url': 'https://raw.githubusercontent.com/kinverarity1/las-reader/unstable/standards/examples/1.2/sample.las', 'path': None, 'time_opened': datetime.datetime(2014, 3, 30, 20, 3, 25, 836000), 'name': 'sample.las'}
```

