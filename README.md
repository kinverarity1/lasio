# LAS Reader

``las_reader`` is a Python package to read in Log ASCII Standard (LAS) files, used for borehole data (e.g. geophysical/geological/petrophysical logs). It is intended to be a lightweight package for getting the data out for use with [``numpy``][numpy] and other scientific Python tools, and also has the ability to write LAS files.

It is compatible with versions 1.2 and 2.0 of the LAS file specification, published by the [Canadian Well Logging Society][CWLS].

In principle it is designed to read as many types of LAS files as possible, including ones containing common errors or non-compliant formatting. 

## Installation

``las_reader`` works on any platform. It depends on the small third-party package [``namedlist``][namedlist] as well as [``numpy``][numpy] and [``setuptools``][setuptools]. To install use:

```bash
$ pip install las_reader
```

If necessary this will download and install the package dependencies.

## Usage

```python
>>> import las_reader
>>> l = las_reader.read("example.las")
```

The curve data are available as items:

```python
>>> l["ILD"]
[145, 262, 272, ...]
```

There are some [example IPython notebooks here](https://github.com/kinverarity1/las-reader/tree/master/docs) demonstrating how to use the package. More are in the works.

### Character encodings

Three options:

1. Do nothing and [hope for no errors](https://docs.python.org/2.7/howto/unicode.html#encodings).

2. Specify the encoding (it uses [``codecs.open``](https://docs.python.org/2/library/codecs.html#codecs.open) internally):

   ```python
   >>> l = las_reader.read("example.las", encoding="windows-1252")
   ```

3. Install a third-party package like [``cChardet``][cChardet] (faster) or [``chardet``][chardet] (slower) to automatically detect the character encoding. If these packages are installed this code will use the fastest option:
   
   ```python
   >>> l = las_reader.read("example.las", autodetect_encoding=True)
   ```

  Note that by default ``autodetect_encoding`` = ``False``.

## Development

### Version history

  - 0.5 (2015-08-01) - Improvements to writing LAS files
  - 0.4 (2015-07-26) - Improved handling of character encodings, other internal improvements
  - 0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
  - 0.2 (2015-07-08) - Tidied code and published on PyPi

### Contributions

Contributions, enhancements, comments, bug reports, or examples of LAS files which do not work as expected are all welcome -- please submit [via GitHub](https://github.com/kinverarity1/las-reader/issues/new) or by [email](kinverarity@hotmail.com).

### License

The code is freely available for any kind of use or modification under the MIT License.

[CWLS]: http://www.cwls.org/las/ "Canadian Well Logging Society"
[numpy]: http://www.numpy.org/  "NumPy website"
[namedlist]: https://pypi.python.org/pypi/namedlist "namedlist"
[setuptools]: https://pypi.python.org/pypi/setuptools "setuptools"
[chardet]:  https://pypi.python.org/pypi/chardet "chardet"
[cChardet]: https://github.com/PyYoshi/cChardet "cChardet"
