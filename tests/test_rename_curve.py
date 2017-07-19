import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

from lasio import read
from lasio.excel import ExcelConverter

from lasio.reader import StringIO

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)


def test_rename_and_write_curve_mnemonic():
    l = read(egfn("sample.las"))
    for curve in l.curves:
        if curve.mnemonic != 'DEPT':
            curve.mnemonic = "New_" + curve.mnemonic
    for curve in l.curves:
        print('mnemonic=%s original_mnemonic=%s' % (curve.mnemonic, curve.original_mnemonic))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    assert s.read() == '''~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M                  1670.0 : 
STOP.M                 1669.75 : 
STEP.M                  -0.125 : 
NULL.                  -999.25 : 
COMP.   # ANY OIL COMPANY LTD. : COMPANY
WELL.   ANY ET AL OIL WELL #12 : WELL
FLD .                     EDAM : FIELD
LOC .           A9-16-49-20W3M : LOCATION
PROV.             SASKATCHEWAN : PROVINCE
SRVC. ANY LOGGING COMPANY LTD. : SERVICE COMPANY
DATE.              25-DEC-1988 : LOG DATE
UWI .         100091604920W300 : UNIQUE WELL ID
~Curves ----------------------------------------------------
DEPT    .M     : 1  DEPTH
New_DT  .US/M  : 2  SONIC TRANSIT TIME
New_RHOB.K/M3  : 3  BULK DENSITY
New_NPHI.V/V   : 4   NEUTRON POROSITY
New_SFLU.OHMM  : 5  RXO RESISTIVITY
New_SFLA.OHMM  : 6  SHALLOW RESISTIVITY
New_ILM .OHMM  : 7  MEDIUM RESISTIVITY
New_ILD .OHMM  : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
BHT .DEGC   35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM    200.0 : BIT SIZE
FD  .K/M3 1000.0 : FLUID DENSITY
MATR.        0.0 : NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)
MDEN.     2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM  0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3 1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 meters causing the data
between 625 meters and 615 meters to be invalid.
~ASCII -----------------------------------------------------
       1670     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.9     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.8     123.45       2550       0.45     123.45     123.45      110.2      105.6
'''