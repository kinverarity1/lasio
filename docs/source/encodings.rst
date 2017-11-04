Character encodings
===================

There are four options:

1. Specify the encoding (internally lasio uses the `open function from
codecs`_ which is part of the standard library):

.. code-block:: python

    >>> las = lasio.read('example.las', encoding='windows-1252')

2. Do nothing. By default :func:`lasio.read` uses the keyword argument
``autodetect_encoding=True``. This will try to open the file with a few
different encodings, like 'ascii', 'windows-1252', and 'latin-1'. The
first one to raise no ``UnicodeDecodeError`` exceptions will be used.

This may still result in an error, or incorrectly decoded characters.

3. Install a package like `cChardet`_ (faster) or `chardet`_
(slower) to automatically detect the character encoding. If these
packages are installed then lasio will use them by default:

.. code-block:: python

    >>> import logging
    >>> logging.basicConfig()
    >>> logging.getLogger().setLevel(logging.DEBUG)
    >>> las = lasio.read('encodings_utf8.las')
    DEBUG:lasio.reader:get_encoding Using cchardet
    DEBUG:lasio.reader:cchardet method detected encoding of UTF-8 at confidence 0.9900000095367432
    INFO:lasio.reader:Opening encodings_utf8.las as UTF-8 and treating errors with "replace"
    DEBUG:lasio.las:n_curves=8 ncols=8
    DEBUG:lasio.las:set_data data.shape = (3, 8)
    DEBUG:lasio.las:set_data self.data.shape = (3, 8)

This may still result in an error, or incorrectly decoded characters.

If you are certain that you have no `"extended characters" <https://en.wikipedia.org/wiki/Extended_ASCII>`__
(or that you don't care), you can easily speed up lasio's performance by 
using:

.. code-block:: python

    >>> try:
    ...     las = lasio.read('example.las', autodetect_encoding=False)
    ... except UnicodeDecodeError:
    ...     continue

.. _open function from codecs: https://docs.python.org/2/library/codecs.html#codecs.open
.. _cChardet: https://github.com/PyYoshi/cChardet
.. _chardet: https://pypi.python.org/pypi/chardet