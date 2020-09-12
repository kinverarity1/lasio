~Version Information
 VERS.  3.0   : CWLS LOG ASCII STANDARD
 WRAP.  NO    : One line per depth step
 DLM .  SPACE : Delimiting character
~Well Information
#MNEM.UNIT               DATA               DESCRIPTION
#---- ----        -------------------      ----------------
 STRT .F                 1088.1737       : First Index Value
 STOP .F                 8211.6737       : Last Index Value
 STEP .F                    0.5000       : Step
 NULL .                  -999.2500       : Null Value
 COMP .                       : Company
 WELL .                  : Well
 FLD  .                      : Field
 LOC  .                           : Location
 SRVC .             : Service company
 DATE .                        : Service Date {DD/MM/YYYY}
 CTRY .                               : Country
 STAT .                      : State
 CNTY .                         : County
 API  .                 : API Number
 LATI .                                  : Latitude
 LONG .                                  : Longitude
 GDAT .                                  : Geodetic Datum
~Curve
#MNEM  .UNIT            LOG CODES          CURVE DESCRIPTION
#----   ----        -------------------    -----------------
 DEPT  .F                                : Depth {F}
 TENS  .LBF                              : Tension {F}
 COLLAR.                                 : CCL {F}
 GAMMA .                                 : GR {F}
 3'AMP .MV                               : 3 Foot Amplitude {F}
 3'TRA .µS                               : 3 Foot Floating Gate Transit Time {F}
~   DEPTH     TENSION        CCL       GR        3' AMP      TT
  1088.1737   339.4208     9.0000    35.2786     0.8635   776.7905
  1088.6737   339.4208     9.0000    35.2786     0.8635   776.7905