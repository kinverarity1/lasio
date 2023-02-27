import os

import pytest

# pathlib for python2 is installed via pip install -r requirements.txt
from pathlib import Path

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lasio import read
from lasio.las import LASFile

test_dir = os.path.dirname(__file__)


def egfn(fn):
    return os.path.join(test_dir, "examples", fn)


def test_open_pathlib_object():
    las = read(Path(egfn("sample.las")))
    assert isinstance(las, LASFile)


def test_open_url():
    las = read(
        "https://raw.githubusercontent.com/kinverarity1/"
        "lasio/master/standards/examples"
        "/1.2/sample_curve_api.las"
    )
    assert isinstance(las, LASFile)


def test_open_url_different_newlines():
    las = read(
        "https://raw.githubusercontent.com/kinverarity1/"
        "lasio/master/tests/examples"
        "/2.0/sample_2.0_universal_newline.las"
    )
    assert las.well.keys() == [
        "STRT",
        "STOP",
        "STEP",
        "NULL",
        "COMP",
        "WELL",
        "FLD",
        "LOC",
        "PROV",
        "SRVC",
        "DATE",
        "UWI",
    ]


def test_open_file_object():
    with open(egfn("sample.las"), mode="r") as f:
        las = read(f)
        assert isinstance(las, LASFile)


def test_open_filename():
    las = read(egfn("sample.las"))
    assert isinstance(las, LASFile)


def test_open_incorrect_filename():
    with pytest.raises(OSError):
        las = read(egfn("sampleXXXDOES NOT EXIST.las"))
        # Should never get here because of the Exception
        assert not isinstance(las, LASFile)


def test_open_string():
    las = read(
        """~VERSION INFORMATION
 VERS.                  1.2:   CWLS LOG ASCII STANDARD -VERSION 1.2
 WRAP.                  NO:   ONE LINE PER DEPTH STEP
~WELL INFORMATION BLOCK
#MNEM.UNIT       DATA TYPE    INFORMATION
#---------    -------------   ------------------------------
 STRT.M        1670.000000:
 STOP.M        1660.000000:
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
 DT  .US/M               :  2  SONIC TRANSIT TIME
 RHOB.K/M3                   :  3  BULK DENSITY
 NPHI.V/V                    :  4   NEUTRON POROSITY
 SFLU.OHMM                   :  5  RXO RESISTIVITY
 SFLA.OHMM                   :  6  SHALLOW RESISTIVITY
 ILM .OHMM                   :  7  MEDIUM RESISTIVITY
 ILD .OHMM                   :  8  DEEP RESISTIVITY
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
~A  DEPTH     DT       RHOB     NPHI     SFLU     SFLA      ILM      ILD
1670.000   123.450 2550.000    0.450  123.450  123.450  110.200  105.600
1669.875   123.450 2550.000    0.450  123.450  123.450  110.200  105.600
1669.750   123.450 2550.000    0.450  123.450  123.450  110.200  105.600
"""
    )
    assert isinstance(las, LASFile)
