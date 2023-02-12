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

3. Install optional package `chardet`_ to automatically detect the character
   encoding. If `chardet`_ is installed then lasio will use it by default:

.. code-block:: python

    >>> import logging
    >>> logging.basicConfig()
    >>> logging.getLogger().setLevel(logging.DEBUG)
    >>> las = lasio.read('encodings_utf8.las')
    DEBUG:lasio.reader:get_encoding Using chardet
    DEBUG:lasio.reader:chardet method detected encoding of utf-8 at confidence 0.99
    INFO:lasio.reader:Opening encodings_utf8.las as utf-8 and treating errors with "replace"
    ...

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
.. _chardet: https://pypi.org/project/chardet
