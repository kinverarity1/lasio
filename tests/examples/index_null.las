~VERSION INFORMATION
 VERS.                          2.0 :   CWLS LOG ASCII STANDARD -VERSION 2.0
 WRAP.                          NO  :   ONE LINE PER DEPTH STEP
~WELL INFORMATION
#MNEM.UNIT              DATA                       DESCRIPTION
#----- -----            ----------               -------------------------
STRT    .M              999.50                  :START DEPTH
STOP    .M              999.00                  :STOP DEPTH
STEP    .M              0.2500                  :STEP
NULL    .               999.25                  :NULL VALUE
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
~PARAMETER INFORMATION
~OTHER
~A  DEPTH     DT    RHOB        NPHI
999.00      999.25  123.450  110.200
999.25     123.450  123.450  110.200
999.50     123.450  123.450   999.25
