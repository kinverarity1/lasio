import os
import logging

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio
import lasio.examples

test_dir = os.path.dirname(__file__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def stegfn(vers, fn):
    return os.path.join(test_dir, "examples", vers, fn)


def test_read_v30_sample():
    las = lasio.read(stegfn("3.0", "sample_3.0.las"))
    assert las.version[0].mnemonic == "VERS"
    assert las.version[0].value == 3.0
    assert las.version[0].descr == "CWLS LOG ASCII STANDARD -VERSION 3.0"
    assert len(las.data) == 3
    assert len(las.data[0]) == 15
    assert las.data[2][8] == "2850000000000.0"
    assert las.data[2][9] == "LOST INTERVAL   "


def test_read_v30_sample_standard_sections():
    """
    Verify 'Curves' does read '~Log_Definition'
    Verify 'Curves' doesn't read 'Core_*' sections
    Verity 'Parameter' does read '~Log_Parameter'
    Verify 'Parameter' doesn't read 'Performations_*' sections

    """
    las = lasio.read(stegfn("3.0", "sample_3.0.las"))
    assert las.curves.DEPT.unit == "M"
    # ~Log_Definition, a LAS3.0 equivalent of ~Curves has its data installed in Curves.
    assert las.sections["Curves"].DEPT.unit == "M"
    # ~Log_Parameter, a LAS3.0 equivalent of ~Parameter has its data installed in Parameter.
    assert "Log_Parameter" not in las.sections.keys()
    assert len(las.sections["Parameter"]) == 71
    assert las.sections["Perforations_Definition"][0].mnemonic == "PERFT:1"


def test_read_v30_tab_dlm_normal_engine():
    # GitHub Issue 554
    las = lasio.examples.open("3.0/sample_3.0_tab_dlm.las", engine="normal")
    assert las["DEPT"].data[1] == 1669.875


def test_read_v30_tab_dlm_numpy_engine():
    # GitHub Issue 554
    las = lasio.examples.open("3.0/sample_3.0_tab_dlm.las", engine="numpy")
    assert las["DEPT"].data[1] == 1669.875
