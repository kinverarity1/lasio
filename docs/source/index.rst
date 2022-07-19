lasio - Log ASCII Standard (LAS) files in Python
====================================================

|License|

Read and write Log ASCII Standard files with Python.

This is a Python 3.6+ package to read and write Log ASCII Standard
(LAS) files, used for borehole data such as geophysical, geological, or
petrophysical logs. It's compatible with versions 1.2 and 2.0 of the LAS file
specification, published by the `Canadian Well Logging Society`_. 
Support for LAS 3 is `being worked on`_.

lasio is primarily for reading and writing data and metadata to and from 
LAS files. It is designed to read as many LAS files as possible, including
those containing common errors and non-compliant formatting. It can be used
directly, but you may want to consider using some other packages, depending
on your priorities:

- `welly`_ is a Python package that 
  uses lasio for I/O but provides a **lot** more functionality aimed at working
  with curves, wells, and projects. I would recommend starting there in most 
  cases, to avoid re-inventing the wheel!
- `lascheck`_ is focused on
  checking whether your LAS file meets the specifications.
- `lasr`_ is an R package which 
  is designed to read large amounts of data quickly from LAS files; this is 
  a great thing to check out if speed is a priority for you, as lasio is not 
  particularly fast.
- LiDAR surveys are also called "LAS files", but they are quite different and
  lasio will not help you -- check out `laspy`_ instead.

lasio stopped supporting Python 2.7 in August 2020. The final version of lasio 
with Python 2.7 support is version 0.26.

.. _Canadian Well Logging Society: https://www.cwls.org/products/#products-las
.. _welly: https://github.com/agilescientific/welly
.. _lasr: https://github.com/donald-keighley/lasr
.. _laspy: https://github.com/laspy/laspy
.. _lascheck: https://github.com/MandarJKulkarni/lascheck
.. _being worked on: https://github.com/kinverarity1/lasio/issues/5

.. |Status| image:: https://img.shields.io/badge/status-beta-yellow.svg
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/kinverarity1/lasio/blob/main/LICENSE
.. |Research software impact| image:: http://depsy.org/api/package/pypi/lasio/badge.svg
   :target: http://depsy.org/package/python/lasio


.. toctree::
   :maxdepth: 2
   :caption: User guide

   installation
   basic-example
   pandas
   header-section
   data-section
   writing
   exporting
   building
   encodings


.. toctree::
   :maxdepth: 2
   :caption: API reference

   lasio



.. toctree::
   :maxdepth: 2
   :caption: Other resources

   contributing
   changelog


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`


.. toctree::
   :caption: Project links
   :hidden:

    PyPI releases <https://pypi.org/project/lasio/>
    Code in GitHub <https://github.com/kinverarity1/lasio>
    Issue tracker <https://github.com/kinverarity1/lasio/issues>
