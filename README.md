LAS Reader
==========

``las_reader`` is a Python package to read in Log ASCII Standard (LAS) files, used in borehole geophysical logging. The LAS file format is specified by the [Canadian Well Logging Society](http://www.cwls.org/las/). This is intended to be a lightweight package for getting the data out for use with ``numpy`` and other scientific Python tools. It also has the ability to write LAS files.

In principle it should read as many of the existing LAS files as possible, including common types of non-compliant files. Please submit an issue on GitHub or [email](kinverarity1+github@gmail.com) me if you have any examples of LAS files which this package does not read properly or as expected.

Quick start
-----------

Install using:

    $ pip install las_reader

The only requirements are ``namedlist``, ``numpy``, and ``setuptools``, which can all be installed via pip as well. There is an [example usage IPython notebook](http://nbviewer.ipython.org/github/kinverarity1/las-reader/blob/master/docs/Example%20usage.ipynb) demonstrating how to use the package.

Version history
---------------

  - 0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
  - 0.2 (2015-07-08) - Tidied code and published on PyPi

Development
-----------

Contributions, enhancements, comments, or bug reports are welcome -- please submit via GitHub or by [email](kinverarity1+github@gmail.com).

The code is freely available for any kind of use or modification under the MIT License.
