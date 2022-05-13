lasio - Log ASCII Standard (LAS) files in Python
====================================================

|License|

lasio is a Python 3 package to read and write Log ASCII Standard (LAS)
files, used for borehole data such as geophysical, geological, or
petrophysical logs. It’s compatible with versions 1.2 and 2.0 of the LAS
file specification, published by the `Canadian Well Logging Society`_.
In principle it is designed to read as many types of LAS files as
possible, including ones containing common errors or non-compliant
formatting. 

Depending on your particular application you may also want to check out
`striplog`_ for stratigraphic/lithological data, or 
`welly`_ for dealing with data at the well level. lasio is primarily for
reading & writing LAS files. lasio is also not particularly fast at reading 
LAS data, being instead focused on convience and reliability; if you are 
interested in reading LAS data rapidly (and have a clean or simple set of data),
you may want to shift gears to R and have a look at `lasr`_.

Note this is *not* a package for reading LiDAR data, which is also stored
in "LAS" files.

The final version of lasio with Python 2.7 support is v0.26.

.. _Canadian Well Logging Society: http://www.cwls.org/las
.. _striplog: https://github.com/agile-geoscience/striplog
.. _welly: https://github.com/agile-geoscience/welly
.. _lasr: https://github.com/donald-keighley/lasr

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
   lasio
   contributing
   changelog

* :ref:`genindex`
* :ref:`search`
