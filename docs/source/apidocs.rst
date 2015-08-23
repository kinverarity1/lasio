API documentation
=================

``lasio`` - main interface
--------------------------

Although all the code lies in the two modules described in detail below, all the objects that you will need to use are available here:

.. code:: python
   
    >>> from lasio import __version__,                  # version string for lasio
    ...                   read,                         # use for reading existing LAS data
    ...                   LASFile, Curve, HeaderItem    # use for creating new LAS files from scratch

``lasio.las`` - main module
---------------------------

.. automodule:: lasio.las
   :members:

``lasio.las2excel`` - LAS -> Excel conversion
---------------------------------------------

.. automodule:: lasio.las2excel
   :members:
