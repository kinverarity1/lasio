# LAS Reader

``las_reader`` is a Python package to read in Log ASCII Standard (LAS) files, used for borehole data (e.g. geophysical/geological/petrophysical logs). The LAS file format is specified by the [Canadian Well Logging Society](http://www.cwls.org/las/). This is intended to be a lightweight package for getting the data out for use with ``numpy`` and other scientific Python tools. It also has the ability to write LAS files.

In principle it should read as many of the existing LAS files as possible, including common types of non-compliant files. 

## Installation

``las_reader`` works on any platform. It depends on the small third-party package ``namedlist`` as well as ``numpy`` and ``setuptools``. To install use:

    $ pip install las_reader

This will download and install the dependencies if necessary as well.

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

There is an [example usage IPython notebook](http://nbviewer.ipython.org/github/kinverarity1/las-reader/blob/master/docs/Example%20usage.ipynb) demonstrating how to use the package.

### Character encodings

Three options:

1. Do nothing and [hope for no errors](https://docs.python.org/2.7/howto/unicode.html#encodings).

2. Specify the encoding (it uses [``codecs.open``](https://docs.python.org/2/library/codecs.html#standard-encodings) internally):

   ```python
   >>> l = las_reader.read("example.las", encoding="windows-1252")
   ```

3. Install a third-party package (``chardet`` (slow) or ``cchardet`` (fast)) to automatically detect the character encoding. If these packages are installed this code will use the fastest option:
   
   ```python
   >>> l = las_reader.read("example.las", autodetect_encoding=True)
   ```

## Development

### Version history

  - 0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
  - 0.2 (2015-07-08) - Tidied code and published on PyPi

### Contributions

Contributions, enhancements, comments, or bug reports are welcome -- please submit via GitHub or by [email](kinverarity@hotmail.com).

Please let me know if you have any examples of LAS files which this package does not read properly or as expected.

### License

The code is freely available for any kind of use or modification under the MIT License.
