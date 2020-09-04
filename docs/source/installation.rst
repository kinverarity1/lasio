Installation
============

lasio is written to be compatible with Python 3.2+. The best
way to install is using pip.

.. code-block:: bash

    $ pip install lasio

This will make sure that the dependency `numpy`_ is installed as well.

The final version of lasio with Python 2.7 support is v0.26.

There are some other packages which lasio will use to
provide extra functionality if they are installed (`pandas`_,
`cChardet`_ and/or `chardet`_, and `openpyxl`_). I
recommend installing these with:

.. code-block::

    $ pip install lasio[all]

lasio is now installed.

To upgrade to the latest PyPI version, use:

.. code-block::

    $ pip install --upgrade lasio

Development version
-------------------

Installing via pip gets the latest release which has been published on `PyPI <https://pypi.python.org/pypi/lasio/>`__. If you want, you can install the latest changes from `GitHub`_:

.. code-block::

    $ pip install https://github.com/kinverarity1/lasio/archive/master.zip

.. _numpy: http://numpy.org/
.. _pandas: https://pypi.python.org/pypi/pandas
.. _cChardet: https://github.com/PyYoshi/cChardet
.. _chardet: https://github.com/chardet/chardet
.. _openpyxl: https://openpyxl.readthedocs.io/en/default/
.. _GitHub: https://github.com/kinverarity1/lasio

Testing
-------

|Build Status Travis|

Every time lasio is updated, automated tests are run using `Travis CI`_ on
Python 3.5, 3.6, 3.7, and 3.8, on Linux. lasio should also work on Python
3.3, and 3.4 but these are not regularly tested.

To run tests yourself:

.. code-block::

    $ pip install pytest>=3.6 pytest-cov coverage
    $ pytest

.. _Travis CI: https://travis-ci.org/kinverarity1/lasio

.. |Build Status Travis| image:: https://travis-ci.org/kinverarity1/lasio.svg?branch=master
   :target: https://travis-ci.org/kinverarity1/lasio
