~VERSION INFORMATION 
VERS.                       3.0            :LAS - Fpwd las output with realtime data
WRAP.                        NO            :One line per step
DLM.                      COMMA            :Delimiting character
#
~Well Information Block 
#MNEM.UNIT            Data type            :Information
#______________________________________________________
STRT.ft                14757.03            :START INDEX
STOP.ft                14757.03            :STOP INDEX
STEP.                    0.0625            :STEP
NULL.                   -999.25            :NULL
COMP.                DUMMY COMP            :Company Name
WELL.                DUMMY WELL            :Well Name
FLD.                DUMMY FIELD            :Field
CNTY.                                      :County or Rig
STAT.               DUMMY STATE            :STATE
LOC.             DUMMY LOC                 :Location
API.             999999999999              :Api number
LATI.            00° 0' 00.00" N          :Well Latitude
LONG.            00° 00' 00.0" W           :Longitude
GDAT.                       MSL            :Datum
DPRF.ft                14757.03            :Depth Reference
DATE.                 01-Jan-01            :Current Date
SRVC.                DUMMY CORP            :Service Company
EDF.ft                   202.99            :Elevation of Derrick Floor


~Parameter 
RUN.                          5            :Run {F}
TEST.                         2            :Test {F}
MD.FT                  14757.03            :Measured Depth {F}
TVD.FT                 14441.34            :Tvd of the test {F}
BHT.DEGF                    212            :Bottom Hole Temperature {F}
PROBE_TFO.DEG            174.11            :Probe Angle Offset {F}
BS.IN                     10.25            :Bit Size {F}
DFT_CATEGORY.               Oil            :Drilling Fluid Type {S}
DFT.              Synthetic Oil            :Drilling Fluid Oil Type {S}
RMS.OHMM                    500            :Resistivity of Mud Sample {F}
RMCS.OHMM                                  :Resistivity of Mud Cake Sample {F}
BSAL.PPM                      0            :Borehole Salinity {F}
BHK.%                         0            :Drilling Fluid Potassium Concentration {F}
DHGS.%                                     :Drilling Fluid High Gravity Solids {F}
FPWD_OD.IN                 8.25            :FPWD Outside Diameter {F}
QUARTZGAUGE.         Quartzdyne            :Primary Gauge Type {S}
STRAINGAUGE.              Paine            :Strain Gauge Type {S}



~Phase_A_Definition 
BAT_DEP_STATE.                             :Battery Condition with Depassivation {F}
AORIENT.deg                                :Phase A Probe Orientation {F}
ALONG_DL.                                  :Phase A Long Downlink feedback {F}
ASTATE.                                    :Phase A Tool State feedback {F}

~Phase_A_data | Phase_A_Definition 
     0.00,   120.11,   110.00,     2.00
     0.00,   120.11,   110.00,     2.00
     0.00,   120.11,   110.00,     2.00
     0.00,   120.11,   110.00,     2.00
     0.00,   120.11,   110.00,     2.00
     0.00,   120.11,   110.00,     2.00

~Phase_A_Parameter 
PHASE.    A     : Phase    {S}

~Phase_B_Definition 
BDIS.                                      :Phase B Discriminator Position {F}
BDIS_TIM.s                                 :Phase B Delta Pressure Time Stamp {F}
BP_DELTA.psi                               :Phase B Delta Pressure Measurement {F}
BT_DELTA.s                                 :Phase B Delta Pressure Time Stamp {F}

~Phase_B_data | Phase_B_Definition 
     5.00,     0.00,     2.76,     0.00
     5.00,     0.00,     2.76,     0.00
     6.00,     1.00,  7667.77,     1.00
     0.00,    28.00,  7669.76,    28.00
     5.00,    63.00,  7669.76,    63.00
     5.00,    84.00,  7688.76,    84.00
     5.00,    95.00,  7686.76,    95.00
     5.00,   108.00,  7686.76,   108.00
     5.00,   121.00,  6423.77,   121.00
     6.00,   122.00,  7667.77,   122.00
     1.00,   140.00,  5619.76,   140.00
     2.00,   160.00,  5715.76,   160.00
     3.00,   168.00,  5612.76,   168.00
     5.00,   199.00,  5714.77,   199.00
     5.00,   210.00,  5716.76,   210.00
     5.00,   223.00,  5715.76,   223.00
     6.00,   224.00,  7668.76,   224.00
     2.00,   226.00,  5715.76,   226.00
     3.00,   230.00,  5619.76,   230.00
     5.00,   280.00,  5716.76,   280.00
     5.00,   293.00,  5714.77,   293.00
     5.00,   314.00,  5714.77,   314.00
     5.00,   325.00,  5716.76,   325.00
     6.00,   326.00,  7665.76,   326.00
     5.00,   351.00,  5715.76,   351.00
     5.00,   372.00,  5714.77,   372.00
     5.00,   382.00,  5714.77,   382.00
     5.00,   395.00,  5714.77,   395.00
     5.00,   408.00,  5715.76,   408.00
     4.00,   411.00,  5715.76,   411.00
     6.00,   412.00,  7657.76,   412.00
     5.00,   453.00,  7665.76,   453.00
     5.00,   466.00,  7660.76,   466.00

~Phase_B_Parameter 
PHASE.    B     : Phase    {S}
BP_HY_B4.psi          7669.76:  Phase B Hydrostatic Pressure before test {F}
BT_HY_B4.s            28.00:  Phase B Hydrostatic Pressure before test Time Stamp {F}
BP_IV_DR.psi          5619.76:  Phase B Investigation Drawdown Pressure {F}
BT_IV_DR.s           140.00:  Phase B Investigation Drawdown Pressure Time Stamp {F}
BP_IV_BU.psi          5715.76:  Phase B Investigation Buildup Pressure {F}
BT_IV_BU.s           226.00:  Phase B Investigation Buildup Pressure Time Stamp {F}
BP_FN_DR.psi          5619.76:  Phase B Final Drawdown Pressure {F}
BT_FN_DR.s           230.00:  Phase B Final Drawdown Pressure Time Stamp {F}
BP_FN_BU.psi          5715.76:  Phase B Final Buildup Pressure {F}
BT_FN_BU.s           411.00:  Phase B Final Buildup Pressure Time Stamp {F}
BP_CORR.psi             2.76:  Phase B Hydraulic Head Correction {F}
B_STATE.          -999.25:  Phase B State Machine Description {F}
B_RETRACT.          -999.25:  Phase B Deployed/Retract Status {F}

~Phase_C_Parameter 
PHASE.    C     : Phase    {S}
TIME.HH.MM.SS         23:28:54:  Test time {S}
DATE.DATE        13-Aug-17:  Test date {S}
DEPTH.ft         14757.03: Depth Index {F}
TVD.ft         14441.34:  True Vertical Depth {F}
STATUS1.        Retracted:  Status Flag One {F}
STATUS1T.s           561.74:  Status Flag One Time Stamp {F}
CP_FN_BU.psi          5716.06:  Phase C Final Buildup Pressure {F}
Q_60S.psi/min             0.08:  Quality 60s slope {F}
Q_TEST.           124.00:  Quality of Test indicator {F}
Q_PRSVAR.psi             1.19:  Quality Pressure Variance {F}
BAT_DEP_STATE.             0.00:  Battery Condition with Depassivation {F}
STATUS2.        Retracted:  Status Flag Two {F}
STATUS2T.s           589.54:  Status Flag Two Time Stamp {F}
CP_IV_BU.psi          5716.06:  Phase C Investigation Buildup Pressure {F}
CP_HY_B4.psi          7670.06:  Phase C Hydrostatic Pressure before Test {F}
CP_FN_DR.psi          5620.07:  Phase C Final Drawdown Pressure {F}
CP_IV_DR.psi          5613.06:  Phase C Investigation Drawdown Pressure {F}
STATUS3.        Retracted:  Status Flag Three {F}
STATUS3T.s           622.84:  Status Flag Three Time Stamp {F}
CT_IV_BU.s           225.00:  Phase C Investigation Buildup Pressure Time Stamp {F}
CT_FN_DR.s           228.50:  Phase C Final Drawdown Pressure Time Stamp {F}
CT_FN_BU.s           411.00:  Phase C Final Buildup Pressure Time Stamp {F}
CT_IV_DR.s           168.00:  Phase C Investigation Drawdown Pressure Time Stamp {F}
CT_EXPON.             4.20:  Phase C Time Exponent for Deltas {F}
STATUS4.        Retracted:  Status Flag Four {F}
STATUS4T.s           643.74:  Status Flag Four Time Stamp {F}
CP_DELTA1.psi          5708.06:  Phase C Delta Pressure First Position {F}
CP_DELTA2.psi          5713.06:  Phase C Delta Pressure Second Position {F}
CP_DELTA3.psi          5715.06:  Phase C Delta Pressure Third Position {F}
CP_DELTA4.psi          5716.06:  Phase C Delta Pressure Fourth Position {F}
CP_DELTA5.psi          5716.06:  Phase C Delta Pressure Fifth Position {F}
CT_DELTA1.s           229.00:  Phase C Delta Pressure Time Stamp First Position {F}
CT_DELTA2.s           230.60:  Phase C Delta Pressure Time Stamp Second Position {F}
CT_DELTA3.s           237.32:  Phase C Delta Pressure Time Stamp Third Position {F}
CT_DELTA4.s           265.54:  Phase C Delta Pressure Time Stamp Fourth Position {F}
CT_DELTA5.s           384.08:  Phase C Delta Pressure Time Stamp Fifth Position {F}
C_MOB_FN.mD/cP           100.23:  Phase C Final Mobility {F}
PRETEST.            14.00:  PreTest Code {F}
STATUS5.        Retracted:  Status Flag Five {F}
STATUS5T.s           679.17:  Status Flag Five Time Stamp {F}
FP_EQMW.g/cm3             0.91:  Formation Pressure Equivalent Mud Weight {F}
AORIENT.deg           120.11:  Phase A Probe Orientation {F}
