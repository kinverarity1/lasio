lasio
=====

|PyPI Version| |PyPI Downloads| |Build Status| |Coverage Status| |GitHub
Issues| |GitHub PRs| |Python Version| |PyPI Format| |MIT License|

Read/write well data from Log ASCII Standard (LAS) files.

This is a Python package to read and write Log ASCII Standard (LAS)
files, used for borehole/well data (e.g.
geophysical/geological/petrophysical logs). It is compatible with
versions 1.2 and 2.0 of the LAS file specification, published by the
`Canadian Well Logging Society <http://www.cwls.org/las/>`__. In
principle it is designed to read as many types of LAS files as possible,
including ones containing common errors or non-compliant formatting.

It is written entirely in Python and works on any platform. It requires:

-  the small third-party packages
   ```namedlist`` <https://pypi.python.org/pypi/namedlist>`__ and
   ```ordereddict`` <https://pypi.python.org/pypi/ordereddict>`__
-  ```numpy`` <http://www.numpy.org/>`__.

Install
-------

To install from `PyPI <https://pypi.python.org/pypi/lasio>`__ use:

.. code:: bash

    $ pip install lasio

If necessary this will download and install the package dependencies.

Alternatively if you would like the latest version (which may contain
bugs and errors) make sure you have
```setuptools`` <https://pypi.python.org/pypi/setuptools>`__ and ``git``
installed and then:

.. code:: bash

    $ git clone https://github.com/kinverarity1/lasio.git
    $ cd lasio
    $ python setup.py develop 

How to use
----------

Look at the `example IPython notebooks
here <http://nbviewer.ipython.org/github/kinverarity1/lasio/tree/master/notebooks/>`__.
More detailed examples are coming.

Opening LAS files
~~~~~~~~~~~~~~~~~

From a filename:

.. code:: python

    >>> import lasio
    >>> l = lasio.read("example.las")

Or a URL:

.. code:: python

    >>> l = lasio.read("http://someplace.com/example.las")

Getting data
~~~~~~~~~~~~

The curve data are available as items:

.. code:: python

    >>> l["ILD"]
    [145, 262, 272, ...]

Or you can iterate through the curves:

.. code:: python

    >>> for c in l.curves:
    ...     print c.mnemonic, c.unit, c.data
    DEPT m [0, 0.05, 0.10, ...] 
    ILD mS/m [145, 262, 272, ...]

Character encodings
~~~~~~~~~~~~~~~~~~~

Three options:

1. Do nothing and `hope for no
   errors <https://docs.python.org/2.7/howto/unicode.html#encodings>`__.

2. Specify the encoding (it uses
   ```codecs.open`` <https://docs.python.org/2/library/codecs.html#codecs.open>`__
   internally):

``python    >>> l = lasio.read("example.las", encoding="windows-1252")``

3. Install a third-party package like
   ```cChardet`` <https://github.com/PyYoshi/cChardet>`__ (faster) or
   ```chardet`` <https://pypi.python.org/pypi/chardet>`__ (slower) to
   automatically detect the character encoding. If these packages are
   installed this code will use the fastest option:

``python    >>> l = lasio.read("example.las", autodetect_encoding=True)``

Note that by default ``autodetect_encoding=False``.

Development
-----------

-  0.7 (2015-08-08) - all tests passing on Python 2.6 through 3.4
-  0.6 (2015-08-05) - bugfixes and renamed from ``las_reader`` to
   ``lasio``
-  0.5 (2015-08-01) - Improvements to writing LAS files
-  0.4 (2015-07-26) - Improved handling of character encodings, other
   internal improvements
-  0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
-  0.2 (2015-07-08) - Tidied code and published on PyPI

Contributions
~~~~~~~~~~~~~

Contributions are very welcome. Please fork ``kinverarity1/lasio`` on
GitHub and submit a PR request containing any changes you have made.

Suggested improvements, bug reports, shortcomings, desirable features,
examples of LAS files which do not load as you expected, are all also
welcome either `via
GitHub <https://github.com/kinverarity1/lasio/issues/new>`__ or by
`email <kinverarity@hotmail.com>`__.

Thanks to the following people in chronological order for their help:

-  @VelizarVESSELINOV
-  @diverdude

License
~~~~~~~

The code is freely available for any kind of use or modification under
the MIT License.

.. |PyPI Version| image:: http://img.shields.io/pypi/v/lasio.svg
   :target: https://pypi.python.org/pypi/lasio/
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dd/lasio.svg
   :target: https://pypi.python.org/pypi/lasio/
.. |Build Status| image:: https://travis-ci.org/kinverarity1/lasio.svg
   :target: https://travis-ci.org/kinverarity1/lasio
.. |Coverage Status| image:: https://coveralls.io/repos/kinverarity1/lasio/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/kinverarity1/lasio?branch=master
.. |GitHub Issues| image:: http://githubbadges.herokuapp.com/kinverarity1/lasio/issues.svg
   :target: https://github.com/kinverarity1/lasio/issues
.. |GitHub PRs| image:: http://githubbadges.herokuapp.com/kinverarity1/lasio/pulls.svg
   :target: https://github.com/kinverarity1/lasio/pulls
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/lasio.svg
   :target: https://www.python.org/downloads/
.. |PyPI Format| image:: https://img.shields.io/pypi/format/lasio.svg
   :target: https://pypi.python.org/pypi/lasio/
.. |MIT License| image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/kinverarity1/lasio/blob/master/LICENSE
