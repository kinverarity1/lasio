``lasio`` - Log ASCII Standard (LAS) files in Python
====================================================

|PyPI Version| |PyPI Downloads| |Build Status| |Coverage Status| |Python Version| |PyPI Format| |MIT License|

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

``lasio`` is a Python package to read and write Log ASCII Standard (LAS) files, used for borehole/well data (e.g. geophysical/geological/petrophysical logs). It is compatible with versions 1.2 and 2.0 of the LAS file specification, published by the `Canadian Well Logging Society <http://www.cwls.org/las>`__. In principle it is designed to read as many types of LAS files as possible, including ones containing common errors or non-compliant formatting.

.. toctree::
   :maxdepth: 2

   install
   usage
   apidocs

* :ref:`genindex`
* :ref:`search`

What's new
----------

-  0.9.1 (2015-11-11) - pandas.DataFrame now as .df attribute, bugfix
-  0.8 (2015-08-20) - numerous bug fixes, API documentation added
-  0.7 (2015-08-08) - all tests passing on Python 2.6 through 3.4
-  0.6 (2015-08-05) - bugfixes and renamed from ``las_reader`` to ``lasio``
-  0.5 (2015-08-01) - Improvements to writing LAS files
-  0.4 (2015-07-26) - Improved handling of character encodings, other internal improvements
-  0.3 (2015-07-23) - Added Python 3 support, now reads LAS 1.2 and 2.0
-  0.2 (2015-07-08) - Tidied code and published on PyPI