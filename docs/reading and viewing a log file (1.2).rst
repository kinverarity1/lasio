
reading and viewing a log file (1.2)
====================================

Read in an example LAS 1.2 file:

.. code:: python

    import las_reader           
    log = las_reader.read('https://raw.github.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las')
    type(log)

.. parsed-literal::

    VERS.                  1.2:   CWLS LOG ASCII STANDARD -VERSION 1.2
    ['VERS', None, '1.2', 'CWLS LOG ASCII STANDARD -VERSION 1.2']
    WRAP.                  NO:   ONE LINE PER DEPTH STEP
    ['WRAP', None, 'NO', 'ONE LINE PER DEPTH STEP']
    STRT.M        1670.000000:
    ['STRT', 'M', '1670.000000', '']
    STOP.M        1660.000000:
    ['STOP', 'M', '1660.000000', '']
    STEP.M            -0.1250:
    ['STEP', 'M', '-0.1250', '']
    NULL.           -999.2500:
    ['NULL', None, '-999.2500', '']
    COMP.             COMPANY:   ANY OIL COMPANY LTD.
    ['COMP', None, 'COMPANY', 'ANY OIL COMPANY LTD.']
    WELL.                WELL:   ANY ET AL OIL WELL #12
    ['WELL', None, 'WELL', 'ANY ET AL OIL WELL #12']
    FLD .               FIELD:   EDAM
    ['FLD', None, 'FIELD', 'EDAM']
    LOC .            LOCATION:   A9-16-49-20W3M
    ['LOC', None, 'LOCATION', 'A9-16-49-20W3M']
    PROV.            PROVINCE:   SASKATCHEWAN
    ['PROV', None, 'PROVINCE', 'SASKATCHEWAN']
    SRVC.     SERVICE COMPANY:   ANY LOGGING COMPANY LTD.
    ['SRVC', None, 'SERVICE COMPANY', 'ANY LOGGING COMPANY LTD.']
    DATE.            LOG DATE:   25-DEC-1988
    ['DATE', None, 'LOG DATE', '25-DEC-1988']
    UWI .      UNIQUE WELL ID:   100091604920W300
    ['UWI', None, 'UNIQUE WELL ID', '100091604920W300']
    



.. parsed-literal::

    las_reader.LASFile



The LASFile object has some provenance information depending on what was
read. You can pass the read() function a filename, URL, file-like
object, or string.

.. code:: python

    log.provenance



.. parsed-literal::

    {'name': 'sample_curve_api.las',
     'path': None,
     'time_opened': datetime.datetime(2013, 12, 24, 21, 45, 53, 708000),
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

    