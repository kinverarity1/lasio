
Installation
============

Compatibility and design
------------------------

``lasio`` is written to be compatible with Python 2.6+ (and runs without modification on Python 3).

It is structured as a standard Python package so that you can use it without having to modify your PYTHONPATH environment variable or update versions by copying files manually.

Installation from PyPI
----------------------

The recommended way to install it is from `PyPI <https://pypi.python.org/pypi/lasio>`__ with:

.. code:: bash

    $ pip install lasio

If necessary this will download and install the packages which ``lasio`` depends on to run:

- `namedlist <https://pypi.python.org/pypi/namedlist>`__ - simple and small
- `ordereddict <https://pypi.python.org/pypi/ordereddict>`__ - simple extension to the standard library for Python 2.6 support
- `numpy <http://numpy.org>`__ - for numerical computing, often pre-installed with scientific Python distributions

There are some packages which ``lasio`` will use to provide extra functionality if they are installed, but they are not required:

- `pandas <https://pypi.python.org/pypi/pandas>`__ - data analysis library
- `chardet <https://pypi.python.org/pypi/chardet>`__ or `cChardet <https://github.com/PyYoshi/cChardet>`__ - automatic detection of character encodings

Unless you have a particular reason I'd recommend installing these as well with:

.. code:: bash

    $ pip install -r optional-packages.txt

Updating your installation from PyPI
------------------------------------

New releases are frequently sent to `PyPI <https://pypi.python.org/pypi/lasio>`__, so if you want to stay updated:

.. code:: bash

   $ pip install --upgrade lasio

Installing from git
-------------------

If you would like the latest version from `GitHub <https://github.com/kinverarity1/lasio>`__ use:

.. code:: bash

    $ git clone https://github.com/kinverarity1/lasio.git
    $ cd lasio
    $ python setup.py develop

And to update:

.. code:: bash

    $ git pull origin master

License
-------

``lasio`` is open-sourced under the `MIT License <https://github.com/kinverarity1/lasio/blob/master/LICENSE>`__.

The code is available at `GitHub <https://github.com/kinverarity1/lasio>`__. 



Contributing
------------

Contributions are very welcome. Please fork the project on `GitHub <https://github.com/kinverarity1/lasio>`__ and submit a pull request (PR) containing any changes you have made.

Suggested improvements, bug reports, shortcomings, desirable features, examples of LAS files which do not load as you expected, are all also welcome either via `GitHub <https://github.com/kinverarity1/lasio/issues/new>`__ or `email <mailto:kinverarity@hotmail.com>`__.

Thanks to the following GitHub users (in chronological order) for their help:

-  VelizarVESSELINOV
-  diverdude
-  tomtommahout 
-  dagrha

Last updated 2015-12-02