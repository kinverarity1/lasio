import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging

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


def test_check_no_version_section():
    las = lasio.read(egfn("missing_version_section.las"))
    assert not spec.MandatoryLinesInVersionSection.check(las)


def test_check_no_well_well():
    las = lasio.read(egfn("missing_well_well.las"))
    assert not las.check_conforming()


def test_check_no_well_strt():
    las = lasio.read(egfn("missing_well_strt.las"))
    assert not las.check_conforming()


def test_check_no_well_stop():
    las = lasio.read(egfn("missing_well_stop.las"))
    assert not las.check_conforming()


def test_check_no_well_step():
    las = lasio.read(egfn("missing_well_step.las"))
    assert not las.check_conforming()


def test_check_no_well_null():
    las = lasio.read(egfn("missing_well_null.las"))
    assert not las.check_conforming()


def test_check_no_well_comp():
    las = lasio.read(egfn("missing_well_comp.las"))
    assert not las.check_conforming()


def test_check_no_well_fld():
    las = lasio.read(egfn("missing_well_fld.las"))
    assert not las.check_conforming()


def test_check_no_well_loc():
    las = lasio.read(egfn("missing_well_loc.las"))
    assert not las.check_conforming()


def test_check_no_well_prov():
    las = lasio.read(egfn("missing_well_prov.las"))
    assert not las.check_conforming()


def test_check_no_well_prov_having_cnty():
    las = lasio.read(egfn("missing_well_prov_having_cnty.las"))
    assert las.check_conforming()


def test_check_no_well_srvc():
    las = lasio.read(egfn("missing_well_srvc.las"))
    assert not las.check_conforming()


def test_check_no_well_date():
    las = lasio.read(egfn("missing_well_date.las"))
    assert not las.check_conforming()


def test_check_no_well_uwi():
    las = lasio.read(egfn("missing_well_uwi.las"))
    assert not las.check_conforming()


def test_check_no_well_uwi_having_api():
    las = lasio.read(egfn("missing_well_uwi_having_api.las"))
    assert las.check_conforming()


def test_check_no_well_section():
    las = lasio.read(egfn("missing_well_section.las"))
    assert not spec.MandatoryLinesInWellSection.check(las)


def test_check_duplicate_sections():
    las = lasio.read(egfn("sample_duplicate_sections.las"))
    assert not las.check_conforming()


def test_check_sections_after_a_section():
    las = lasio.read(egfn("sample_sections_after_a_section.las"))
    assert not las.check_conforming()


def test_check_valid_mnemonic():
    las = lasio.read(egfn("invalid_index_mnemonic.las"))
    assert not las.check_conforming()


def test_check_v_section_first():
    las = lasio.read(egfn("sample_v_section_second.las"))
    assert not las.check_conforming()


def test_check_depth_divide_by_step():
    las = lasio.read(egfn("sample.las"))
    assert spec.ValidDepthDividedByStep.check(las)


def test_check_blank_line_in_section():
    las = lasio.read(egfn("blank_line_embedded_in_section.las"))
    assert not spec.BlankLineInSection.check(las)


def test_check_conforming_positive():
    las = lasio.read(egfn("sample.las"))
    assert las.check_conforming()
