Writing LAS files
============================

Any LASFile object can be written to a new LAS file using the
:meth:`lasio.LASFile.write` method.

Converting between v1.2 and v2.0
--------------------------------

Take this sample LAS 2.0 file:

.. code-block:: none
    :linenos:

    ~VERSION INFORMATION
     VERS.                          2.0 :   CWLS LOG ASCII STANDARD -VERSION 2.0
     WRAP.                          NO  :   ONE LINE PER DEPTH STEP
    ~WELL INFORMATION
    #MNEM.UNIT              DATA                       DESCRIPTION
    #----- -----            ----------               -------------------------
    STRT    .M              1670.0000                :START DEPTH
    STOP    .M              1660.0000                :STOP DEPTH
    STEP    .M              -0.1250                  :STEP
    NULL    .               -999.25                  :NULL VALUE
    COMP    .       ANY OIL COMPANY INC.             :COMPANY
    WELL    .       AAAAA_2            :WELL
    FLD     .       WILDCAT                          :FIELD
    LOC     .       12-34-12-34W5M                   :LOCATION
    PROV    .       ALBERTA                          :PROVINCE
    SRVC    .       ANY LOGGING COMPANY INC.         :SERVICE COMPANY
    DATE    .       13-DEC-86                        :LOG DATE
    UWI     .       100123401234W500                 :UNIQUE WELL ID
    ~CURVE INFORMATION
    #MNEM.UNIT              API CODES                   CURVE DESCRIPTION
    #------------------     ------------              -------------------------
     DEPT   .M                                       :  1  DEPTH
     DT     .US/M           60 520 32 00             :  2  SONIC TRANSIT TIME
     RHOB   .K/M3           45 350 01 00             :  3  BULK DENSITY
     NPHI   .V/V            42 890 00 00             :  4  NEUTRON POROSITY
     SFLU   .OHMM           07 220 04 00             :  5  SHALLOW RESISTIVITY
     SFLA   .OHMM           07 222 01 00             :  6  SHALLOW RESISTIVITY
     ILM    .OHMM           07 120 44 00             :  7  MEDIUM RESISTIVITY
     ILD    .OHMM           07 120 46 00             :  8  DEEP RESISTIVITY
    ~PARAMETER INFORMATION
    #MNEM.UNIT              VALUE             DESCRIPTION
    #--------------     ----------------      -----------------------------------------------
     MUD    .               GEL CHEM        :   MUD TYPE
     BHT    .DEGC           35.5000         :   BOTTOM HOLE TEMPERATURE
     BS     .MM             200.0000        :   BIT SIZE
     FD     .K/M3           1000.0000       :   FLUID DENSITY
     MATR   .               SAND            :   NEUTRON MATRIX
     MDEN   .               2710.0000       :   LOGGING MATRIX DENSITY
     RMF    .OHMM           0.2160          :   MUD FILTRATE RESISTIVITY
     DFD    .K/M3           1525.0000       :   DRILL FLUID DENSITY
    ~OTHER
         Note: The logging tools became stuck at 625 metres causing the data
         between 625 metres and 615 metres to be invalid.
    ~A  DEPTH     DT    RHOB        NPHI   SFLU    SFLA      ILM      ILD
    1670.000   123.450 2550.000    0.450  123.450  123.450  110.200  105.600
    1669.875   123.450 2550.000    0.450  123.450  123.450  110.200  105.600
    1669.750   123.450 2550.000    0.450  123.450  123.450  110.200  105.600

And we can use ``lasio`` to convert it to LAS 1.2:

.. code-block:: ipython

    In [31]: las = lasio.read("tests/examples/2.0/sample_2.0.las")

    In [33]: las.write('example-as-v1.2.las', version=1.2)

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS. 1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
    WRAP.  NO : ONE LINE PER DEPTH STEP
    ~Well ------------------------------------------------------
    STRT.M         1670.0 : START DEPTH
    STOP.M        1669.75 : STOP DEPTH
    STEP.M         -0.125 : STEP
    NULL.         -999.25 : NULL VALUE
    COMP.         COMPANY : ANY OIL COMPANY INC.
    WELL.            WELL : AAAAA_2
    FLD .           FIELD : WILDCAT
    LOC .        LOCATION : 12-34-12-34W5M
    PROV.        PROVINCE : ALBERTA
    SRVC. SERVICE COMPANY : ANY LOGGING COMPANY INC.
    DATE.        LOG DATE : 13-DEC-86
    UWI .  UNIQUE WELL ID : 100123401234W500
    ~Curves ----------------------------------------------------
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
           1670     123.45       2550       0.45     123.45     123.45      110.2      105.6
         1669.9     123.45       2550       0.45     123.45     123.45      110.2      105.6
         1669.8     123.45       2550       0.45     123.45     123.45      110.2      105.6

Converting between wrapped/unwrapped
------------------------------------

Here is an example using this file to convert a wrapped data section to
unwrapped.

.. code-block:: none
    :linenos:

    ~Version Information
     VERS.                1.20:   CWLS log ASCII Standard -VERSION 1.20
     WRAP.                 YES:   Multiple lines per depth step
    ~Well Information
    #MNEM.UNIT       Data Type    Information
    #---------    -------------   ------------------------------
     STRT.M            910.000:
     STOP.M            901.000:
     STEP.M            -0.1250:
     NULL.           -999.2500:   Null value
     COMP.             COMPANY:   ANY OIL COMPANY INC.
     WELL.                WELL:   ANY ET AL XX-XX-XX-XX
     FLD .               FIELD:   WILDCAT
     LOC .            LOCATION:   XX-XX-XX-XXW3M
     PROV.            PROVINCE:   SASKATCHEWAN
     SRVC.     SERVICE COMPANY:   ANY LOGGING COMPANY INC.
     SON .     SERVICE ORDER :   142085
     DATE.            LOG DATE:   13-DEC-86
     UWI .      UNIQUE WELL ID:
    ~Curve Information
    #MNEM.UNIT      API CODE      Curve Description
    #---------    -------------   ------------------------------
     DEPT.M                       :    Depth
     DT  .US/M                    :  1 Sonic Travel Time
     RHOB.K/M                     :  2 Density-Bulk Density
     NPHI.V/V                     :  3 Porosity -Neutron
     RX0 .OHMM                    :  4 Resistivity -Rxo
     RESS.OHMM                    :  5 Resistivity -Shallow
     RESM.OHMM                    :  6 Resistivity -Medium
     RESD.OHMM                    :  7 Resistivity -Deep
     SP  .MV                      :  8 Spon. Potential
     GR  .GAPI                    :  9 Gamma Ray
     CALI.MM                      : 10 Caliper
     DRHO.K/M3                    : 11 Delta-Rho
     EATT.DBM                     : 12 EPT Attenuation
     TPL .NS/M                    : 13 TP -EPT
     PEF .                        : 14 PhotoElectric Factor
     FFI .V/V                     : 15 Porosity -NML FFI
     DCAL.MM                      : 16 Caliper-Differential
     RHGF.K/M3                    : 17 Density-Formation
     RHGA.K/M3                    : 18 Density-Apparent
     SPBL.MV                      : 19 Baselined SP
     GRC .GAPI                    : 20 Gamma Ray BHC
     PHIA.V/V                     : 21 Porosity -Apparent
     PHID.V/V                     : 22 Porosity -Density
     PHIE.V/V                     : 23 Porosity -Effective
     PHIN.V/V                     : 24 Porosity -Neut BHC
     PHIC.V/V                     : 25 Porosity -Total HCC
     R0  .OHMM                    : 26 Ro
     RWA .OHMM                    : 27 Rfa
     SW   .                       : 28 Sw -Effective
     MSI .                        : 29 Sh Idx -Min
     BVW .                        : 30 BVW
     FGAS.                        : 31 Flag -Gas Index
     PIDX.                        : 32 Prod Idx
     FBH .                        : 33 Flag -Bad Hole
     FHCC.                        : 34 Flag -HC Correction
     LSWB.                        : 35 Flag -Limit SWB
    ~A Log data section
    910.000000
      -999.2500  2692.7075     0.3140    19.4086    19.4086    13.1709    12.2681
        -1.5010    96.5306   204.7177    30.5822  -999.2500  -999.2500     3.2515
      -999.2500     4.7177  3025.0264  3025.0264    -1.5010    93.1378     0.1641
         0.0101     0.1641     0.3140     0.1641    11.1397     0.3304     0.9529
         0.0000     0.1564     0.0000    11.1397     0.0000     0.0000     0.0000
    909.875000
      -999.2500  2712.6460     0.2886    23.3987    23.3987    13.6129    12.4744
        -1.4720    90.2803   203.1093    18.7566  -999.2500  -999.2500     3.7058
      -999.2500     3.1093  3004.6050  3004.6050    -1.4720    86.9078     0.1456
        -0.0015     0.1456     0.2886     0.1456    14.1428     0.2646     1.0000
         0.0000     0.1456     0.0000    14.1428     0.0000     0.0000     0.0000
    909.750000
      -999.2500  2692.8137     0.2730    22.5909    22.5909    13.6821    12.6146
        -1.4804    89.8492   201.9287     3.1551  -999.2500  -999.2500     4.3124
      -999.2500     1.9287  2976.4451  2976.4451    -1.4804    86.3465     0.1435
         0.0101     0.1435     0.2730     0.1435    14.5674     0.2598     1.0000
         0.0000     0.1435     0.0000    14.5674     0.0000     0.0000     0.0000
    909.625000
      -999.2500  2644.3650     0.2765    18.4831    18.4831    13.4159    12.6900
        -1.5010    93.3999   201.5826    -6.5861  -999.2500  -999.2500     4.3822
      -999.2500     1.5826  2955.3528  2955.3528    -1.5010    89.7142     0.1590
         0.0384     0.1590     0.2765     0.1590    11.8600     0.3210     0.9667
         0.0000     0.1538     0.0000    11.8600     0.0000     0.0000     0.0000
    909.500000
      -999.2500  2586.2822     0.2996    13.9187    13.9187    12.9195    12.7016
        -1.4916    98.1214   201.7126    -4.5574  -999.2500  -999.2500     3.5967
      -999.2500     1.7126  2953.5940  2953.5940    -1.4916    94.2670     0.1880
         0.0723     0.1880     0.2996     0.1880     8.4863     0.4490     0.8174
         0.0000     0.1537     0.0000     8.4863     0.0000     0.0000     0.0000

We will change the wrap by adjusting the relevant header section in the LASFile
header:

.. code-block:: ipython

    In [26]: las.version
    Out[26]:
    [HeaderItem(mnemonic=VERS, unit=, value=1.2, descr=CWLS log ASCII Standard -VERSION 1.20, original_mnemonic=VERS),
     HeaderItem(mnemonic=WRAP, unit=, value=YES, descr=Multiple lines per depth step, original_mnemonic=WRAP)]

    In [27]: las.version.WRAP = 'NO'

    In [28]: las.version.WRAP
    Out[28]: HeaderItem(mnemonic=WRAP, unit=, value=NO, descr=Multiple lines per depth step, original_mnemonic=WRAP)

    In [29]: las.write('example-unwrapped.las')
    WARNING:lasio.writer:[v1.2] line #58 has 396 chars (>256)
    WARNING:lasio.writer:[v1.2] line #59 has 396 chars (>256)
    WARNING:lasio.writer:[v1.2] line #60 has 396 chars (>256)
    WARNING:lasio.writer:[v1.2] line #61 has 396 chars (>256)
    WARNING:lasio.writer:[v1.2] line #62 has 396 chars (>256)

We get warnings because the LAS 1.2 standard doesn't allow writing lines longer
than 256 characters. ``lasio`` provides the warning but still produces the long
lines:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS. 1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
    WRAP.  NO : Multiple lines per depth step
    ~Well ------------------------------------------------------
    STRT.M          910.0 :
    STOP.M          909.5 :
    STEP.M         -0.125 :
    NULL.         -999.25 : Null value
    COMP.         COMPANY : ANY OIL COMPANY INC.
    WELL.            WELL : ANY ET AL XX-XX-XX-XX
    FLD .           FIELD : WILDCAT
    LOC .        LOCATION : XX-XX-XX-XXW3M
    PROV.        PROVINCE : SASKATCHEWAN
    SRVC. SERVICE COMPANY : ANY LOGGING COMPANY INC.
    SON .   SERVICE ORDER : 142085
    DATE.        LOG DATE : 13-DEC-86
    UWI .  UNIQUE WELL ID :
    ~Curves ----------------------------------------------------
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
            910    -999.25     2692.7      0.314     19.409     19.409     13.171     12.268     -1.501     96.531     204.72     30.582    -999.25    -999.25     3.2515    -999.25     4.7177       3025       3025     -1.501     93.138     0.1641     0.0101     0.1641      0.314     0.1641      11.14     0.3304     0.9529          0     0.1564          0      11.14          0          0          0
         909.88    -999.25     2712.6     0.2886     23.399     23.399     13.613     12.474     -1.472      90.28     203.11     18.757    -999.25    -999.25     3.7058    -999.25     3.1093     3004.6     3004.6     -1.472     86.908     0.1456    -0.0015     0.1456     0.2886     0.1456     14.143     0.2646          1          0     0.1456          0     14.143          0          0          0
         909.75    -999.25     2692.8      0.273     22.591     22.591     13.682     12.615    -1.4804     89.849     201.93     3.1551    -999.25    -999.25     4.3124    -999.25     1.9287     2976.4     2976.4    -1.4804     86.347     0.1435     0.0101     0.1435      0.273     0.1435     14.567     0.2598          1          0     0.1435          0     14.567          0          0          0
         909.62    -999.25     2644.4     0.2765     18.483     18.483     13.416      12.69     -1.501       93.4     201.58    -6.5861    -999.25    -999.25     4.3822    -999.25     1.5826     2955.4     2955.4     -1.501     89.714      0.159     0.0384      0.159     0.2765      0.159      11.86      0.321     0.9667          0     0.1538          0      11.86          0          0          0
          909.5    -999.25     2586.3     0.2996     13.919     13.919     12.919     12.702    -1.4916     98.121     201.71    -4.5574    -999.25    -999.25     3.5967    -999.25     1.7126     2953.6     2953.6    -1.4916     94.267      0.188     0.0723      0.188     0.2996      0.188     8.4863      0.449     0.8174          0     0.1537          0     8.4863          0          0          0

If we decide to write the file in LAS 2.0 format, the warnings will go away:

.. code-block:: ipython

    In [23]: las.write('example-version-2.0.las', version=2.0)

    In [24]:

.. code-block:: none
    :linenos:

    ~Version ---------------------------------------------------
    VERS. 2.0 : CWLS log ASCII Standard -VERSION 2.0
    WRAP.  NO : Multiple lines per depth step
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
    ~Curves ----------------------------------------------------
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
            910    -999.25     2692.7      0.314     19.409     19.409     13.171     12.268     -1.501     96.531     204.72     30.582    -999.25    -999.25     3.2515    -999.25     4.7177       3025       3025     -1.501     93.138     0.1641     0.0101     0.1641      0.314     0.1641      11.14     0.3304     0.9529          0     0.1564          0      11.14          0          0          0
         909.88    -999.25     2712.6     0.2886     23.399     23.399     13.613     12.474     -1.472      90.28     203.11     18.757    -999.25    -999.25     3.7058    -999.25     3.1093     3004.6     3004.6     -1.472     86.908     0.1456    -0.0015     0.1456     0.2886     0.1456     14.143     0.2646          1          0     0.1456          0     14.143          0          0          0
         909.75    -999.25     2692.8      0.273     22.591     22.591     13.682     12.615    -1.4804     89.849     201.93     3.1551    -999.25    -999.25     4.3124    -999.25     1.9287     2976.4     2976.4    -1.4804     86.347     0.1435     0.0101     0.1435      0.273     0.1435     14.567     0.2598          1          0     0.1435          0     14.567          0          0          0
         909.62    -999.25     2644.4     0.2765     18.483     18.483     13.416      12.69     -1.501       93.4     201.58    -6.5861    -999.25    -999.25     4.3822    -999.25     1.5826     2955.4     2955.4     -1.501     89.714      0.159     0.0384      0.159     0.2765      0.159      11.86      0.321     0.9667          0     0.1538          0      11.86          0          0          0
          909.5    -999.25     2586.3     0.2996     13.919     13.919     12.919     12.702    -1.4916     98.121     201.71    -4.5574    -999.25    -999.25     3.5967    -999.25     1.7126     2953.6     2953.6    -1.4916     94.267      0.188     0.0723      0.188     0.2996      0.188     8.4863      0.449     0.8174          0     0.1537          0     8.4863          0          0          0

