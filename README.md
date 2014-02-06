las_reader
==========

This is a Python package to read in Log ASCII Standard (LAS) files, used in geophysical 
logging. The file format is specified by the 
[Canadian Well Logging Society](http://cwls.org/las_info.php). It works fine for 1.2 and
2.0 files, but not for 3.0 yet.

The object for a LAS file is surprisingly named ``LASFile``. It gives you access to the
raw data and metadata, and also some useful shortcut methods. A slightly contrived 
example is:

```python
>>> l = las_reader.LASFile('/path/to/something.las')
>>> type(l.data)
<pandas.DataFrame object>
>>> l.data.keys()
['DEPT', 'GAPI', 'CALI', 'NEUT']
>>> len(l.data)
5330
>>> l.traces()
[('GAPI', <pandas.Series object...>),
 ('CALI', <pandas.Series object...>),
 ('NEUT', <pandas.Series object...>)]
>>> l.metadata_list()
[('UWI', '1234-56789'),
 ('SRVC', 'Department of Mines'),
 ...]
```
   
Data traces/curves are basically [numpy][1] ndarrays indexed by depth, in the form of [pandas][2]
``Series`` and ``DataFrame`` objects. For more details see [the pandas documentation][3].

[1]: http://www.numpy.org/
[2]: http://pandas.pydata.org/ "Python Data Analysis Library"
[3]: http://pandas.pydata.org/pandas-docs/dev/dsintro.html

Examples
--------

- [reading and viewing a log file (1.2)](http://nbviewer.ipython.org/github/kinverarity1/las-reader/blob/master/docs/reading%20and%20viewing%20a%20log%20file%20%281.2%29.ipynb)
- [reading a large log file (1.2)](http://nbviewer.ipython.org/github/kinverarity1/las-reader/blob/master/docs/reading%20a%20large%20log%20file%20%281.2%29.ipynb)
- [reading some real-life data from a LAS 2.0 file](http://nbviewer.ipython.org/github/kinverarity1/las-reader/blob/master/docs/reading%20some%20real-life%20data%20from%20a%20LAS%202.0%20file.ipynb)

