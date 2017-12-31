import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch
import logging

import numpy as np
import pytest

import lasio

logger = logging.getLogger(__name__)

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_delete_curve():
    las = lasio.read(egfn("sample.las"))
    del las.curves['DT']
    assert las.curves.keys() == ['DEPT', 'RHOB', 'NPHI', 'SFLU', 'SFLA','ILM', 'ILD']

def test_delete_section_item_by_index():
    las = lasio.read(egfn('sample.las'))
    del las.params[1]
    assert las.params.keys() == ['BHT', 'FD', 'MATR', 'MDEN', 'RMF', 'DFD']

def test_delete_section_item_by_mnemonic():
    las = lasio.read(egfn('sample.las'))
    del las.params['MDEN']
    assert las.params.keys() == ['BHT', 'BS', 'FD', 'MATR', 'RMF', 'DFD']

def test_section_items_slice():
    las = lasio.read(egfn('sample.las'))
    sl = las.curves[slice(1, 4)]
    assert sl.keys() == ['DT', 'RHOB', 'NPHI']

def test_section_items_indices():
    las = lasio.read(egfn('sample.las'))
    logger.debug('Type of las.curves = {}'.format(type(las.curves)))
    sl = las.curves[1:4]
    # logger.debug(str(sl))
    assert sl.keys() == ['DT', 'RHOB', 'NPHI']

def test_add_curve_duplicate():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    las.add_curve('DEPT', a)
    las.add_curve('B', b1, descr='b1')
    las.add_curve('B', b2, descr='b2')
    # assert l.keys == ['DEPT', 'B', 'B']
    assert [c.descr for c in las.curves] == ['', 'b1', 'b2']


def test_append_curve_duplicate():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    las.append_curve('DEPT', a)
    las.append_curve('B', b1, descr='b1')
    las.append_curve('B', b2, descr='b2')
    assert [c.descr for c in las.curves] == ['', 'b1', 'b2']

def test_insert_curve_1():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    las.append_curve('DEPT', a)
    las.append_curve('B', b2, descr='b2')
    las.insert_curve(1, 'B', b1, descr='b1')
    assert [c.descr for c in las.curves] == ['', 'b1', 'b2']

def test_insert_curve_2():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    las.append_curve('DEPT', a)
    las.append_curve('B', b2, descr='b2')
    las.insert_curve(2, 'B', b1, descr='b1')
    assert [c.descr for c in las.curves] == ['', 'b2', 'b1']
    
def test_delete_curve_ix():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    las.append_curve('DEPT', a)
    las.append_curve('B', b2, descr='b2')
    las.insert_curve(2, 'B', b1, descr='b1')
    las.delete_curve(ix=0)
    assert [c.descr for c in las.curves] == ['b2', 'b1']


def test_delete_curve_mnemonic():
    las = lasio.LASFile()
    a = np.array([1, 2, 3, 4])
    b1 = np.array([5, 9, 1, 4])
    b2 = np.array([1, 2, 3, 2])
    logger.info(str([c.mnemonic for c in las.curves]))
    las.append_curve('DEPT', a)
    logger.info(str([c.mnemonic for c in las.curves]))
    las.append_curve('B', b2, descr='b2')
    logger.info(str([c.mnemonic for c in las.curves]))
    las.insert_curve(2, 'B', b1, descr='b1')
    logger.info(str([c.mnemonic for c in las.curves]))
    las.delete_curve(mnemonic='DEPT')
    assert [c.descr for c in las.curves] == ['b2', 'b1']

def test_mnemonic_case_comparison_preserve_1():
    las = lasio.read(egfn('mnemonic_case.las'), mnemonic_case='preserve')
    assert 'Dept' in las.curves

def test_mnemonic_case_comparison_preserve_2():
    las = lasio.read(egfn('mnemonic_case.las'), mnemonic_case='preserve')
    assert not 'DEPT' in las.curves

def test_mnemonic_case_comparison_upper():
    las = lasio.read(egfn('mnemonic_case.las'), mnemonic_case='upper')
    assert 'dept' in las.curves
    
def test_mnemonic_case_comparison_lower():
    las = lasio.read(egfn('mnemonic_case.las'), mnemonic_case='lower')
    assert 'DEPT' in las.curves

def test_missing_sectionitems_mnemonic():
    las = lasio.read(egfn('sample.las'))
    with pytest.raises(KeyError):
        las.curves['blahblahblah']

def test_mnemonic_rename_1():
    las = lasio.read(egfn('sample.las'))
    las.curves[-1].mnemonic = ''
    assert las.curves[-1].mnemonic == 'UNKNOWN'