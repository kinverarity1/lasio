~VERSION INFORMATION 
VERS.                       3.0            :LAS - Fpwd las output with realtime data
WRAP.                        NO            :One line per step
DLM.                      COMMA            :Delimiting character
#
~Well Information Block 
#MNEM.UNIT            Data type            :Information
#______________________________________________________
STRT.ft                20299.05            :START INDEX
STOP.ft                20299.05            :STOP INDEX
STEP.                    0.0625            :STEP
NULL.                   -999.25            :NULL
COMP.            DUMMY COMP                       :Company Name
WELL.            DUMMY WELL                :Well Name
FLD.             DUMMY FIELD               :Field
CNTY.                                      :County or Rig
STAT.                 DUMMY STATE          :STATE
LOC.             DUMMY LOC                        :Location
API.               999999999999            :Api number
LATI.            00.000000 degrees         :Well Latitude
LONG.            -00.000000 degrees        :Longitude
GDAT.                       MSL            :Datum
DPRF.ft                20299.05            :Depth Reference
DATE.                 01-Jan-01            :Current Date
SRVC.              DUMMY CORP              :Service Company
EDF.ft                    83.99            :Elevation of Derrick Floor


~Parameter 
RUN.                          9            :Run {F}
TEST.                         5            :Test {F}
MD.FT                  20299.05            :Measured Depth {F}
TVD.FT                 19745.64            :Tvd of the test {F}
BHT.DEGF                   98.6            :Bottom Hole Temperature {F}
PROBE_TFO.DEG               151            :Probe Angle Offset {F}
BS.IN                       8.5            :Bit Size {F}
DFT.              Synthetic Oil            :Drilling Fluid Oil Type {S}
RMS.OHMM                    500            :Resistivity of Mud Sample {F}
RMCS.OHMM                  1000            :Resistivity of Mud Cake Sample {F}
BSAL.PPM                  77452            :Borehole Salinity {F}
BHK.%                         0            :Drilling Fluid Potassium Concentration {F}
DHGS.%                                     :Drilling Fluid High Gravity Solids {F}
FPWD_OD.IN                 6.75            :FPWD_OD Outside Diameter {F}
QUARTZGAUGE.               ACQG            :Primary Gauge Type {S}
STRAINGAUGE.              Paine            :Strain Gauge Type {S}



~Phase_A_Definition 
BAT_DEP_STATE.                             :Battery Condition with Depassivation {F}
AORIENT.deg                                :Phase A Probe Orientation {F}
ALONG_DL.                                  :Phase A Long Downlink feedback {F}
ASTATE.                                    :Phase A Tool State feedback {F}

~Phase_A_data | Phase_A_Definition 
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00
     2.00,    94.75,   110.00,     2.00

~Phase_A_Parameter 
PHASE.    A     : Phase    {S}

~Phase_B_Definition 
BDIS.                                      :Phase B Discriminator Position {F}
BDIS_TIM.s                                 :Phase B Delta Pressure Time Stamp {F}
BP_DELTA.psi                               :Phase B Delta Pressure Measurement {F}
BT_DELTA.s                                 :Phase B Delta Pressure Time Stamp {F}

~Phase_B_data | Phase_B_Definition 
     5.00,     0.00,     4.36,     0.00
     5.00,     0.00,     4.36,     0.00
     6.00,     1.00, 13710.36,     1.00
     0.00,    24.00, 13738.36,    24.00
     5.00,    63.00, 13722.36,    63.00
     5.00,    84.00, 13749.36,    84.00
     5.00,    95.00, 13750.36,    95.00
     5.00,   108.00, 13743.36,   108.00
     5.00,   121.00, 13315.36,   121.00
     6.00,   122.00, 13735.36,   122.00
     5.00,   152.00,  9539.36,   152.00
     5.00,   165.00,  8894.36,   165.00
     5.00,   178.00,  8894.36,   178.00
     1.00,   167.00,  8893.36,   167.00
     2.00,   188.00,  8894.36,   188.00
     5.00,   224.00,  8894.36,   224.00
     6.00,   225.00, 13725.36,   225.00
     5.00,   257.00,  8894.36,   257.00
     5.00,   267.00,  8894.36,   267.00
     5.00,   280.00,  8894.36,   280.00
     5.00,   293.00,  8894.36,   293.00
     2.00,   305.00,  8894.36,   305.00
     3.00,   202.00,  8890.36,   202.00
     6.00,   306.00, 13738.36,   306.00
     5.00,   351.00,  8894.36,   351.00
     5.00,   372.00,  8894.36,   372.00
     5.00,   382.00,  8894.36,   382.00
     5.00,   395.00,  8894.36,   395.00
     3.00,   312.00,  8889.36,   312.00
     4.00,   408.00,  8894.36,   408.00
     6.00,   409.00, 13756.36,   409.00
     5.00,   453.00, 13752.36,   453.00
     5.00,   467.00, 13746.36,   467.00

~Phase_B_Parameter 
PHASE.    B     : Phase    {S}
BP_HY_B4.psi         13738.36:  Phase B Hydrostatic Pressure before test {F}
BT_HY_B4.s            24.00:  Phase B Hydrostatic Pressure before test Time Stamp {F}
BP_IV_DR.psi          8893.36:  Phase B Investigation Drawdown Pressure {F}
BT_IV_DR.s           167.00:  Phase B Investigation Drawdown Pressure Time Stamp {F}
BP_IV_BU.psi          8894.36:  Phase B Investigation Buildup Pressure {F}
BT_IV_BU.s           305.00:  Phase B Investigation Buildup Pressure Time Stamp {F}
BP_FN_DR.psi          8889.36:  Phase B Final Drawdown Pressure {F}
BT_FN_DR.s           312.00:  Phase B Final Drawdown Pressure Time Stamp {F}
BP_FN_BU.psi          8894.36:  Phase B Final Buildup Pressure {F}
BT_FN_BU.s           408.00:  Phase B Final Buildup Pressure Time Stamp {F}
BP_CORR.psi             4.36:  Phase B Hydraulic Head Correction {F}
B_STATE.          -999.25:  Phase B State Machine Description {F}
B_RETRACT.          -999.25:  Phase B Deployed/Retract Status {F}

~Phase_C_Parameter 
PHASE.    C     : Phase    {S}
TIME.HH.MM.SS         11:30:36:  Test time {S}
DATE.DATE        18-Jul-15:  Test date {S}
DEPTH.ft         20299.05: Depth Index {F}
TVD.ft         19745.64:  True Vertical Depth {F}
STATUS1.        Retracted:  Status Flag One {F}
STATUS1T.s           672.46:  Status Flag One Time Stamp {F}
CP_FN_BU.psi          8894.86:  Phase C Final Buildup Pressure {F}
Q_60S.psi/min            -0.06:  Quality 60s slope {F}
Q_TEST.            88.00:  Quality of Test indicator {F}
Q_PRSVAR.psi             0.14:  Quality Pressure Variance {F}
BAT_DEP_STATE.             2.00:  Battery Condition with Depassivation {F}
STATUS2.        Retracted:  Status Flag Two {F}
STATUS2T.s           700.25:  Status Flag Two Time Stamp {F}
CP_IV_BU.psi          8894.76:  Phase C Investigation Buildup Pressure {F}
CP_HY_B4.psi         13737.86:  Phase C Hydrostatic Pressure before Test {F}
CP_FN_DR.psi          8889.86:  Phase C Final Drawdown Pressure {F}
CP_IV_DR.psi          8891.76:  Phase C Investigation Drawdown Pressure {F}
STATUS3.        Retracted:  Status Flag Three {F}
STATUS3T.s           733.54:  Status Flag Three Time Stamp {F}
CT_IV_BU.s           305.00:  Phase C Investigation Buildup Pressure Time Stamp {F}
CT_FN_DR.s           311.50:  Phase C Final Drawdown Pressure Time Stamp {F}
CT_FN_BU.s           407.00:  Phase C Final Buildup Pressure Time Stamp {F}
CT_IV_DR.s           202.00:  Phase C Investigation Drawdown Pressure Time Stamp {F}
CT_EXPON.             3.57:  Phase C Time Exponent for Deltas {F}
STATUS4.        Retracted:  Status Flag Four {F}
STATUS4T.s           754.43:  Status Flag Four Time Stamp {F}
CP_DELTA1.psi          8894.86:  Phase C Delta Pressure First Position {F}
CP_DELTA2.psi          8894.86:  Phase C Delta Pressure Second Position {F}
CP_DELTA3.psi          8894.86:  Phase C Delta Pressure Third Position {F}
CP_DELTA4.psi          8894.86:  Phase C Delta Pressure Fourth Position {F}
CP_DELTA5.psi          8894.86:  Phase C Delta Pressure Fifth Position {F}
CT_DELTA1.s           312.00:  Phase C Delta Pressure Time Stamp First Position {F}
CT_DELTA2.s           313.29:  Phase C Delta Pressure Time Stamp Second Position {F}
CT_DELTA3.s           317.87:  Phase C Delta Pressure Time Stamp Third Position {F}
CT_DELTA4.s           334.25:  Phase C Delta Pressure Time Stamp Fourth Position {F}
CT_DELTA5.s           392.72:  Phase C Delta Pressure Time Stamp Fifth Position {F}
C_MOB_FN.mD/cP           812.96:  Phase C Final Mobility {F}
PRETEST.            14.00:  PreTest Code {F}
STATUS5.        Retracted:  Status Flag Five {F}
STATUS5T.s           789.87:  Status Flag Five Time Stamp {F}
FP_EQMW.g/cm3             1.04:  Formation Pressure Equivalent Mud Weight {F}
AORIENT.deg            94.75:  Phase A Probe Orientation {F}
