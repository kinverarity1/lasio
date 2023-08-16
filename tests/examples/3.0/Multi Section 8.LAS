~VERSION INFORMATION 
VERS.                       3.0            :LAS - Fpwd las output with realtime data
WRAP.                        NO            :One line per step
DLM.                      COMMA            :Delimiting character
#
~Well Information Block 
#MNEM.UNIT            Data type            :Information
#______________________________________________________
STRT.ft                22538.11            :START INDEX
STOP.ft                22538.11            :STOP INDEX
STEP.                    0.0625            :STEP
NULL.                   -999.25            :NULL
COMP.            DUMMY COMP                     :Company Name
WELL.            DUMMY WELL                :Well Name
FLD.             DUMMY FIELD               :Field
CNTY.                                      :County or Rig
STAT.                 DUMMY STATE          :STATE
LOC.             DUMMY LOC                  :Location
API.                                       :Api number
LATI.            00° 0' 10.000" N          :Well Latitude
LONG.            00° 00' 00.000" W         :Longitude
GDAT.                       MSL            :Datum
DPRF.ft                22538.11            :Depth Reference
DATE.                 01-Jan-01            :Current Date
SRVC.              DUMMY COMP              :Service Company
EDF.ft                    81.00            :Elevation of Derrick Floor


~Parameter 
RUN.                          4            :Run {F}
TEST.                        11            :Test {F}
MD.FT                  22538.11            :Measured Depth {F}
TVD.FT                 21391.68            :Tvd of the test {F}
BHT.DEGF                    212            :Bottom Hole Temperature {F}
PROBE_TFO.DEG             44.35            :Probe Angle Offset {F}
BS.IN                       8.5            :Bit Size {F}
DFT_CATEGORY.               Oil            :Drilling Fluid Type {S}
DFT.              Synthetic Oil            :Drilling Fluid Oil Type {S}
RMS.OHMM                    500            :Resistivity of Mud Sample {F}
RMCS.OHMM                                  :Resistivity of Mud Cake Sample {F}
BSAL.PPM                  54128            :Borehole Salinity {F}
BHK.%                         0            :Drilling Fluid Potassium Concentration {F}
DHGS.%                                     :Drilling Fluid High Gravity Solids {F}
FPWD_OD.IN                 6.75            :FPWD Outside Diameter {F}
QUARTZGAUGE.               ACQG            :Primary Gauge Type {S}
STRAINGAUGE.              Paine            :Strain Gauge Type {S}



~Phase_A_Definition 
BAT_DEP_STATE.                             :Battery Condition with Depassivation {F}
AORIENT.deg                                :Phase A Probe Orientation {F}
ALONG_DL.                                  :Phase A Long Downlink feedback {F}
ASTATE.                                    :Phase A Tool State feedback {F}

~Phase_A_data | Phase_A_Definition 
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00
     0.00,  -147.65,   109.00,     2.00

~Phase_A_Parameter 
PHASE.    A     : Phase    {S}

~Phase_B_Definition 
BDIS.                                      :Phase B Discriminator Position {F}
BDIS_TIM.s                                 :Phase B Delta Pressure Time Stamp {F}
BP_DELTA.psi                               :Phase B Delta Pressure Measurement {F}
BT_DELTA.s                                 :Phase B Delta Pressure Time Stamp {F}

~Phase_B_data | Phase_B_Definition 
     5.00,     0.00,     3.83,     0.00
     5.00,     0.00,     3.83,     0.00
     5.00,     0.00,     3.83,     0.00
     6.00,     1.00, 14367.00,     1.00
     0.00,    28.00, 14354.83,    28.00
     5.00,    71.00, 14225.82,    71.00
     5.00,    82.00, 14289.82,    82.00
     5.00,    95.00, 14284.83,    95.00
     5.00,   112.00, 12631.82,   112.00
     5.00,   124.00, 12604.83,   124.00
     6.00,   125.00, 14370.00,   125.00
     1.00,   124.00, 12598.83,   124.00
     5.00,   165.00, 12620.83,   165.00
     5.00,   178.00, 12623.83,   178.00
     5.00,   189.00, 12619.83,   189.00
     5.00,   202.00, 12625.83,   202.00
     5.00,   219.00, 12621.83,   219.00
     6.00,   220.00, 14362.00,   220.00
     5.00,   243.00, 12622.82,   243.00
     2.00,   245.00, 12622.82,   245.00
     3.00,   264.00, 12600.83,   264.00
     5.00,   285.00, 12619.83,   285.00
     5.00,   295.00, 12622.82,   295.00
     5.00,   308.00, 12620.83,   308.00
     6.00,   309.00, 14370.00,   309.00
     5.00,   338.00, 12618.82,   338.00
     5.00,   349.00, 12623.83,   349.00
     5.00,   362.00, 12620.83,   362.00
     5.00,   379.00, 12624.83,   379.00
     5.00,   392.00, 12620.83,   392.00
     5.00,   402.00, 12621.83,   402.00
     6.00,   403.00, 14344.00,   403.00
     4.00,   407.00, 12622.82,   407.00
     5.00,   445.00, 14349.83,   445.00

~Phase_B_Parameter 
PHASE.    B     : Phase    {S}
BP_HY_B4.psi         14354.83:  Phase B Hydrostatic Pressure before test {F}
BT_HY_B4.s            28.00:  Phase B Hydrostatic Pressure before test Time Stamp {F}
BP_IV_DR.psi         12598.83:  Phase B Investigation Drawdown Pressure {F}
BT_IV_DR.s           124.00:  Phase B Investigation Drawdown Pressure Time Stamp {F}
BP_IV_BU.psi         12622.82:  Phase B Investigation Buildup Pressure {F}
BT_IV_BU.s           245.00:  Phase B Investigation Buildup Pressure Time Stamp {F}
BP_FN_DR.psi         12600.83:  Phase B Final Drawdown Pressure {F}
BT_FN_DR.s           264.00:  Phase B Final Drawdown Pressure Time Stamp {F}
BP_FN_BU.psi         12622.82:  Phase B Final Buildup Pressure {F}
BT_FN_BU.s           407.00:  Phase B Final Buildup Pressure Time Stamp {F}
BP_CORR.psi             3.83:  Phase B Hydraulic Head Correction {F}
B_STATE.          -999.25:  Phase B State Machine Description {F}
B_RETRACT.          -999.25:  Phase B Deployed/Retract Status {F}

~Phase_C_Parameter 
PHASE.    C     : Phase    {S}
TIME.HH.MM.SS         15:41:03:  Test time {S}
DATE.DATE        19-Feb-22:  Test date {S}
DEPTH.ft         22538.11: Depth Index {F}
TVD.ft         21391.68:  True Vertical Depth {F}
STATUS1.        Retracted:  Status Flag One {F}
STATUS1T.s           543.43:  Status Flag One Time Stamp {F}
CP_FN_BU.psi         12623.12:  Phase C Final Buildup Pressure {F}
Q_60S.psi/min            -0.04:  Quality 60s slope {F}
Q_TEST.           104.00:  Quality of Test indicator {F}
Q_PRSVAR.psi             2.40:  Quality Pressure Variance {F}
BAT_DEP_STATE.             0.00:  Battery Condition with Depassivation {F}
STATUS2.        Retracted:  Status Flag Two {F}
STATUS2T.s           577.58:  Status Flag Two Time Stamp {F}
CP_IV_BU.psi         12623.12:  Phase C Investigation Buildup Pressure {F}
CP_HY_B4.psi         14355.12:  Phase C Hydrostatic Pressure before Test {F}
CP_FN_DR.psi         12601.12:  Phase C Final Drawdown Pressure {F}
CP_IV_DR.psi         12600.13:  Phase C Investigation Drawdown Pressure {F}
STATUS3.        Retracted:  Status Flag Three {F}
STATUS3T.s           600.59:  Status Flag Three Time Stamp {F}
CT_IV_BU.s           244.00:  Phase C Investigation Buildup Pressure Time Stamp {F}
CT_FN_DR.s           264.00:  Phase C Final Drawdown Pressure Time Stamp {F}
CT_FN_BU.s           406.00:  Phase C Final Buildup Pressure Time Stamp {F}
CT_IV_DR.s           124.40:  Phase C Investigation Drawdown Pressure Time Stamp {F}
CT_EXPON.             3.95:  Phase C Time Exponent for Deltas {F}
STATUS4.        Retracted:  Status Flag Four {F}
STATUS4T.s           627.85:  Status Flag Four Time Stamp {F}
CP_DELTA1.psi         12623.12:  Phase C Delta Pressure First Position {F}
CP_DELTA2.psi         12621.13:  Phase C Delta Pressure Second Position {F}
CP_DELTA3.psi         12623.12:  Phase C Delta Pressure Third Position {F}
CP_DELTA4.psi         12623.12:  Phase C Delta Pressure Fourth Position {F}
CP_DELTA5.psi         12620.12:  Phase C Delta Pressure Fifth Position {F}
CT_DELTA1.s           264.50:  Phase C Delta Pressure Time Stamp First Position {F}
CT_DELTA2.s           265.98:  Phase C Delta Pressure Time Stamp Second Position {F}
CT_DELTA3.s           271.80:  Phase C Delta Pressure Time Stamp Third Position {F}
CT_DELTA4.s           294.81:  Phase C Delta Pressure Time Stamp Fourth Position {F}
CT_DELTA5.s           385.72:  Phase C Delta Pressure Time Stamp Fifth Position {F}
C_MOB_FN.mD/cP            72.32:  Phase C Final Mobility {F}
PRETEST.             9.00:  PreTest Code {F}
STATUS5.        Retracted:  Status Flag Five {F}
STATUS5T.s           652.98:  Status Flag Five Time Stamp {F}
FP_EQMW.g/cm3             1.36:  Formation Pressure Equivalent Mud Weight {F}
AORIENT.deg          -147.65:  Phase A Probe Orientation {F}
