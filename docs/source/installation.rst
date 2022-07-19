Installation
============

lasio is written to be compatible with Python 3.6+. The best
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

    $ pip install "lasio[all]"

lasio is now installed.

To upgrade to the latest PyPI version, use:

.. code-block::

    $ pip install --upgrade lasio

Development version
-------------------

Installing via pip gets the latest release which has been published on
`PyPI <https://pypi.org/project/lasio/>`__. If you want, you can install 
the latest changes from `GitHub`_:

.. code-block::

    $ pip install https://github.com/kinverarity1/lasio/archive/master.zip

.. _numpy: https://numpy.org/
.. _pandas: https://pypi.org/project/pandas/
.. _cChardet: https://github.com/PyYoshi/cChardet
.. _chardet: https://github.com/chardet/chardet
.. _openpyxl: https://openpyxl.readthedocs.io/en/stable/
.. _GitHub: https://github.com/kinverarity1/lasio


