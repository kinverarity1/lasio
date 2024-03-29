~VERSION INFORMATION
 VERS.                  1.2:   CWLS LOG ASCII STANDARD -VERSION 1.2
 WRAP.                  NO:   ONE LINE PER DEPTH STEP
~WELL INFORMATION BLOCK
#MNEM.UNIT       DATA TYPE    INFORMATION
#---------    -------------   ------------------------------
 STRT.M        1670.000000:
 STOP.M        1669.750000:
 STEP.M            -0.1250:
 NULL.           -999.2500:
 COMP.             COMPANY:   # ANY OIL COMPANY LTD.
 WELL.                WELL:   ANY ET AL OIL WELL #12
 FLD .               FIELD:   EDAM
 LOC .            LOCATION:   A9-16-49-20W3M
 PROV.            PROVINCE:   SASKATCHEWAN
 SRVC.     SERVICE COMPANY:   ANY LOGGING COMPANY LTD.
 DATE.            LOG DATE:   25-DEC-1988
 UWI .      UNIQUE WELL ID:   100091604920W300
~CURVE INFORMATION
#MNEM.UNIT      API CODE      CURVE DESCRIPTION
#---------    -------------   ------------------------------
 DEPT.M                      :  1  DEPTH
 RHO .ohmm     		     :  curve 1,2,3
 RHO .ohmm               :  curve 10,20,30
 RHO .ohmm               :  curve 100,200,300
 PHI .                   : porosity
~PARAMETER INFORMATION
#MNEM.UNIT        VALUE       DESCRIPTION
#---------    -------------   ------------------------------
 BHT .DEGC         35.5000:   BOTTOM HOLE TEMPERATURE
 BS  .MM          200.0000:   BIT SIZE
 FD  .K/M3       1000.0000:   FLUID DENSITY
 MATR.              0.0000:   NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)
 MDEN.           2710.0000:   LOGGING MATRIX DENSITY
 RMF .OHMM          0.2160:   MUD FILTRATE RESISTIVITY
 DFD .K/M3       1525.0000:   DRILL FLUID DENSITY
~Other
     Note: The logging tools became stuck at 625 meters causing the data
	   between 625 meters and 615 meters to be invalid.
~A  DEPTH     
1670.000   1 10 100 0.1
1669.875   2 20 200 0.2
1669.750   3 30 300 0.3
