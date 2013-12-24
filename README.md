las_reader
==========

Planned API
-----------

Get an example file:

```python
>>> import urllib2, StringIO
>>> url = ('https://raw.github.com/kinverarity1/las-reader'
           '/master/standards/examples/1.2/sample_curve_api.las')
```

And read it in:
           
```python
>>> import las_reader           
>>> log = las_reader.read(url)
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
```

