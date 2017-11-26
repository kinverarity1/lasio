Installation
============

|Python versions| |PyPI version| |PyPI format|

``lasio`` is written to be compatible with Python 2.6+, and 3.2+. The best
way to install is using ``pip``.

.. code-block:: doscon

    (test) C:\Users\kent>pip install lasio

This will download and install lasio’s dependencies (`numpy`_ and
`ordereddict`_). 

There are some other packages which lasio will use to
provide extra functionality if they are installed (`pandas`_,
`cChardet`_ and/or `chardet`_, `openpyxl`_, and `argparse`_). I
recommend installing these too with:

.. code-block:: doscon

    (test) C:\Users\kent\Code\lasio>pip install -r optional-packages.txt

``lasio`` is now installed. See the following pages for examples of how to use the package.

To upgrade to the latest PyPI version, use:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>pip install --upgrade lasio

Development version
-------------------

Installing via pip gets the latest release which has been published on `PyPI <https://pypi.python.org/pypi/lasio/>`__.

The source code for lasio is kept at:

`https://github.com/kinverarity1/lasio <https://github.com/kinverarity1/lasio>`__

Updates are made much more frequently to the ``master`` branch here. If you have
Git installed, you can keep up to date with these changes:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing>git clone https://github.com/kinverarity1/lasio

    (test2) C:\Users\kent\Code\testing>cd lasio

    (test2) C:\Users\kent\Code\testing\lasio>pip install -r requirements.txt

    (test2) C:\Users\kent\Code\testing\lasio>python setup.py develop

To update your version with the latest changes on GitHub:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>git pull origin master

.. _numpy: http://numpy.org/
.. _ordereddict: https://pypi.python.org/pypi/ordereddict
.. _pandas: https://pypi.python.org/pypi/pandas
.. _cChardet: https://github.com/PyYoshi/cChardet
.. _chardet: https://github.com/chardet/chardet
.. _openpyxl: https://openpyxl.readthedocs.io/en/default/
.. _argparse: https://github.com/ThomasWaldmann/argparse/

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/lasio.svg
   :target: https://www.python.org/downloads/
.. |PyPI version| image:: http://img.shields.io/pypi/v/lasio.svg
   :target: https://pypi.python.org/pypi/lasio/
.. |PyPI format| image:: https://img.shields.io/pypi/format/lasio.svg
   :target: https://pypi.python.org/pypi/lasio

Testing
-------

Every time ``lasio`` is updated, automated tests are run:

* |Build Status Travis| `Travis CI`_: Linux, Python versions 2.7, 3.3, 3.4, 3.5, and 3.6. 
* |Build Status Appveyor| `Appveyor CI`_: Windows, Python versions 2.7, 3.4, 3.5, and 3.6.

``lasio`` should also work on Python 2.6 and 3.2, but these are tested only
occassionally.

To run tests yourself, first install the testing framework and all the
optional packages:

.. code:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>pip install pytest

    (test2) C:\Users\kent\Code\testing\lasio>pip install -r optional-packages.txt

And then run tests:

.. code:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>py.test

.. _Travis CI: https://travis-ci.org/kinverarity1/lasio
.. _Appveyor CI: https://ci.appveyor.com/project/kinverarity1/lasio

.. |Build Status Travis| image:: https://travis-ci.org/kinverarity1/lasio.svg?branch=master
   :target: https://travis-ci.org/kinverarity1/lasio

.. |Build Status Appveyor| image:: https://ci.appveyor.com/api/projects/status/csr7bg8urkbtbq4n
   :target: https://ci.appveyor.com/project/kinverarity1/lasio