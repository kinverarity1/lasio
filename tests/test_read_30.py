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


@pytest.mark.skip(reason="Need to add 3.0 logic to read() and its sub-functions")
def test_read_v30_sample():
    las = lasio.read(stegfn("3.0", "sample_3.0.las"))
    assert las.version[0].mnemonic == "VERS"
    assert las.version[0].value == 3.0
    assert las.version[0].descr == "CWLS LOG ASCII STANDARD -VERSION 3.0"
