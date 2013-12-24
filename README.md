las_reader
==========

usage
-----

Read in an example LAS file:
           
```python
>>> import las_reader           
>>> log = las_reader.read('https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las')
>>> type(log)
las_reader.LASFile
```

You should get provenance metadata depending on what was read (a filename,
URL, file-like object, or string).

```python
>>> log.provenance
{'path': None, 
 'name': 'sample_curve_api.las',
 'url': 'https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las',
 'time_opened': datetime.datetime(2013, 12, 24, 20, 10, 2, 76000)
 }
```

The version and well sections are always there:

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

