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


def test_read_v30_sample_v20_sections_are_empty():
    """
    Verify 'Curves' doesn't read 'Core_*' sections
    Verify 'Parameter' doesn't read 'Performations_*' sections
    """
    las = lasio.read(stegfn("3.0", "sample_3.0.las"))
    assert not las.sections["Curves"]
    assert not las.sections["Parameter"]
    assert las.sections["Perforations_Definition"][0].mnemonic == "PERFT:1"
