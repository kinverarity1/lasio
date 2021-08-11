import os
import sys
import logging
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio

test_dir = os.path.dirname(__file__)

stegfn = lambda vers, fn: os.path.join(os.path.dirname(__file__), "examples", vers, fn)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_read_v30_sample():
    las = lasio.read(stegfn("3.0", "sample_3.0.las"))
    assert las.version[0].mnemonic == "VERS"
    assert las.version[0].value == 3.0
    assert las.version[0].descr == "CWLS LOG ASCII STANDARD -VERSION 3.0"
    assert len(las.data) == 3
    assert len(las.data[0]) == 15
    assert las.data[2][8] == '2850000000000.0'
    assert las.data[2][9] == 'LOST INTERVAL   '


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
