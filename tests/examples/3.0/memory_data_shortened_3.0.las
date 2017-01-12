~VERSION INFORMATION 
VERS  .    3.0                                     :CWLS Log ASCII Standard - VERSION 3.0
WRAP  .    NO                                      :One Line per Time step
DLM   .    SPACE                                   :Column Data section Delimiter
PROD  .    xxxProducer                             :LAS Producer
PROG  .    xxxProgram                              :LAS Program name and version
SOURCE.    xxxSource                               :Run&Pass Information
CREA  .    01/01/2016                              :LAS Creation date {MM/DD/YYYY}
#--------------------------------------------------
~WELL INFORMATION 
#MNEM           .UNIT                      DATA            :DESCRIPTION
#----            ------          --------------            -----------------------------
STRT            .d               42606.1666666667          :START TIME(OLE Automation date)
STOP            .d               42612.1666666667          :STOP TIME(OLE Automation date)
STEP            .d                            0            :STEP TIME(1s in time)
NULL            .                       -999.25            :NULL VALUE
COMP            .                   xxCompanyxx            :COMPANY
WELL            .                   xxWellxxxxx            :WELL NAME
FLD             .                   xxFieldxxxx            :FIELD NAME
RIGN            .                   xxRigxxxxxx            :Rig Name
RIGTYP          .                      Platform            :Rig Type
SRVC            .               xxxxxxxxxxxxxxx            :SERVICE COMPANY
DATE            .                    01/22/2016            :LOG DATE(Composite Date for Composite LAP) {MM/DD/YYYY}
#--------------------------------------------------
~CURVE INFORMATION
#MNEM           .UNIT                  API CODE            :DESCRIPTION
#----            ------          --------------            -----------------------------
TIME_1900       .d                                         :                                                        Time Index(OLE Automation date){S}
TIME            .s                                         :                                (1s)                    Time(hh mm ss/dd-MMM-yyyy){S}
ROP5            .m/h                                       :(RT)    (DRILLING_SURFACE)                              Rate of penetration averaged over the last 5 ft (1.5 m){F13.4}
DEPTH           .m                                         :(RT)    (DnMWorkflow)                                   Depth Index{F13.4}
HDTH            .m                                         :(RT)    (DnMWorkflow)                                   Hole Depth{F13.4}
TVD             .m                                         :(RT)    (DnMWorkflow)                                   True Vertical Depth{F13.4}
BLKP            .m                                         :(RT)    (DRILLING_SURFACE)                              Height of block above rig floor{F13.4}
HKLA            .1000 kgf                                  :(RT)    (DRILLING_SURFACE)                              Average Hookload{F13.4}
GR              .gAPI                                      :(RT)    (ARC8)                                          Gamma Ray{F13.4}
GR_CAL          .gAPI                                      :(RT)    (ARC8)                                          Calibrated Gamma Ray{F13.4}
TFLO            .L/min                                     :(RT)    (DRILLING_SURFACE)                              Total flow rate of all active pumps{F13.4}
SPPA            .bar                                       :(RT)    (DRILLING_SURFACE)                              Standpipe Pressure{F13.4}
RPM             .c/min                                     :(RT)    (DRILLING_SURFACE)                              Rotational Speed{F13.4}
CRPM            .c/min                                     :(RT)    (TELE825)                                       Collar Rotational Speed{F13.4}
TRPM            .c/min                                     :(RT)    (TELE825)                                       MWD Turbine Rotation Speed{F13.4}
STICK           .c/min                                     :(RT)    (TELE825)                                       Stick Slip Indicator{F13.4}
STICKRATIO      .                                          :(RT)    (TELE825)                                       Stick Ratio{F13.4}
SWOB            .1000 kgf                                  :(RT)    (DRILLING_SURFACE)                              Surface Weight On Bit{F13.4}
DWOB_AVG        .1000 kgf                                  :(RM)    (DMM1_900)                                      Mean Downhole Weight On Bit{F13.4}
DWOB_MAX        .1000 kgf                                  :(RM)    (DMM1_900)                                      Maximum Downhole Weight On Bit{F13.4}
DWOB_MIN        .1000 kgf                                  :(RM)    (DMM1_900)                                      Minimum Downhole Weight On Bit{F13.4}
STOR            .kN.m                                      :(RT)    (DRILLING_SURFACE)                              Surface Torque{F13.4}
DTOR_AVG        .kN.m                                      :(RM)    (DMM1_900)                                      Mean Downhole Torque{F13.4}
DTOR_MAX        .kN.m                                      :(RM)    (DMM1_900)                                      Downhole Maximum Torque{F13.4}
DTOR_MIN        .kN.m                                      :(RM)    (DMM1_900)                                      Minimum Downhole Torque{F13.4}
BND_AVG_DMM     .kN.m                                      :(RM)    (DMM1_900)                                      Mean Bending Magnitude at Strain Gauge{F13.4}
SHKPK           .gn                                        :(RT)    (TELE825)                                       Shock Peak{F13.4}
SHKL            .                                          :(RM)    (ARC8)                                          Tool Shock Level{F13.4}
SHKRSK          .                                          :(RT)    (TELE825)                                       Shock Risk{F13.4}
ESD             .g/cm3                                     :(RT)    (ARC8)                                          Equivalent Static Density{F13.4}
ESD_MAX         .g/cm3                                     :(RT)    (ARC8)                                          Maximum Equivalent Static Density{F13.4}
ESD_MIN         .g/cm3                                     :(RT)    (ARC8)                                          Mininum Equivalent Static Density{F13.4}
BIT_DEPTH       .m                                         :(RT)    (DRILLING_SURFACE)                              Bit Depth{F13.4}
PESD            .bar                                       :(RT)    (ARC8)                                          Hydrostatic pressure (ESD){F13.4}
ECD             .g/cm3                                     :(RM)    (ARC8)                                          Equivalent Circulating Density{F13.4}
DHAT            .degC                                      :(RM)    (ARC8)                                          Downhole Annulus Temperature{F13.4}
DHAP            .bar                                       :(RM)    (ARC8)                                          Downhole Annulus Pressure{F13.4}
#-------------------------------------------------------------
#       TIME_1900                 TIME         ROP5        DEPTH         HDTH          TVD         BLKP         HKLA           GR       GR_CAL         TFLO         SPPA          RPM         CRPM         TRPM        STICK   STICKRATIO         SWOB     DWOB_AVG     DWOB_MAX     DWOB_MIN         STOR     DTOR_AVG     DTOR_MAX     DTOR_MIN  BND_AVG_DMM        SHKPK         SHKL       SHKRSK          ESD      ESD_MAX      ESD_MIN    BIT_DEPTH         PESD          ECD         DHAT         DHAP 
#                                       (DRILLING_)  (DnMWorkfl)  (DnMWorkfl)  (DnMWorkfl)  (DRILLING_)  (DRILLING_)       (ARC8)       (ARC8)  (DRILLING_)  (DRILLING_)  (DRILLING_)    (TELE825)    (TELE825)    (TELE825)    (TELE825)  (DRILLING_)   (DMM1_900)   (DMM1_900)   (DMM1_900)  (DRILLING_)   (DMM1_900)   (DMM1_900)   (DMM1_900)   (DMM1_900)    (TELE825)       (ARC8)    (TELE825)       (ARC8)       (ARC8)       (ARC8)  (DRILLING_)       (ARC8)       (ARC8)       (ARC8)       (ARC8) 
#                                              (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RM)         (RM)         (RM)         (RT)         (RM)         (RM)         (RM)         (RM)         (RT)         (RM)         (RT)         (RT)         (RT)         (RT)         (RT)         (RT)         (RM)         (RM)         (RM) 
#                                 (1s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
~ASCII
 42606.1666666667 04:00:00/24-Aug-2016      -999.25    4700.8608    7700.0000    2015.4140      23.3843     114.2930      -999.25      -999.25      -999.25      20.4747      32.2050      -999.25      -999.25      -999.25      -999.25      -0.5530      -999.25      -999.25      -999.25      46.7503      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25    4700.8610      -999.25      -999.25      -999.25      -999.25
 42606.1666782407 04:00:01/24-Aug-2016      -999.25    4700.8545    7700.0000    2015.4140      23.3908     114.2869      -999.25      -999.25     525.6240      20.6346      32.2050      -999.25      -999.25      -999.25      -999.25      -0.5468      -999.25      -999.25      -999.25      47.1588      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25    4700.8540      -999.25      -999.25      -999.25      -999.25
 42606.1666898148 04:00:02/24-Aug-2016      -999.25    4700.8486    7700.0000    2015.4130      23.3966     114.2616      -999.25      -999.25      -999.25      20.7946      32.0874      -999.25      -999.25      -999.25      -999.25      -0.5216      -999.25      -999.25      -999.25      46.2750      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25      -999.25    4700.8490      -999.25      -999.25      -999.25      -999.25
