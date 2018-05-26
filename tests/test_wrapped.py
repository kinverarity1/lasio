import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lasio import read

from lasio.reader import StringIO

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_wrapped():
    fn = egfn("1001178549.las")
    l = read(fn)

def test_write_wrapped():
    fn = stegfn("1.2", "sample_wrapped.las")
    l = read(fn)
    s = StringIO()
    l.write(s, version=2.0, wrap=True, fmt="%.5f")
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP. YES : Multiple lines per depth step
~Well ------------------------------------------------------
STRT.M                   910.0 : 
STOP.M                   909.5 : 
STEP.M                  -0.125 : 
NULL.                  -999.25 : Null value
COMP.     ANY OIL COMPANY INC. : COMPANY
WELL.    ANY ET AL XX-XX-XX-XX : WELL
FLD .                  WILDCAT : FIELD
LOC .           XX-XX-XX-XXW3M : LOCATION
PROV.             SASKATCHEWAN : PROVINCE
SRVC. ANY LOGGING COMPANY INC. : SERVICE COMPANY
SON .                   142085 : SERVICE ORDER
DATE.                13-DEC-86 : LOG DATE
UWI .                          : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.M     : Depth
DT  .US/M  : 1 Sonic Travel Time
RHOB.K/M   : 2 Density-Bulk Density
NPHI.V/V   : 3 Porosity -Neutron
RX0 .OHMM  : 4 Resistivity -Rxo
RESS.OHMM  : 5 Resistivity -Shallow
RESM.OHMM  : 6 Resistivity -Medium
RESD.OHMM  : 7 Resistivity -Deep
SP  .MV    : 8 Spon. Potential
GR  .GAPI  : 9 Gamma Ray
CALI.MM    : 10 Caliper
DRHO.K/M3  : 11 Delta-Rho
EATT.DBM   : 12 EPT Attenuation
TPL .NS/M  : 13 TP -EPT
PEF .      : 14 PhotoElectric Factor
FFI .V/V   : 15 Porosity -NML FFI
DCAL.MM    : 16 Caliper-Differential
RHGF.K/M3  : 17 Density-Formation
RHGA.K/M3  : 18 Density-Apparent
SPBL.MV    : 19 Baselined SP
GRC .GAPI  : 20 Gamma Ray BHC
PHIA.V/V   : 21 Porosity -Apparent
PHID.V/V   : 22 Porosity -Density
PHIE.V/V   : 23 Porosity -Effective
PHIN.V/V   : 24 Porosity -Neut BHC
PHIC.V/V   : 25 Porosity -Total HCC
R0  .OHMM  : 26 Ro
RWA .OHMM  : 27 Rfa
SW  .      : 28 Sw -Effective
MSI .      : 29 Sh Idx -Min
BVW .      : 30 BVW
FGAS.      : 31 Flag -Gas Index
PIDX.      : 32 Prod Idx
FBH .      : 33 Flag -Bad Hole
FHCC.      : 34 Flag -HC Correction
LSWB.      : 35 Flag -Limit SWB
~Params ----------------------------------------------------
~Other -----------------------------------------------------
~ASCII -----------------------------------------------------
  910.00000    -999.25 2692.70750    0.31400   19.40860   19.40860   13.17090
12.26810   -1.50100   96.53060  204.71770   30.58220    -999.25    -999.25
3.25150    -999.25    4.71770 3025.02640 3025.02640   -1.50100   93.13780
0.16410    0.01010    0.16410    0.31400    0.16410   11.13970    0.33040
0.95290    0.00000    0.15640    0.00000   11.13970    0.00000    0.00000
0.00000
  909.87500    -999.25 2712.64600    0.28860   23.39870   23.39870   13.61290
12.47440   -1.47200   90.28030  203.10930   18.75660    -999.25    -999.25
3.70580    -999.25    3.10930 3004.60500 3004.60500   -1.47200   86.90780
0.14560   -0.00150    0.14560    0.28860    0.14560   14.14280    0.26460
1.00000    0.00000    0.14560    0.00000   14.14280    0.00000    0.00000
0.00000
  909.75000    -999.25 2692.81370    0.27300   22.59090   22.59090   13.68210
12.61460   -1.48040   89.84920  201.92870    3.15510    -999.25    -999.25
4.31240    -999.25    1.92870 2976.44510 2976.44510   -1.48040   86.34650
0.14350    0.01010    0.14350    0.27300    0.14350   14.56740    0.25980
1.00000    0.00000    0.14350    0.00000   14.56740    0.00000    0.00000
0.00000
  909.62500    -999.25 2644.36500    0.27650   18.48310   18.48310   13.41590
12.69000   -1.50100   93.39990  201.58260   -6.58610    -999.25    -999.25
4.38220    -999.25    1.58260 2955.35280 2955.35280   -1.50100   89.71420
0.15900    0.03840    0.15900    0.27650    0.15900   11.86000    0.32100
0.96670    0.00000    0.15380    0.00000   11.86000    0.00000    0.00000
0.00000
  909.50000    -999.25 2586.28220    0.29960   13.91870   13.91870   12.91950
12.70160   -1.49160   98.12140  201.71260   -4.55740    -999.25    -999.25
3.59670    -999.25    1.71260 2953.59400 2953.59400   -1.49160   94.26700
0.18800    0.07230    0.18800    0.29960    0.18800    8.48630    0.44900
0.81740    0.00000    0.15370    0.00000    8.48630    0.00000    0.00000
0.00000
"""

def test_write_unwrapped():
    fn = stegfn("1.2", "sample_wrapped.las")
    l = read(fn)
    s = StringIO()
    l.write(s, version=2, wrap=False, fmt="%.5f")
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.  NO : One line per depth step
~Well ------------------------------------------------------
STRT.M                   910.0 : 
STOP.M                   909.5 : 
STEP.M                  -0.125 : 
NULL.                  -999.25 : Null value
COMP.     ANY OIL COMPANY INC. : COMPANY
WELL.    ANY ET AL XX-XX-XX-XX : WELL
FLD .                  WILDCAT : FIELD
LOC .           XX-XX-XX-XXW3M : LOCATION
PROV.             SASKATCHEWAN : PROVINCE
SRVC. ANY LOGGING COMPANY INC. : SERVICE COMPANY
SON .                   142085 : SERVICE ORDER
DATE.                13-DEC-86 : LOG DATE
UWI .                          : UNIQUE WELL ID
~Curve Information -----------------------------------------
DEPT.M     : Depth
DT  .US/M  : 1 Sonic Travel Time
RHOB.K/M   : 2 Density-Bulk Density
NPHI.V/V   : 3 Porosity -Neutron
RX0 .OHMM  : 4 Resistivity -Rxo
RESS.OHMM  : 5 Resistivity -Shallow
RESM.OHMM  : 6 Resistivity -Medium
RESD.OHMM  : 7 Resistivity -Deep
SP  .MV    : 8 Spon. Potential
GR  .GAPI  : 9 Gamma Ray
CALI.MM    : 10 Caliper
DRHO.K/M3  : 11 Delta-Rho
EATT.DBM   : 12 EPT Attenuation
TPL .NS/M  : 13 TP -EPT
PEF .      : 14 PhotoElectric Factor
FFI .V/V   : 15 Porosity -NML FFI
DCAL.MM    : 16 Caliper-Differential
RHGF.K/M3  : 17 Density-Formation
RHGA.K/M3  : 18 Density-Apparent
SPBL.MV    : 19 Baselined SP
GRC .GAPI  : 20 Gamma Ray BHC
PHIA.V/V   : 21 Porosity -Apparent
PHID.V/V   : 22 Porosity -Density
PHIE.V/V   : 23 Porosity -Effective
PHIN.V/V   : 24 Porosity -Neut BHC
PHIC.V/V   : 25 Porosity -Total HCC
R0  .OHMM  : 26 Ro
RWA .OHMM  : 27 Rfa
SW  .      : 28 Sw -Effective
MSI .      : 29 Sh Idx -Min
BVW .      : 30 BVW
FGAS.      : 31 Flag -Gas Index
PIDX.      : 32 Prod Idx
FBH .      : 33 Flag -Bad Hole
FHCC.      : 34 Flag -HC Correction
LSWB.      : 35 Flag -Limit SWB
~Params ----------------------------------------------------
~Other -----------------------------------------------------
~ASCII -----------------------------------------------------
  910.00000    -999.25 2692.70750    0.31400   19.40860   19.40860   13.17090   12.26810   -1.50100   96.53060  204.71770   30.58220    -999.25    -999.25    3.25150    -999.25    4.71770 3025.02640 3025.02640   -1.50100   93.13780    0.16410    0.01010    0.16410    0.31400    0.16410   11.13970    0.33040    0.95290    0.00000    0.15640    0.00000   11.13970    0.00000    0.00000    0.00000
  909.87500    -999.25 2712.64600    0.28860   23.39870   23.39870   13.61290   12.47440   -1.47200   90.28030  203.10930   18.75660    -999.25    -999.25    3.70580    -999.25    3.10930 3004.60500 3004.60500   -1.47200   86.90780    0.14560   -0.00150    0.14560    0.28860    0.14560   14.14280    0.26460    1.00000    0.00000    0.14560    0.00000   14.14280    0.00000    0.00000    0.00000
  909.75000    -999.25 2692.81370    0.27300   22.59090   22.59090   13.68210   12.61460   -1.48040   89.84920  201.92870    3.15510    -999.25    -999.25    4.31240    -999.25    1.92870 2976.44510 2976.44510   -1.48040   86.34650    0.14350    0.01010    0.14350    0.27300    0.14350   14.56740    0.25980    1.00000    0.00000    0.14350    0.00000   14.56740    0.00000    0.00000    0.00000
  909.62500    -999.25 2644.36500    0.27650   18.48310   18.48310   13.41590   12.69000   -1.50100   93.39990  201.58260   -6.58610    -999.25    -999.25    4.38220    -999.25    1.58260 2955.35280 2955.35280   -1.50100   89.71420    0.15900    0.03840    0.15900    0.27650    0.15900   11.86000    0.32100    0.96670    0.00000    0.15380    0.00000   11.86000    0.00000    0.00000    0.00000
  909.50000    -999.25 2586.28220    0.29960   13.91870   13.91870   12.91950   12.70160   -1.49160   98.12140  201.71260   -4.55740    -999.25    -999.25    3.59670    -999.25    1.71260 2953.59400 2953.59400   -1.49160   94.26700    0.18800    0.07230    0.18800    0.29960    0.18800    8.48630    0.44900    0.81740    0.00000    0.15370    0.00000    8.48630    0.00000    0.00000    0.00000
"""