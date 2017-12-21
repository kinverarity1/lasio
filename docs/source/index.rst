``lasio`` - Log ASCII Standard (LAS) files in Python
====================================================

|Status| |License| |Research software impact|

This is a Python 2/3 package to read and write Log ASCII Standard (LAS)
files, used for borehole data such as geophysical, geological, or
petrophysical logs. It’s compatible with versions 1.2 and 2.0 of the LAS
file specification, published by the `Canadian Well Logging Society`_.
In principle it is designed to read as many types of LAS files as
possible, including ones containing common errors or non-compliant
formatting.

Depending on your particular application you may also want to check out
`striplog`_ for stratigraphic/lithological data, or (still in alpha dev)
`welly`_ for dealing with data at the well level. lasio is primarily for
reading & writing LAS files.

Note this is *not* a package for reading LiDAR data (also called “LAS
files”).

.. _Canadian Well Logging Society: http://www.cwls.org/las
.. _striplog: https://github.com/agile-geoscience/striplog
.. _welly: https://github.com/agile-geoscience/welly

.. |Status| image:: https://img.shields.io/badge/status-beta-yellow.svg
.. |License| image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/kinverarity1/lasio/blob/master/LICENSE
.. |Research software impact| image:: http://depsy.org/api/package/pypi/lasio/badge.svg
   :target: http://depsy.org/package/python/lasio

.. toctree::
   :maxdepth: 5

   installation
   basic-example
   pandas
   header-section
   data-section
   writing
   exporting
   building
   encodings
   contributing
   lasio

* :ref:`genindex`
* :ref:`search`
