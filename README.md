# lasio

![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Version](http://img.shields.io/pypi/v/lasio.svg)](https://pypi.python.org/pypi/lasio/)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kinverarity1/lasio/blob/master/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/lasio.svg)](https://www.python.org/downloads/)
[![Build Status](https://travis-ci.org/kinverarity1/lasio.svg?branch=master)](https://travis-ci.org/kinverarity1/lasio)
[![Build status](https://ci.appveyor.com/api/projects/status/csr7bg8urkbtbq4n?svg=true)](https://ci.appveyor.com/project/kinverarity1/lasio)
[![Docker Build](https://img.shields.io/docker/build/kinverarity/lasio.svg)](https://hub.docker.com/r/kinverarity/lasio/)

This is a Python 2.7 and 3.3+ package to read and write Log ASCII Standard (LAS) files, used for borehole data such as geophysical, geological, or petrophysical logs. It's compatible with versions 1.2 and 2.0 of the LAS file specification, published by the [Canadian Well Logging Society](http://www.cwls.org/las). Support for LAS 3 is being worked on. In principle it is designed to read as many types of LAS files as possible, including ones containing common errors or non-compliant formatting.

Depending on your particular application you may also want to check out [striplog](https://github.com/agile-geoscience/striplog) for stratigraphic/lithological data, or [welly](https://github.com/agile-geoscience/welly) for dealing with data at the well level. lasio is primarily for reading & writing LAS files.

Note this is *not* a package for reading LiDAR data (also called "LAS files").

## Documentation

See here for the [complete lasio package documentation](https://lasio.readthedocs.io/en/latest/).

## Quick start

Install the usual way:

```bash
$ pip install lasio
```

Very quick example session:

```python
>>> import lasio
>>> las = lasio.read("sample_big.las")
```

Data is accessible both directly as numpy arrays

```python
>>> las.keys()
['DEPT', 'DT', 'RHOB', 'NPHI', 'SFLU', 'SFLA', 'ILM', 'ILD']
>>> las['SFLU']
array([ 123.45,  123.45,  123.45, ...,  123.45,  123.45,  123.45])
>>> las['DEPT']
array([ 1670.   ,  1669.875,  1669.75 , ...,  1669.75 ,  1670.   ,
        1669.875])
```

and as ``CurveItem`` objects with associated metadata:

```python
>>> las.curves
[CurveItem(mnemonic=DEPT, unit=M, value=, descr=1  DEPTH, original_mnemonic=DEPT, data.shape=(29897,)), 
CurveItem(mnemonic=DT, unit=US/M, value=, descr=2  SONIC TRANSIT TIME, original_mnemonic=DT, data.shape=(29897,)), 
CurveItem(mnemonic=RHOB, unit=K/M3, value=, descr=3  BULK DENSITY, original_mnemonic=RHOB, data.shape=(29897,)), 
CurveItem(mnemonic=NPHI, unit=V/V, value=, descr=4   NEUTRON POROSITY, original_mnemonic=NPHI, data.shape=(29897,)), 
CurveItem(mnemonic=SFLU, unit=OHMM, value=, descr=5  RXO RESISTIVITY, original_mnemonic=SFLU, data.shape=(29897,)), 
CurveItem(mnemonic=SFLA, unit=OHMM, value=, descr=6  SHALLOW RESISTIVITY, original_mnemonic=SFLA, data.shape=(29897,)), 
CurveItem(mnemonic=ILM, unit=OHMM, value=, descr=7  MEDIUM RESISTIVITY, original_mnemonic=ILM, data.shape=(29897,)), 
CurveItem(mnemonic=ILD, unit=OHMM, value=, descr=8  DEEP RESISTIVITY, original_mnemonic=ILD, data.shape=(29897,))]
```

Header information is parsed into simple HeaderItem objects, and stored in a dictionary for each section of the header:

```python
>>> las.version
[HeaderItem(mnemonic=VERS, unit=, value=1.2, descr=CWLS LOG ASCII STANDARD -VERSION 1.2, original_mnemonic=VERS), 
HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=ONE LINE PER DEPTH STEP, original_mnemonic=WRAP)]
>>> las.well
[HeaderItem(mnemonic=STRT, unit=M, value=1670.0, descr=, original_mnemonic=STRT), 
HeaderItem(mnemonic=STOP, unit=M, value=1660.0, descr=, original_mnemonic=STOP), 
HeaderItem(mnemonic=STEP, unit=M, value=-0.125, descr=, original_mnemonic=STEP), 
HeaderItem(mnemonic=NULL, unit=, value=-999.25, descr=, original_mnemonic=NULL), 
HeaderItem(mnemonic=COMP, unit=, value=ANY OIL COMPANY LTD., descr=COMPANY, original_mnemonic=COMP), 
HeaderItem(mnemonic=WELL, unit=, value=ANY ET AL OIL WELL #12, descr=WELL, original_mnemonic=WELL), 
HeaderItem(mnemonic=FLD, unit=, value=EDAM, descr=FIELD, original_mnemonic=FLD), 
HeaderItem(mnemonic=LOC, unit=, value=A9-16-49, descr=LOCATION, original_mnemonic=LOC), 
HeaderItem(mnemonic=PROV, unit=, value=SASKATCHEWAN, descr=PROVINCE, original_mnemonic=PROV), 
HeaderItem(mnemonic=SRVC, unit=, value=ANY LOGGING COMPANY LTD., descr=SERVICE COMPANY, original_mnemonic=SRVC), 
HeaderItem(mnemonic=DATE, unit=, value=25-DEC-1988, descr=LOG DATE, original_mnemonic=DATE), 
HeaderItem(mnemonic=UWI, unit=, value=100091604920, descr=UNIQUE WELL ID, original_mnemonic=UWI)]
>>> las.params
[HeaderItem(mnemonic=BHT, unit=DEGC, value=35.5, descr=BOTTOM HOLE TEMPERATURE, original_mnemonic=BHT), 
HeaderItem(mnemonic=BS, unit=MM, value=200.0, descr=BIT SIZE, original_mnemonic=BS), 
HeaderItem(mnemonic=FD, unit=K/M3, value=1000.0, descr=FLUID DENSITY, original_mnemonic=FD), 
HeaderItem(mnemonic=MATR, unit=, value=0.0, descr=NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO), original_mnemonic=MATR), 
HeaderItem(mnemonic=MDEN, unit=, value=2710.0, descr=LOGGING MATRIX DENSITY, original_mnemonic=MDEN), 
HeaderItem(mnemonic=RMF, unit=OHMM, value=0.216, descr=MUD FILTRATE RESISTIVITY, original_mnemonic=RMF), 
HeaderItem(mnemonic=DFD, unit=K/M3, value=1525.0, descr=DRILL FLUID DENSITY, original_mnemonic=DFD)]
```

The data is stored as a 2D numpy array:

```python
>>> las.data
array([[ 1670.   ,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ],
       [ 1669.875,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ],
       [ 1669.75 ,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ],
       ...,
       [ 1669.75 ,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ],
       [ 1670.   ,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ],
       [ 1669.875,   123.45 ,  2550.   , ...,   123.45 ,   110.2  ,   105.6  ]])
```

You can also retrieve and load data as a ``pandas`` DataFrame, build LAS files from scratch, 
write them back to disc, and export to Excel, amongst other things.

See the [documentation](https://lasio.readthedocs.io/en/latest/) for more details.

## License

MIT
