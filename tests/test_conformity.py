import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import glob
import fnmatch
import traceback
import logging

import numpy
import pytest

import lasio
from lasio import spec

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)

logger = logging.getLogger(__name__)


def test_check_conforming_no_version_section():
    las = lasio.read(egfn("missing_version_section.las"))
    assert not las.check_conforming()


def test_check_conforming_no_well_section():
    las = lasio.read(egfn("missing_well_section.las"))
    assert not las.check_conforming()


def test_check_conforming_no_curves_section():
    las = lasio.read(egfn("missing_curves_section.las"))
    assert not las.check_conforming()


def test_check_conforming_no_ascii_section():
    las = lasio.read(egfn("missing_ascii_section.las"))
    assert not las.check_conforming()


def test_check_ascii_for_no_curves():
    las = lasio.read(egfn("missing_curves_section.las"))
    assert not spec.AsciiSectionExists.check(las)


def test_check_no_version():
    las = lasio.read(egfn("missing_vers.las"))
    assert not las.check_conforming()


def test_check_no_wrap():
    las = lasio.read(egfn("missing_wrap.las"))
    assert not las.check_conforming()


def test_check_no_well_well():
    las = lasio.read(egfn("missing_well_well.las"))
    assert not spec.MandatoryLinesInWellSection.check(las)


def test_check_no_well_strt():
    las = lasio.read(egfn("missing_well_strt.las"))
    assert not spec.MandatoryLinesInWellSection.check(las)


def test_check_no_well_stop():
    las = lasio.read(egfn("missing_well_stop.las"))
    assert not spec.MandatoryLinesInWellSection.check(las)


def test_check_no_well_step():
    las = lasio.read(egfn("missing_well_step.las"))
    assert not spec.MandatoryLinesInWellSection.check(las)


def test_check_conforming_positive():
    las = lasio.read(egfn("sample.las"))
    assert las.check_conforming()


