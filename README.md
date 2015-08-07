# lasio

[![Build Status](https://travis-ci.org/kinverarity1/lasio.svg)](https://travis-ci.org/kinverarity1/lasio) 
[![Coverage Status](https://coveralls.io/repos/kinverarity1/lasio/badge.svg?branch=master&service=github)](https://coveralls.io/github/kinverarity1/lasio?branch=master) 
[![PyPI Version](http://img.shields.io/pypi/v/lasio.svg?style=flat-square)](https://pypi.python.org/pypi/lasio/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/kinverarity1/lasio/blob/master/LICENSE)

Read/write well data from Log ASCII Standard (LAS) files.

This is a Python package to read and write Log ASCII Standard (LAS) files, used for borehole/well data (e.g. geophysical/geological/petrophysical logs). It is compatible with versions 1.2 and 2.0 of the LAS file specification, published by the [Canadian Well Logging Society][CWLS]. In principle it is designed to read as many types of LAS files as possible, including ones containing common errors or non-compliant formatting.

It is written entirely in Python and works on any platform. It requires:

  - Python >= 2.7
  - the small third-party package [``namedlist``][namedlist]
  - [``numpy``][numpy]. 

### Install

To install from [PyPI][PyPI] use:

```bash
$ pip install lasio
```

If necessary this will download and install the package dependencies.

Alternatively if you would like the latest version (which may contain bugs and errors) make sure you have [``setuptools``][setuptools] and ``git`` installed and then:

```bash
$ git clone https://github.com/kinverarity1/lasio.git
$ cd lasio
$ python setup.py develop 
```

### How to use

Look at the [example IPython notebooks here](http://nbviewer.ipython.org/github/kinverarity1/lasio/tree/master/notebooks/). More detailed examples are coming.

#### Opening LAS files

From a filename:

```python
>>> import lasio
>>> l = lasio.read("example.las")
```

Or a URL:

```python
>>> l = lasio.read("http://someplace.com/example.las")
```

#### Getting data

The curve data are available as items:

```python
>>> l["ILD"]
[145, 262, 272, ...]
```

Or you can iterate through the curves:

```python
>>> for c in l.curves:
...     print c.mnemonic, c.unit, c.data
DEPT m [0, 0.05, 0.10, ...] 
ILD mS/m [145, 262, 272, ...]
```

#### Character encodings

Three options:

1. Do nothing and [hope for no errors](https://docs.python.org/2.7/howto/unicode.html#encodings).

2. Specify the encoding (it uses [``codecs.open``](https://docs.python.org/2/library/codecs.html#codecs.open) internally):

   ```python
   >>> l = lasio.read("example.las", encoding="windows-1252")
   ```

3. Install a third-party package like [``cChardet``][cChardet] (faster) or [``chardet``][chardet] (slower) to automatically detect the character encoding. If these packages are installed this code will use the fastest option:
   
   ```python
   >>> l = lasio.read("example.las", autodetect_encoding=True)
   ```

  Note that by default ``autodetect_encoding=False``.

### Development

  - 0.6 (2015-08-05) - bugfixes and renamed from ``las_reader`` to ``lasio``
  - 0.5 (2015-08-01) - Improvements to writing LAS files
  - 0.4 (2015-07-26) - Improved handling of character encodings, other internal improvements
  - 0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
  - 0.2 (2015-07-08) - Tidied code and published on PyPI

#### Contributions

Contributions are very welcome. Please fork ``kinverarity1/lasio`` on GitHub and submit a PR request containing any changes you have made.

Suggested improvements, bug reports, shortcomings, desirable features, examples of LAS files which do not load as you expected, are all also welcome either [via GitHub](https://github.com/kinverarity1/lasio/issues/new) or by [email](kinverarity@hotmail.com).

Thanks to the following people in chronological order for their help:

  - @VelizarVESSELINOV
  - @diverdude

#### License

The code is freely available for any kind of use or modification under the MIT License.

[CWLS]: http://www.cwls.org/las/ "Canadian Well Logging Society"
[numpy]: http://www.numpy.org/  "NumPy website"
[namedlist]: https://pypi.python.org/pypi/namedlist "namedlist"
[setuptools]: https://pypi.python.org/pypi/setuptools "setuptools"
[chardet]:  https://pypi.python.org/pypi/chardet "chardet"
[cChardet]: https://github.com/PyYoshi/cChardet "cChardet"
[PyPI]: https://pypi.python.org/pypi/lasio "Python Package Index"

