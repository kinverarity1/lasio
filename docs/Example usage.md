
# LAS Reader

``las_reader`` is a Python package to read in Log ASCII Standard (LAS) files,
used in geophysical logging.
The file format is specified by the Canadian Well Logging Society. The package
only works for versions 1.2 and 2.0 so far.

The ``las_reader.read()`` function accepts a filename, file-like object, or URL
as an argument and returns a ``Las`` object:


    import las_reader
    l = las_reader.read('https://raw.githubusercontent.com/kinverarity1/las-reader'
                        '/master/standards/examples/1.2/sample_curve_api.las')
    type(l)




    las_reader.las.Las



Curves are available as ``numpy.ndarray`` objects as items in the ``Las`` object
itself:


    l.keys()




    ['DEPTH', 'RHOB', 'NPHI', 'MSFL', 'SFLA', 'ILM', 'ILD', 'SP']




    l['RHOB']




    array([    nan,  123.45,  123.45])



You can also access curves by their index:


    print id(l['NPHI'])
    print id(l[3])

    67844832
    67844880
    


    print id(l['ILM'])
    print id(l[-2])

    67844976
    67845024
    

All the curves are stored as a two-dimensional ``ndarray`` under the ``data``
attribute:


    l.data.shape




    (3, 8)



Metadata from the LAS file's header is stored in a special kind of dictionary,
one for each section (``version``, ``well``, ``curves``, and ``params``). Each
line of a metadata has a particular type depending on its section (``Metadata``,
``Curve``, or ``Parameter``). The latter types are named tuples created using
``collections.namedtuple``. The value of any bit of metadata can always be
accessed with the ``value`` attribute:


    l.version




    {'VERS': Metadata(unit=None, value=1.2, descr='CWLS LOG ASCII STANDARD -VERSION 1.2'),
     'WRAP': Metadata(unit=None, value='NO', descr='ONE LINE PER DEPTH STEP')}




    l.version['VERS'].value




    1.2




    l.well




    {'STRT': Metadata(unit='M', value=1670.0, descr=''),
     'STOP': Metadata(unit='M', value=1660.0, descr=''),
     'STEP': Metadata(unit='M', value=-0.125, descr=''),
     'NULL': Metadata(unit=None, value=-999.25, descr=''),
     'COMP': Metadata(unit=None, value='ANY OIL COMPANY LTD.', descr='COMPANY'),
     'WELL': Metadata(unit=None, value='ANY ET AL OIL WELL #12', descr='WELL'),
     'FLD': Metadata(unit=None, value='EDAM', descr='FIELD'),
     'LOC': Metadata(unit=None, value='A9-16-49-20W3M', descr='LOCATION'),
     'PROV': Metadata(unit=None, value='SASKATCHEWAN', descr='PROVINCE'),
     'SRVC': Metadata(unit=None, value='ANY LOGGING COMPANY LTD.', descr='SERVICE COMPANY'),
     'DATE': Metadata(unit=None, value='25-DEC-1988', descr='LOG DATE'),
     'UWI': Metadata(unit=None, value='100091604920W300', descr='UNIQUE WELL ID')}



A simpler way of viewing this is to use the special ``_d`` attribute of each
section's dictionary:


    l.well._d




    {'COMP': 'ANY OIL COMPANY LTD.',
     'DATE': '25-DEC-1988',
     'FLD': 'EDAM',
     'LOC': 'A9-16-49-20W3M',
     'NULL': -999.25,
     'PROV': 'SASKATCHEWAN',
     'SRVC': 'ANY LOGGING COMPANY LTD.',
     'STEP': -0.125,
     'STOP': 1660.0,
     'STRT': 1670.0,
     'UWI': '100091604920W300',
     'WELL': 'ANY ET AL OIL WELL #12'}




    l.curves




    {'DEPTH': Curve(unit='M', API_code='', descr='1       DEPTH'),
     'RHOB': Curve(unit='K/M3', API_code='7 350 02 00', descr='2       BULK DENSITY'),
     'NPHI': Curve(unit='VOL/VOL', API_code='7 890 00 00', descr='3       NEUTRON POROSITY - SANDSTONE'),
     'MSFL': Curve(unit='OHMM', API_code='7 220 01 00', descr='4       Rxo RESISTIVITY'),
     'SFLA': Curve(unit='OHMM', API_code='7 222 01 00', descr='5       SHALLOW RESISTIVITY'),
     'ILM': Curve(unit='OHMM', API_code='7 120 44 00', descr='6       MEDIUM RESISTIVITY'),
     'ILD': Curve(unit='OHMM', API_code='7 120 46 00', descr='7       DEEP RESISTIVITY'),
     'SP': Curve(unit='MV', API_code='7 010 01 00', descr='8       SPONTANEOUS POTENTIAL')}




    l.params




    {'BHT': Parameter(unit='DEGC', value=35.5, descr='BOTTOM HOLE TEMPERATURE'),
     'BS': Parameter(unit='MM', value=200.0, descr='BIT SIZE'),
     'FD': Parameter(unit='K/M3', value=1000.0, descr='FLUID DENSITY'),
     'MATR': Parameter(unit=None, value=0.0, descr='NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)'),
     'MDEN': Parameter(unit=None, value=2710.0, descr='LOGGING MATRIX DENSITY'),
     'RMF': Parameter(unit='OHMM', value=0.216, descr='MUD FILTRATE RESISTIVITY'),
     'DFD': Parameter(unit='K/M3', value=1525.0, descr='DRILL FLUID DENSITY')}



For convenience there's a special attribute which is an ordinary dictionary that
brings together all the metadata in the file:


    l.metadata




    {'BHT': 35.5,
     'BS': 200.0,
     'COMP': 'ANY OIL COMPANY LTD.',
     'DATE': '25-DEC-1988',
     'DFD': 1525.0,
     'FD': 1000.0,
     'FLD': 'EDAM',
     'LOC': 'A9-16-49-20W3M',
     'MATR': 0.0,
     'MDEN': 2710.0,
     'NULL': -999.25,
     'PROV': 'SASKATCHEWAN',
     'RMF': 0.216,
     'SRVC': 'ANY LOGGING COMPANY LTD.',
     'STEP': -0.125,
     'STOP': 1660.0,
     'STRT': 1670.0,
     'UWI': '100091604920W300',
     'VERS': 1.2,
     'WELL': 'ANY ET AL OIL WELL #12',
     'WRAP': 'NO'}



As per the standard, the ~Other section is free text. I know many companies put
LAS-formatted metadata in here; I'll figure out a way to incorporate this soon:


    print l.other

    Note: The logging tools became stuck at 625 meters causing the data
    between 625 meters and 615 meters to be invalid.
    

Finally there is some useful information in the ``provenance`` attribute that
depends on how you opened the file in the first place:


    l.provenance




    {'name': 'sample_curve_api.las',
     'path': None,
     'time_opened': datetime.datetime(2014, 4, 6, 12, 34, 42, 851000),
     'url': 'https://raw.githubusercontent.com/kinverarity1/las-reader/master/standards/examples/1.2/sample_curve_api.las'}




    
