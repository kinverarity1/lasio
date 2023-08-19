~Version Information
VERS.       3.0     :LAS - FPWD LAS output with realtime data
WRAP.        NO     :One line per step
DLM.      COMMA     :Delimiting character
# 
~Well Information Block
#MNEM.UNIT            Data type: Information 
# __________________________________________
STRT.FT                23849.88 : START INDEX 
STOP.FT                23849.88 : STOP INDEX  
STEP.                      0.00 : STEP        
NULL.                   -999.25 : NULL        
COMP.                DUMMY COMP : Company name 
WELL.                DUMMY WELL : Well name
FLD.                DUMMY FIELD : Field
CNTY.              DUMMY COUNTY : County or Rig 
STAT.               DUMMY STATE : State 
LOC1. X: -0000000.00 ft, Y: 000 : Location 
API.               999999999999 : Api number 
LATI.                00.00000 N : Latitude 
LONG.                00.00000 W : Longitude 
GDAT.            Mean Sea Level : Datum 
DPRF.FT                23849.88 : Depth Reference 
DATE.                 01-Jan-01 : Current Date  
SRVC.                DUMMY COMP : Service company 

~Parameter 
# 
#Required Parameters 
# init parameter list
# 

RUN.                    4.00  :Run {F}
TEST.                  11.00  :Test {F}
MD.FT                23871.96  :Planned Probe Depth {F}
TVD.FT               22683.22  :Planned Probe TVD {F}
FLOWTST.GPM           900.00  :Flow test {F}
FLOWDRL.GPM           900.00  :Flow during drilling {F}
DHTEMP.DEGF           178.00  :Down hole temperature {F}
ORIENT.DEG             90.00  :Probe Offset Angle {F}
MEMORY.%               82.00  :Memory {F}
RMDRLOF.FT             -6.00  :Ream Drill offset {F}
RMSLKOF.FT              0.00  :Ream Slack offset {F}
BITDIA.IN              10.63  :Bit Diameter {F}
MUDWT.LB/G             13.50  :Mud weight {F}
MUDTYPE.                SOBM  :Mud type  {S}
MUDNAME.            Rheliant  :Mud name  {S}
RM.OHMM              1000.00  :Resistivity of the mud {F}
RMF.OHMM             1000.00  :Resistivity of the mud formation {F}
RMC.OHMM             1000.00  :Resistivity of the mud cake {F}
CL.PPM               27000.00  :Clorine {F}
K.PPM                   0.00  :Potassium {F}
HPHT.C3/30M             1.60  :HPHT {F}
SAND%.%                 0.00  :Percent sand {F}
HG_SOL.%               17.90  :HG Sol {F}
LG_SOL.%                8.10  :LG_Sol {F}
GAUGE.                  ACQG  :FPWD Primary Gauge Type {S}
FPWD_OD.IN              8.00  :FPWD Outside Diameter {F}


~Phase_A_Definition 
BAT_COND.                 : Battery Status of depassivation {F}
AORIENT.DEG               : Orientation of the Probe {F}
ALONG_DL.                 : Tool status - Downlink feedback {F}
ASTATE.                   : Tool entered Standby via Manual/Automatic mode {F}

~Phase_A_data | Phase_A_Definition
    0.00,   144.00,   104.00,     2.00 
    0.00,   144.00,   104.00,     2.00 
    0.00,   144.00,   104.00,     2.00 
    0.00,   144.00,   104.00,     2.00 
    0.00,   144.00,   104.00,     2.00 
    0.00,   144.00,   104.00,     2.00 
    0.00,    12.00,   110.00,     2.00 
    0.00,  -909.25,  -999.25,  -999.25 

~Phase_A_Parameter
PHASE.    A     : Phase    {S} 


~Phase_B_Definition 
BDIS.                     : Allows the decoder to understand the different functionality of Phase B array {F}
BDIS_TIM.S                : Stores the time of the discriminator decision {F}
BP_DELTA.PSI              : Absolute pressure {F}
BT_DELTA.S                : Time of absolute pressure {F}

~Phase_B_data | Phase_B_Definition
    5.00,     0.00,     3.99,     0.00 
    6.00,     1.00, 16472.99,     1.00 
    0.00,    24.00, 16459.99,    24.00 
    5.00,    94.00, 16551.99,    94.00 
    5.00,   121.00, 16054.99,   121.00 
    1.00,   139.00, 14707.99,   139.00 
    5.00,   168.00, 15440.99,   168.00 
    2.00,   170.00, 15444.99,   170.00 
    6.00,   171.00, 16457.99,   171.00 
    3.00,   178.00, 13770.99,   178.00 
    5.00,   279.00, 15448.99,   279.00 
    5.00,   318.00, 15451.99,   318.00 
    5.00,   344.00, 15440.99,   344.00 
    5.00,   371.00, 15444.99,   371.00 
    5.00,   392.00, 15440.99,   392.00 
    6.00,   393.00, 16424.99,   393.00 
    4.00,   411.00, 15444.99,   411.00 

~Phase_B_Parameter
PHASE.    B     : Phase    {S} 
BP_HY_B4.PSI          16459.99   : Pressure Hydrostatic before {F}
BT_HY_B4.S              24.00   : Time Hydrostatic before {F}
BP_IV_DR.PSI          14707.99   : Pressure investigation drawdown {F}
BT_IV_DR.S             139.00   : Time of pressure investigation drawdown {F}
BP_IV_BU.PSI          15444.99   : Pressure investigation buildup {F}
BT_IV_BU.S             170.00   : Time of pressure investigation buildup {F}
BP_FN_DR.PSI          13770.99   : Pressure final drawdown {F}
BT_FN_DR.S             178.00   : Time of pressure of final drawdown {F}
BP_FN_BU.PSI          15444.99   : Pressure final buildup {F}
BT_FN_BU.S             411.00   : Time of pressure of final buildup {F}
BP_CORR.PSI              3.99   : Pressure Correction  {F}
B_STATE.                98.00   : State machine description {F}
B_RETRACT.               0.00   : Retract status  {F}

~Phase_C_Parameter
PHASE.    C     : Phase    {S} 
TIME.HH:MM:SS        18:39:08   : time  {S}
DATE.DATE           28-Aug-09   : Date {S}
DEPTH.FT              23849.88   : Actual probe depth {F}
TVD.FT                22663.98   : Actual probe Tvd {F}
STATUS1.            Retracted   : Retract/Deploy status flag1 {S}
STATUS1T.             2534.00   : Time for surface recognition of status1 {F}
RUN.                     4.00   : The run number {F}
TEST.                   11.00   : The test number {F}
CP_FN_BU.PSI          15445.29   : Pressure Final Buildup {F}
Q_60s.PSI/MIN          -14.48   : Quality 60 second slope {F}
Q_TEST.                 84.00   : Quality indicator for the overall test {F}
Q_PRSVAR.PSI             6.93   : Quality pressure variance {F}
BAT_COND.                0.00   : Battery Condition available for test with no flow {F}
STATUS2.            Retracted   : Retract/Deploy status flag2 {S}
STATUS2T.S            2594.00   : Time for surface recognition of status2 {F}
CP_IV_BU.PSI          15445.09   : Pressure investigation buildup {F}
CP_HY_B4.PSI          16460.29   : Hydrostatic pressure before testing formation {F}
CP_FN_DR.PSI          13771.29   : Pressure for the final drawdown {F}
CP_IV_DR.PSI          14708.09   : Pressure for the investigation Drawdown {F}
STATUS3.            Retracted   : Retract/Deploy status flag3 {S}
STATUS3T.             2647.00   : Time for surface recognition of status3 {F}
CT_IV_BU.S             169.00   : Time identified for the investigation buildup {F}
CT_FN_DR.S             177.00   : Time identified for the final drawdown {F}
CT_FN_BU.S             411.00   : Time identified for the final buildup {F}
CT_IV_DR.S             139.20   : Time identified for the investigation drawdown {F}
CT_EXPON.S               4.47   : Time step of pressure deltas {F}
STATUS4.            Retracted   : Retract/Deploy status flag4 {S}
STATUS4T.S            2707.00   : Time for surface recognition of status4 {F}
CP_DELTA1.PSI         14338.29   : 1st delta pressure: referenced to Final or Inv Drawdown {F}
CP_DELTA2.PSI         15217.29   : 2nd delta pressure: referenced to Final or Inv Drawdown {F}
CP_DELTA3.PSI         15430.29   : 3rd delta pressure: referenced to Final or Inv Drawdown {F}
CP_DELTA4.PSI         15435.29   : 4th delta pressure: referenced to Final or Inv Drawdown {F}
CP_DELTA5.PSI         15439.29   : 5th delta pressure: referenced to Final or Inv Drawdown {F}
CT_DELTA1.S            177.50   : Time for 1st delta pressure {F}
CT_DELTA2.S            179.24   : Time for 2nd delta pressure {F}
CT_DELTA3.S            186.99   : Time for 3rd delta pressure {F}
CT_DELTA4.S            221.66   : Time for 4th delta pressure {F}
CT_DELTA5.S            376.62   : Time for 5th delta pressure {F}
C_MOB_FN.MD/CP           2.83   : Mobility calculated from final buildup {F}
PRETEST.                14.00   : The type of pretest performed {F}
STATUS5.            Retracted   : Retract/Deploy status flag {S}
STATUS5T.S            2758.00   : Time for surface recognition of status5 {F}

# 
#Required Parameters 
# Edit parameter list
# 

RUN.                    4.00  :The run number {F} 
TEST.                  11.00  :The test number {F} 
MD.FT                23871.96  :Actual Probe Depth {F} 
TVD.FT               22683.22  :Actual Probe TVD {F} 
CP_IV_BU.PSI         15445.10  :Pressure investigation buildup {F} 
CP_FN_BU.PSI         15445.30  :Pressure Final Buildup {F} 
EQMUDWT.LB/G           13.09  :Equivalent Mud Weight {F} 
D_MOB_IV.MD/CP       -999.25  :Mobility calculated from investigation buildup phase {F} 
C_MOB_FN.MD/CP          2.80  :Mobility calculated from final buildup {F} 
CP_HY_B4.PSI         16460.30  :Hydrostatic pressure before testing formation {F} 
DP_HY_AF.PSI         -999.25  :Hydrostatic pressure after the test {F} 
CALIPER.IN           -999.25  :Hole size = bit size + caliper {F} 
AORIENT.DEG            90.00  :Orientation of the Probe {F} 
PRETEST.                6.00  :The type of pretest performed {F} 
Q_PRSVAR.PSI            6.93  :Quality pressure variance {F} 
Q_60s.PSI/MIN         -14.48  :Quality 60 second slope {F} 
Q_TEST.                84.00  :Quality indicator for the overall test {F} 
Q_NOISE.             -999.25  :Quality noise indicator {F} 
Q_INVEST.            -999.25  :Quality indicator for investigation phase {F} 
Q_FINAL.             -999.25  :Quality indicator for final phase {F} 
FLO_FIN.C3/S         -999.25  :Final drawdown flow rate {F} 
FLO_INV.C3/S            0.00  :Investigation drawdown flow rate {F} 
HOLESIZE.IN          -999.25  :HoleSize = (Caliper + BitSize) {F} 
