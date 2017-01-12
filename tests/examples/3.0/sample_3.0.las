~VERSION INFORMATION
 VERS.                          3.0 : CWLS LOG ASCII STANDARD -VERSION 3.0
 WRAP.                           NO : ONE LINE PER DEPTH STEP
 DLM .                        COMMA : DELIMITING CHARACTER BETWEEN DATA COLUMNS 
# Acceptable delimiting characters: SPACE (default), TAB, OR COMMA.
~Well Information
#MNEM.UNIT              DATA                       DESCRIPTION
#----- -----            ----------               -------------------------
 STRT .M              1670.0000                : First Index Value
 STOP .M               713.2500                : Last Index Value 
 STEP .M              -0.1250                  : STEP 
 NULL .               -999.25                  : NULL VALUE
 COMP .       ANY OIL COMPANY INC.             : COMPANY
 WELL .       ANY ET AL 12-34-12-34            : WELL
 FLD  .       WILDCAT                          : FIELD
 LOC  .       12-34-12-34W5M                   : LOCATION
 PROV .       ALBERTA                          : PROVINCE 
 SRVC .       ANY LOGGING COMPANY INC.         : SERVICE COMPANY
 DATE .       13/12/1986                       : LOG DATE  {DD/MM/YYYY}
 UWI  .       100123401234W500                 : UNIQUE WELL ID
 API  .       12345678                         : API NUMBER
 LAT .DEG                             34.56789 : Latitude  {DEG}
 LONG.DEG                           -102.34567 : Longitude  {DEG}
# Lat & Long can also be presented as:
# LAT .DEG                           34/34/4.4 : Latitude  {DEG/MIN/SEC}
# LONG.DEG                        -102/20/44.4 : Longitude  {DEG/MIN/SEC}
 UTM  .                                        : UTM LOCATION
~CURVE INFORMATION
#MNEM.UNIT             LOG CODES                   CURVE DESCRIPTION
#----------------     -----------              -------------------------
# Format of value in data section F=float, E=0.00E00 S=string
 DEPT .M                                       : DEPTH               {F} 
 DT   .US/M           123 456 789              : SONIC TRANSIT TIME  {F} 
 RHOB .K/M3           123 456 789              : BULK DENSITY        {F}
 NPHI .V/V            123 456 789              : NEUTRON POROSITY    {F}       
 SFLU .OHMM           123 456 789              : SHALLOW RESISTIVITY {F}
 SFLA .OHMM           123 456 789              : SHALLOW RESISTIVITY {F}
 ILM  .OHMM           123 456 789              : MEDIUM RESISTIVITY  {F}
 ILD  .OHMM           123 456 789              : DEEP RESISTIVITY    {F}
 YME  .PA             123 456 789              : YOUNGS MODULES      {E}
 CDES .               123 456 789              : CORE DESCRIPTION    {S} 
# A 2D array channel begins here. It has 5 elements.
# value after A: is time spacing of this array element from first element.
 NMR[1] .ms           123 456 789              : NMR Echo Array      {A:0 } 
 NMR[2] .ms           123 456 789              : NMR Echo Array      {A:5 }          
 NMR[3] .ms           123 456 789              : NMR Echo Array      {A:10}          
 NMR[4] .ms           123 456 789              : NMR Echo Array      {A:15}          
 NMR[5] .ms           123 456 789              : NMR Echo Array      {A:20}          
~PARAMETER INFORMATION
#MNEM.UNIT              VALUE             DESCRIPTION
#--------------     ----------------      ---------------------------
 RUNS.  2              : of Runs for this well.
 RUN[1].            1  : Run 1
 RUN[2].            2  : Run 2

#Parameters that are zoned.
 NMAT_Depth[1].M  500,1500     : Neutron Matrix Depth interval {F}               
 NMAT_Depth[2].M  1500,2500    : Neutron Matrix Depth interval {F}                                 
 DMAT_Depth[1].M  500,1510     : Density Matrix Depth interval {F}                  
 DMAT_Depth[2].M  1510,2510    : Density Matrix Depth interval {F}                  

#Service Company specific Parameters
 MATR .            SAND : Neutron Porosity Matrix          |  NMAT_Depth[1]
 MATR .            LIME : Neutron Porosity Matrix          |  NMAT_Depth[2]
 MDEN .KG/M3       2650 : Matrix Bulk Density              |  DMAT_Depth[1]    
 MDEN .KG/M3       2710 : Matrix Bulk Density              |  DMAT_Depth[2]

#Required Parameters
#Run 1 Parameters
 RUN_DEPTH.M      0, 1500  : Run 1 Depth Interval  {F}    | Run[1]       
 RUN_DATE.     12/09/1998  : Run 1 date  {DD/MM/YYYY}     | Run[1]
 DREF .                : Depth Reference (KB,DF,CB)       | RUN[1]       
 EREF .M               : Elevation of Depth Reference     | RUN[1]       
 TDL  .M               : Total Depth Logger               | RUN[1]       
 TDD  .M               : Total Depth Driller              | RUN[1]       
 CSGL .M               : Casing Bottom Logger             | RUN[1]       
 CSGD .M               : Casing Bottom Driller            | RUN[1]       
 CSGS .MM              : Casing Size                      | RUN[1]       
 CSGW .KG/M            : Casing Weight                    | RUN[1]       
 BS   .MM              : Bit Size                         | RUN[1]       
 MUD  .                : Mud type                         | RUN[1]       
 MUDS .                : Mud Source                       | RUN[1]       
 MUDD .KG/M3           : Mud Density                      | RUN[1]       
 MUDV .S               : Mud Viscosity (Funnel)           | RUN[1]       
 FL   .CC              : Fluid Loss                       | RUN[1]       
 PH   .                : PH                               | RUN[1]       
 RM   .OHMM            : Resistivity of Mud               | RUN[1]       
 RMT  .DEGC            : Temperature of Mud               | RUN[1]       
 RMF  .OHMM            : Rest. of Mud Filtrate            | RUN[1]       
 RMFT .DEGC            : Temp. of Mud Filtrate            | RUN[1]       
 RMC  .OHMM            : Rest. of Mud Cake                | RUN[1]       
 RMCT .DEGC            : Temp. of Mud Cake                | RUN[1]       
 TMAX .DEGC            : Max. Recorded Temp.              | RUN[1]       
 TIMC .                : Date/Time Circulation Stopped    | RUN[1]       
 TIML .                : Date/Time Logger Tagged Bottom   | RUN[1]       
 UNIT .                : Logging Unit Number              | RUN[1]       
 BASE .                : Home Base of Logging Unit        | RUN[1]       
 ENG  .                : Recording Engineer               | RUN[1]       
 WIT  .                : Witnessed By                     | RUN[1]       

#Run 2 Parameters
 RUN_DEPTH.M    1500,2513  : Run 2 Depth Interval  {F}    | Run[2]         
 RUN_DATE.     23/10/1998  : Run 2 date  {DD/MM/YYYY}     | Run[2]
 DREF .                : Depth Reference (KB,DF,CB)       | RUN[2]       
 EREF .M               : Elevation of Depth Reference     | RUN[2]       
 TDL  .M               : Total Depth Logger               | RUN[2]       
 TDD  .M               : Total Depth Driller              | RUN[2]       
 CSGL .M               : Casing Bottom Logger             | RUN[2]       
 CSGD .M               : Casing Bottom Driller            | RUN[2]       
 CSGS .MM              : Casing Size                      | RUN[2]       
 CSGW .KG/M            : Casing Weight                    | RUN[2]       
 BS   .MM              : Bit Size                         | RUN[2]       
 MUD  .                : Mud type                         | RUN[2]       
 MUDS .                : Mud Source                       | RUN[2]       
 MUDD .KG/M3           : Mud Density                      | RUN[2]       
 MUDV .S               : Mud Viscosity (Funnel)           | RUN[2]       
 FL   .CC              : Fluid Loss                       | RUN[2]       
 PH   .                : PH                               | RUN[2]       
 RM   .OHMM            : Resistivity of Mud               | RUN[2]       
 RMT  .DEGC            : Temperature of Mud               | RUN[2]       
 RMF  .OHMM            : Rest. of Mud Filtrate            | RUN[2]       
 RMFT .DEGC            : Temp. of Mud Filtrate            | RUN[2]       
 RMC  .OHMM            : Rest. of Mud Cake                | RUN[2]       
 RMCT .DEGC            : Temp. of Mud Cake                | RUN[2]       
 TMAX .DEGC            : Max. Recorded Temp.              | RUN[2]       
 TIMC .                : Date/Time Circulation Stopped    | RUN[2]       
 TIML .                : Date/Time Logger Tagged Bottom   | RUN[2]       
 UNIT .                : Logging Unit Number              | RUN[2]       
 BASE .                : Home Base of Logging Unit        | RUN[2]       
 ENG  .                : Recording Engineer               | RUN[2]       
 WIT  .                : Witnessed By                     | RUN[2]       
