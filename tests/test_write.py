import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import numpy as np

import lasio
from lasio import read
from lasio.excel import ExcelConverter

from lasio.reader import StringIO

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)


def test_write_sect_widths_12(capsys):
    las = lasio.read(egfn("sample_write_sect_widths_12.las"))
    las.write(sys.stdout, version=1.2)
    assert capsys.readouterr()[0] == open(egfn('test_write_sect_widths_12.txt')).read()

def test_write_to_filename():
    las = read(egfn("sample_write_sect_widths_12.las"))
    las.write('test.las', version=1.2)
    assert os.path.isfile('test.las')
    os.remove('test.las')


def test_write_sect_widths_12_curves():
    l = read(egfn("sample_write_sect_widths_12.las"))
    s = StringIO()
    l.write(s, version=1.2)
    for start in ("D.M ", "A.US/M ", "B.K/M3 ", "C.V/V "):
        s.seek(0)
        assert "\n" + start in s.read()


def test_write_sect_widths_20_narrow():
    l = read(egfn("sample_write_sect_widths_20_narrow.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M   1670.0 : START DEPTH
STOP.M  1669.75 : STOP DEPTH
STEP.M   -0.125 : STEP
NULL.   -999.25 : NULL VALUE
COMP.       ANY : COMPANY
WELL.   AAAAA_2 : WELL
FLD .   WILDCAT : FIELD
LOC .        12 : LOCATION
PROV.   ALBERTA : PROVINCE
SRVC.   LOGGING : SERVICE COMPANY ARE YOU KIDDING THIS IS A REALLY REALLY LONG STRING
DATE. 13-DEC-86 : LOG DATE
UWI .  10012340 : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.M                 : 1  DEPTH
DT  .US/M 60 520 32 00 : 2  SONIC TRANSIT TIME
RHOB.K/M3 45 350 01 00 : 3  BULK DENSITY
NPHI.V/V  42 890 00 00 : 4  NEUTRON POROSITY
SFLU.OHMM 07 220 04 00 : 5  SHALLOW RESISTIVITY
SFLA.OHMM 07 222 01 00 : 6  SHALLOW RESISTIVITY
ILM .OHMM 07 120 44 00 : 7  MEDIUM RESISTIVITY
ILD .OHMM 07 120 46 00 : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
MUD .   GEL CHEM : MUD TYPE
BHT .DEGC   35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM    200.0 : BIT SIZE
FD  .K/M3 1000.0 : FLUID DENSITY
MATR.       SAND : NEUTRON MATRIX
MDEN.     2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM  0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3 1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 metres causing the data
between 625 metres and 615 metres to be invalid.
~ASCII -----------------------------------------------------
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.87500  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.75000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
"""


def test_write_sect_widths_20_wide():
    l = read(egfn("sample_write_sect_widths_20_wide.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M                                                         1670.0 : START DEPTH
STOP.M                                                        1669.75 : STOP DEPTH
STEP.M                                                         -0.125 : STEP
NULL.                                                         -999.25 : NULL VALUE
COMP.                                            ANY OIL COMPANY INC. : COMPANY
WELL.                                                         AAAAA_2 : WELL
FLD .                                                         WILDCAT : FIELD
LOC .                                                  12-34-12-34W5M : LOCATION
PROV.                                                         ALBERTA : PROVINCE
SRVC. The company that did this logging has a very very long name.... : SERVICE COMPANY
DATE.                                                       13-DEC-86 : LOG DATE
UWI .                                                100123401234W500 : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.M                 : 1  DEPTH
DT  .US/M 60 520 32 00 : 2  SONIC TRANSIT TIME
RHOB.K/M3 45 350 01 00 : 3  BULK DENSITY
NPHI.V/V  42 890 00 00 : 4  NEUTRON POROSITY
SFLU.OHMM 07 220 04 00 : 5  SHALLOW RESISTIVITY
SFLA.OHMM 07 222 01 00 : 6  SHALLOW RESISTIVITY
ILM .OHMM 07 120 44 00 : 7  MEDIUM RESISTIVITY
ILD .OHMM 07 120 46 00 : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
MUD .   GEL CHEM : MUD TYPE
BHT .DEGC   35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM    200.0 : BIT SIZE
FD  .K/M3 1000.0 : FLUID DENSITY
MATR.       SAND : NEUTRON MATRIX
MDEN.     2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM  0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3 1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 metres causing the data
between 625 metres and 615 metres to be invalid.
~ASCII -----------------------------------------------------
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.87500  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.75000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
"""

def test_write_sample_empty_params():
    l = read(egfn("sample_write_empty_params.las"))
    l.write(StringIO(), version=2)

def test_df_curve_addition_on_export():
    l = read(egfn("sample.las"))
    df = l.df()
    df["ILD_COND"] = 1000 / df.ILD
    l.set_data_from_df(df, truncate=False)
    s = StringIO()
    l.write(s, version=2, wrap=False, fmt="%.5f")
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : One line per depth step
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
~Curve Information -----------------------------------------
DEPT    .M     : 1  DEPTH
DT      .US/M  : 2  SONIC TRANSIT TIME
RHOB    .K/M3  : 3  BULK DENSITY
NPHI    .V/V   : 4   NEUTRON POROSITY
SFLU    .OHMM  : 5  RXO RESISTIVITY
SFLA    .OHMM  : 6  SHALLOW RESISTIVITY
ILM     .OHMM  : 7  MEDIUM RESISTIVITY
ILD     .OHMM  : 8  DEEP RESISTIVITY
ILD_COND.      : 
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
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000    9.46970
 1669.87500  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000    9.46970
 1669.75000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000    9.46970
"""

def test_write_xlsx():
    l = read(egfn("sample.las"))
    e = ExcelConverter(l)
    xlsxfn = "test.xlsx"
    e.write(xlsxfn)
    os.remove(xlsxfn)

def test_export_xlsx():
    l = read(egfn("sample.las"))
    xlsxfn = "test2.xlsx"
    l.to_excel(xlsxfn)
    os.remove(xlsxfn)

def test_multi_curve_mnemonics_rewrite():
    l = read(egfn('sample_issue105_a.las'))
    s = StringIO()
    l.write(s, version=2, wrap=False, fmt="%.5f")
    s.seek(0)
    assert s.read() == '''~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : One line per depth step
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
~Curve Information -----------------------------------------
DEPT.M     : 1  DEPTH
RHO .ohmm  : curve 1,2,3
RHO .ohmm  : curve 10,20,30
RHO .ohmm  : curve 100,200,300
PHI .      : porosity
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
 1670.00000    1.00000   10.00000  100.00000    0.10000
 1669.87500    2.00000   20.00000  200.00000    0.20000
 1669.75000    3.00000   30.00000  300.00000    0.30000
'''

def test_multi_curve_missing_mnemonics_rewrite():
    l = read(egfn('sample_issue105_b.las'))
    s = StringIO()
    l.write(s, version=2, wrap=False, fmt="%.5f")
    s.seek(0)
    assert s.read() == '''~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : One line per depth step
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
~Curve Information -----------------------------------------
DEPT.M     : 1  DEPTH
    .ohmm  : curve 1,2,3
    .ohmm  : curve 10,20,30
    .ohmm  : curve 100,200,300
PHI .      : porosity
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
 1670.00000    1.00000   10.00000  100.00000    0.10000
 1669.87500    2.00000   20.00000  200.00000    0.20000
 1669.75000    3.00000   30.00000  300.00000    0.30000
'''

def test_write_units():
    l = read(egfn("sample.las"))
    l.curves[0].unit = 'FT'
    s = StringIO()
    l.write(s, version=2, wrap=False, fmt="%.5f")
    s.seek(0)
    assert s.read() == '''~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : One line per depth step
~Well ------------------------------------------------------
STRT.FT                 1670.0 : 
STOP.FT                1669.75 : 
STEP.FT                 -0.125 : 
NULL.                  -999.25 : 
COMP.   # ANY OIL COMPANY LTD. : COMPANY
WELL.   ANY ET AL OIL WELL #12 : WELL
FLD .                     EDAM : FIELD
LOC .           A9-16-49-20W3M : LOCATION
PROV.             SASKATCHEWAN : PROVINCE
SRVC. ANY LOGGING COMPANY LTD. : SERVICE COMPANY
DATE.              25-DEC-1988 : LOG DATE
UWI .         100091604920W300 : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.FT    : 1  DEPTH
DT  .US/M  : 2  SONIC TRANSIT TIME
RHOB.K/M3  : 3  BULK DENSITY
NPHI.V/V   : 4   NEUTRON POROSITY
SFLU.OHMM  : 5  RXO RESISTIVITY
SFLA.OHMM  : 6  SHALLOW RESISTIVITY
ILM .OHMM  : 7  MEDIUM RESISTIVITY
ILD .OHMM  : 8  DEEP RESISTIVITY
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
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.87500  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.75000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
'''

def test_to_csv_units_None():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', units_loc=None)
    csv_output = open('test.csv', 'r').readlines()
    proof_output = open(egfn('sample.las_units-none.csv'), 'r').readlines()
    os.remove('test.csv')
    assert csv_output[0] == proof_output[0]
    # assert csv_output[1] == proof_output[1]

def test_to_csv_units_line():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', units_loc='line')
    csv_output = open('test.csv', 'r').readlines()
    proof_output = open(egfn('sample.las_units-line.csv'), 'r').readlines()
    os.remove('test.csv')
    assert csv_output[0] == proof_output[0]
    assert csv_output[1] == proof_output[1]

def test_to_csv_units_parentheses():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', units_loc='()')
    csv_output = open('test.csv', 'r').readlines()
    proof_output = open(egfn('sample.las_units-parentheses.csv'), 'r').readlines()
    os.remove('test.csv')
    assert csv_output[0] == proof_output[0]

def test_to_csv_units_brackets():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', units_loc='[]')
    csv_output = open('test.csv', 'r').readlines()
    proof_output = open(egfn('sample.las_units-brackets.csv'), 'r').readlines()
    os.remove('test.csv')
    assert csv_output[0] == proof_output[0]
    # assert csv_output[1] == proof_output[1]

def test_to_csv_specify_mnemonics():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', mnemonics=[str(i) for i in range(len(las.curves))])
    csv_output = open('test.csv', 'r').readlines()
    assert csv_output[0] == '0,1,2,3,4,5,6,7\n'
    os.remove('test.csv')

def test_to_csv_specify_units():
    las = read(egfn("sample.las"))
    las.to_csv('test.csv', units=[str(i) for i in range(len(las.curves))])
    csv_output = open('test.csv', 'r').readlines()
    assert csv_output[1] == '0,1,2,3,4,5,6,7\n'
    os.remove('test.csv')


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
~Curve Information -----------------------------------------
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
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.87500  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
 1669.75000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
'''

def test_write_large_depths():
    las = lasio.read(egfn("sample.las"))
    las.curves[0].data *= 10.5 + 0.1
    las.write('write_large_depths.las')
    las2 = lasio.read('write_large_depths.las')
    os.remove('write_large_depths.las')
    assert np.all(las.curves[0].data == las2.curves[0].data)

def test_write_single_step():
    las = lasio.read(egfn("single_step_20.las"))
    s = StringIO()
    las.write(s, version=2)
    s.seek(0)
    assert s.read() == '''~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M                  1670.0 : START DEPTH
STOP.M                  1670.0 : STOP DEPTH
STEP.M                    None : STEP
NULL.                  -999.25 : NULL VALUE
COMP.     ANY OIL COMPANY INC. : COMPANY
WELL.                  AAAAA_2 : WELL
FLD .                  WILDCAT : FIELD
LOC .           12-34-12-34W5M : LOCATION
PROV.                  ALBERTA : PROVINCE
SRVC. ANY LOGGING COMPANY INC. : SERVICE COMPANY
DATE.                13-DEC-86 : LOG DATE
UWI .         100123401234W500 : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.M                 : 1  DEPTH
DT  .US/M 60 520 32 00 : 2  SONIC TRANSIT TIME
RHOB.K/M3 45 350 01 00 : 3  BULK DENSITY
NPHI.V/V  42 890 00 00 : 4  NEUTRON POROSITY
SFLU.OHMM 07 220 04 00 : 5  SHALLOW RESISTIVITY
SFLA.OHMM 07 222 01 00 : 6  SHALLOW RESISTIVITY
ILM .OHMM 07 120 44 00 : 7  MEDIUM RESISTIVITY
ILD .OHMM 07 120 46 00 : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
MUD .   GEL CHEM : MUD TYPE
BHT .DEGC   35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM    200.0 : BIT SIZE
FD  .K/M3 1000.0 : FLUID DENSITY
MATR.       SAND : NEUTRON MATRIX
MDEN.     2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM  0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3 1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 metres causing the data
between 625 metres and 615 metres to be invalid.
~ASCII -----------------------------------------------------
 1670.00000  123.45000 2550.00000    0.45000  123.45000  123.45000  110.20000  105.60000
'''
