# lasio

![](https://img.shields.io/badge/status-beta-yellow.svg)
[![](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kinverarity1/lasio/blob/master/LICENSE)
[![Research software impact](http://depsy.org/api/package/pypi/lasio/badge.svg)](http://depsy.org/package/python/lasio)

This is a Python 2/3 package to read and write Log ASCII Standard (LAS) files, used for borehole data such as geophysical, geological, or petrophysical logs. It's compatible with versions 1.2 and 2.0 of the LAS file specification, published by the [Canadian Well Logging Society](http://www.cwls.org/las). In principle it is designed to read as many types of LAS files as possible, including ones containing common errors or non-compliant formatting.

Depending on your particular application you may also want to check out  [striplog](https://github.com/agile-geoscience/striplog) for stratigraphic/lithological data, or (still in alpha dev) [welly](https://github.com/agile-geoscience/welly) for dealing with data at the well level. lasio is primarily for reading & writing LAS files.

## Installation

[![](https://img.shields.io/pypi/pyversions/lasio.svg)](https://www.python.org/downloads/)
[![](http://img.shields.io/pypi/v/lasio.svg)](https://pypi.python.org/pypi/lasio/)
[![](https://img.shields.io/pypi/dd/lasio.svg)](https://pypi.python.org/pypi/lasio/)
[![](https://img.shields.io/pypi/format/lasio.svg)](https://pypi.python.org/pypi/lasio/)

lasio is written to be compatible with Python 2.6+, and 3.2+. To install run:

```bash
$ pip install lasio
```

If necessary this will download and install the requirements ([numpy](http://numpy.org/) and a few other small ones).

There are some other packages which lasio will use to provide extra functionality if they are installed, but they are not required:

- [pandas](https://pypi.python.org/pypi/pandas) - data analysis library
- [chardet](https://pypi.python.org/pypi/chardet) or [cChardet](https://github.com/PyYoshi/cChardet) - automatic detection of character encodings

I'd recommend installing these too with:

```bash
$ pip install -r optional-packages.txt
```

New releases are frequently sent to [PyPI](https://pypi.python.org/pypi/lasio), so if you want to stay updated:

```bash
$ pip install --upgrade lasio
```

## Usage

Take a look through the [example Jupyter notebooks](http://nbviewer.ipython.org/github/kinverarity1/lasio/tree/master/notebooks) (or if that is down [try here](https://github.com/kinverarity1/lasio/tree/master/notebooks)) for detailed examples of how to use lasio

Thanks to [@oliveirarodolfo](https://github.com/oliveirarodolfo) you can also explore [lasio tutorial notebooks](https://github.com/oliveirarodolfo/lasio-notebooks) live in your browser at [binder](http://mybinder.org/repo/oliveirarodolfo/lasio-notebooks): [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/oliveirarodolfo/lasio-notebooks) 

Or as a quick example:

```python
>>> import lasio
>>> l = lasio.read("sample_big.las")
```

Data is accessible both directly as numpy arrays

```python
>>> l["SFLU"]
array([ 123.45,  123.45,  123.45, ...,  123.45,  123.45,  123.45])
>>> l["DEPT"]
array([ 1670.   ,  1669.875,  1669.75 , ...,  1669.75 ,  1670.   , 1669.875])
```

and as ``Curve`` objects with their associated metadata:

```python
>>> l.curves
[Curve(mnemonic=u'DEPT', unit=u'M', value=u'', descr=u'1  DEPTH', data=array([ 1670.   ,  1669.875,  1669.75 , ...,  1669.75 ,  1670.   , 1669.875])),
 Curve(mnemonic=u'DT', unit=u'US/M', value=u'', descr=u'2  SONIC TRANSIT TIME', data=array([ 123.45,  123.45,  123.45, ...,  123.45,  123.45,  123.45])),
 Curve(mnemonic=u'RHOB', unit=u'K/M3', value=u'', descr=u'3  BULK DENSITY', data=array([ 2550.,  2550.,  2550., ...,  2550.,  2550.,  2550.])),
 Curve(mnemonic=u'NPHI', unit=u'V/V', value=u'', descr=u'4   NEUTRON POROSITY', data=array([ 0.45,  0.45,  0.45, ...,  0.45,  0.45,  0.45])),
 Curve(mnemonic=u'SFLU', unit=u'OHMM', value=u'', descr=u'5  RXO RESISTIVITY', data=array([ 123.45,  123.45,  123.45, ...,  123.45,  123.45,  123.45])),
 Curve(mnemonic=u'SFLA', unit=u'OHMM', value=u'', descr=u'6  SHALLOW RESISTIVITY', data=array([ 123.45,  123.45,  123.45, ...,  123.45,  123.45,  123.45])),
 Curve(mnemonic=u'ILM', unit=u'OHMM', value=u'', descr=u'7  MEDIUM RESISTIVITY', data=array([ 110.2,  110.2,  110.2, ...,  110.2,  110.2,  110.2])),
 Curve(mnemonic=u'ILD', unit=u'OHMM', value=u'', descr=u'8  DEEP RESISTIVITY', data=array([ 105.6,  105.6,  105.6, ...,  105.6,  105.6,  105.6]))]
```

Header information is parsed into simple HeaderItem objects, and stored in a dictionary for each section of the header:

```python
>>> l.version
{'VERS': HeaderItem(mnemonic=u'VERS', unit=u'', value=1.2, descr=u'CWLS LOG ASCII STANDARD -VERSION 1.2'),
 'WRAP': HeaderItem(mnemonic=u'WRAP', unit=u'', value=u'NO', descr=u'ONE LINE PER DEPTH STEP')}
>>> l.well
{'STRT': HeaderItem(mnemonic=u'STRT', unit=u'M', value=1670.0, descr=u''),
 'STOP': HeaderItem(mnemonic=u'STOP', unit=u'M', value=1660.0, descr=u''),
 'STEP': HeaderItem(mnemonic=u'STEP', unit=u'M', value=-0.125, descr=u''),
 'NULL': HeaderItem(mnemonic=u'NULL', unit=u'', value=-999.25, descr=u''),
 'COMP': HeaderItem(mnemonic=u'COMP', unit=u'', value=u'ANY OIL COMPANY LTD.', descr=u'COMPANY'),
 'WELL': HeaderItem(mnemonic=u'WELL', unit=u'', value=u'ANY ET AL OIL WELL #12', descr=u'WELL'),
 'FLD': HeaderItem(mnemonic=u'FLD', unit=u'', value=u'EDAM', descr=u'FIELD'),
 'LOC': HeaderItem(mnemonic=u'LOC', unit=u'', value=u'A9-16-49-20W3M', descr=u'LOCATION'),
 'PROV': HeaderItem(mnemonic=u'PROV', unit=u'', value=u'SASKATCHEWAN', descr=u'PROVINCE'),
 'SRVC': HeaderItem(mnemonic=u'SRVC', unit=u'', value=u'ANY LOGGING COMPANY LTD.', descr=u'SERVICE COMPANY'),
 'DATE': HeaderItem(mnemonic=u'DATE', unit=u'', value=u'25-DEC-1988', descr=u'LOG DATE'),
 'UWI': HeaderItem(mnemonic=u'UWI', unit=u'', value=u'100091604920W300', descr=u'UNIQUE WELL ID')}
>>> l.params
{'BHT': HeaderItem(mnemonic=u'BHT', unit=u'DEGC', value=35.5, descr=u'BOTTOM HOLE TEMPERATURE'),
 'BS': HeaderItem(mnemonic=u'BS', unit=u'MM', value=200.0, descr=u'BIT SIZE'),
 'FD': HeaderItem(mnemonic=u'FD', unit=u'K/M3', value=1000.0, descr=u'FLUID DENSITY'),
 'MATR': HeaderItem(mnemonic=u'MATR', unit=u'', value=0.0, descr=u'NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)'),
 'MDEN': HeaderItem(mnemonic=u'MDEN', unit=u'', value=2710.0, descr=u'LOGGING MATRIX DENSITY'),
 'RMF': HeaderItem(mnemonic=u'RMF', unit=u'OHMM', value=0.216, descr=u'MUD FILTRATE RESISTIVITY'),
 'DFD': HeaderItem(mnemonic=u'DFD', unit=u'K/M3', value=1525.0, descr=u'DRILL FLUID DENSITY')}
```

You can also [build LAS files from scratch](https://github.com/kinverarity1/lasio/blob/master/notebooks/build%20LAS%20file%20from%20scratch.ipynb).

### Character encodings

Three options:

- Do nothing and hope for no errors.
- Specify the encoding (internally lasio uses the [open function from codecs](https://docs.python.org/2/library/codecs.html#codecs.open) which is part of the standard library):

```python
>>> l = lasio.read("example.las", encoding="windows-1252")
```

- Install a third-party package like [cChardet](https://github.com/PyYoshi/cChardet) (faster) or [chardet](https://pypi.python.org/pypi/chardet) (slower) to automatically detect the character encoding. If these packages are installed this code will use whichever is faster:

```python
>>> l = lasio.read("example.las", autodetect_encoding=True)
```

Note that by default ``autodetect_encoding=False``.

## Development

[![Build Status](https://travis-ci.org/kinverarity1/lasio.svg?branch=master)](https://travis-ci.org/kinverarity1/lasio)
[![](https://coveralls.io/repos/kinverarity1/lasio/badge.svg?branch=master&service=github)](https://coveralls.io/github/kinverarity1/lasio?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/252911a940b7476d9d7c4450d4045370)](https://www.codacy.com/app/kinverarity/lasio)
[![](https://scrutinizer-ci.com/g/kinverarity1/lasio/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/kinverarity1/lasio/#)
[![](https://www.quantifiedcode.com/api/v1/project/82d62106077f4c44a353c311984930d6/badge.svg)](https://www.quantifiedcode.com/app/project/82d62106077f4c44a353c311984930d6)

See the [list of changes](https://github.com/kinverarity1/lasio/blob/master/CHANGELOG.md) for each released version.

To use the latest development version:

```bash
$ git clone https://github.com/kinverarity1/lasio.git
$ cd lasio
$ python setup.py develop
```

And to update:

```bash
$ git pull origin master
```

lasio should work on Python 3.2, but it isn't tested regularly at [Travis CI](https://travis-ci.org/kinverarity1/lasio) because Miniconda is only Python 3.3+.

[![](http://githubbadges.herokuapp.com/kinverarity1/lasio/pulls.svg)](https://github.com/kinverarity1/lasio/pulls)
[![](http://githubbadges.herokuapp.com/kinverarity1/lasio/issues.svg)](https://github.com/kinverarity1/lasio/issues)

Contributions are very very welcome! Please fork the project on GitHub and submit a pull request (PR) containing any changes you have made. Or anything is welcome as a GitHub issue or an email to kinverarity@hotmail.com - suggestions, criticisms, questions, example files. 

Thanks to the following GitHub users for their help:

- VelizarVESSELINOV
- diverdude
- tomtommahout
- dagrha
- oliveirarodolfo
