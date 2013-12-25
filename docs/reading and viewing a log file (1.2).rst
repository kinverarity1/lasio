
reading and viewing a log file (1.2)
====================================

.. code:: python

    import las_reader
Read in an example LAS 1.2 file:

.. code:: python

    log = las_reader.read('https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las')
    print type(log)

.. parsed-literal::

    <class 'las_reader.LASFile'>
    

The LASFile object has some provenance information depending on what was
read. You can pass the read() function a filename, URL, file-like
object, or string.

.. code:: python

    log.provenance



.. parsed-literal::

    {'name': 'sample_curve_api.las',
     'path': None,
     'time_opened': datetime.datetime(2013, 12, 25, 13, 22, 35, 89000),
     'url': 'https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las'}



The version and well sections are present as dictionaries:

.. code:: python

    log.version



.. parsed-literal::

    {'DLM': ' ', 'VERS': 1.2, 'WRAP': False}



.. code:: python

    log.well



.. parsed-literal::

    {'COMP': 'ANY OIL COMPANY LTD.',
     'CTRY': None,
     'DATE': '25-DEC-1988',
     'FLD': 'EDAM',
     'LOC': 'A9-16-49-20W3M',
     'NULL': -999.25,
     'PROV': 'SASKATCHEWAN',
     'SRVC': 'ANY LOGGING COMPANY LTD.',
     'STEP': -0.125,
     'STEP.UNIT': 'M',
     'STOP': 1660.0,
     'STOP.UNIT': 'M',
     'STRT': 1670.0,
     'STRT.UNIT': 'M',
     'UWI': '100091604920W300',
     'WELL': 'ANY ET AL OIL WELL #12'}



.. code:: python

    
.. code:: python

    