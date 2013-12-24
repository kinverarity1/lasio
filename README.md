las_reader
==========

This is a Python package to read in Log ASCII (LAS) files, used in geophysical 
logging. The file format is specified by the 
[Canadian Well Logging Society](http://cwls.org/las_info.php). The package is
still a work in progress at the moment.

(planned) API
-------------

Read in an example LAS file:
           
```python
>>> import las_reader           
>>> log = las_reader.read('https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las')
>>> type(log)
las_reader.LASFile
```

The LASFile object has some provenance information depending on what was read. 
You can pass the ``read()`` function a filename, URL, file-like object, 
or string.

```python
>>> log.provenance
{'path': None, 
 'name': 'sample_curve_api.las',
 'url': 'https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las',
 'time_opened': datetime.datetime(2013, 12, 24, 20, 10, 2, 76000)
 }
```

The version and well sections are present as dictionaries:

```python
>>> log.version
{'VERS': 1.2, 'WRAP': False, 'DLM': ' '}
>>> log.well
{'COMP': 'ANY OIL COMPANY LTD.',
 'CTRY': None,
 'DATE': '25-DEC-1988',
 'FLD': 'EDAM',
 'LOC': 'A9-16-49-20W3M',
 'NULL': -999.25,
 'PROV': 'SASKATCHEWAN',
 'SRVC': 'ANY LOGGING COMPANY LTD.',
 'STEP': -0.125,
 'STEP.UNIT': 'M',
 'STOP': 1660.0,
 'STOP.UNIT': 'M',
 'STRT': 1670.0,
 'STRT.UNIT': 'M',
 'UWI': '100091604920W300',
 'WELL': 'ANY ET AL OIL WELL #12'}
```

