import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy
import pytest

from lasio import read
from lasio import exceptions

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)


def test_null_policy_NULL_default(): # should read as NaN
    las = read(egfn("null_policy_-999.25.las"))
    assert numpy.isnan(las['DT'][0])

def test_null_policy_NULL_strict(): # should read as NaN
    las = read(egfn("null_policy_-999.25.las"), null_policy='strict')
    assert numpy.isnan(las['DT'][0])

def test_null_policy_NULL_none():
    las = read(egfn("null_policy_-999.25.las"), null_policy='none')
    assert las['DT'][0] == -999.25

def test_null_policy_9999_none():
    las = read(egfn("null_policy_9999.las"), null_policy='none')
    assert las['DT'][1] == 9999

def test_null_policy_9999_strict():
    las = read(egfn("null_policy_9999.las"), null_policy='strict')
    assert las['DT'][1] == 9999

def test_null_policy_9999_common():
    las = read(egfn("null_policy_9999.las"), null_policy='common')
    assert las['DT'][1] == 9999

def test_null_policy_9999_aggressive():
    las = read(egfn("null_policy_9999.las"), null_policy='aggressive')
    assert numpy.isnan(las['DT'][1])

def test_null_policy_9999_all():
    las = read(egfn("null_policy_9999.las"), null_policy='all')
    assert numpy.isnan(las['DT'][1])

def test_null_policy_custom_1_caught_9998():
    las = read(egfn("null_policy_9999.las"), null_policy=[9998, 'NULL'])
    assert numpy.isnan(las['DT'][0])

def test_null_policy_custom_1_caught_NULL():
    las = read(egfn("null_policy_9999.las"), null_policy=[9998, 'NULL'])
    assert numpy.isnan(las['SFLA'][2])

def test_null_policy_custom_2():
    las = read(egfn("null_policy_9999.las"), null_policy=[9998, ])
    assert numpy.isnan(las['DT'][0])
    assert las['SFLA'][2] == -999.25

def test_null_policy_ERR_strict():
    las = read(egfn("null_policy_ERR.las"), null_policy='strict')
    assert las['RHOB'][2] == 'ERR'
    
def test_null_policy_ERR_custom():
    las = read(egfn("null_policy_ERR.las"), null_policy=[('ERR', ' NaN '), ])
    assert numpy.isnan(las['RHOB'][2])
    
def test_null_policy_text_all_subs_ERR():
    las = read(egfn("null_policy_ERR.las"), null_policy='all')
    assert numpy.isnan(las['RHOB'][2])

def test_null_policy_text_all_keeps_data():
    las = read(egfn("null_policy_ERR.las"), null_policy='all')
    assert las['ILD'][2] == 105.6

def test_null_policy_text_all_subs_null():
    las = read(egfn("null_policy_(null).las"), null_policy='aggressive')
    assert numpy.isnan(las['RHOB'][2])

def test_null_policy_text_dashes_1():
    las = read(egfn("null_policy_dashes.las"), null_policy=['-', ])
    assert numpy.isnan(las['RHOB'][0])

def test_null_policy_text_dashes_2():
    las = read(egfn("null_policy_dashes.las"), null_policy=['-', ])
    assert numpy.isnan(las['RHOB'][2])

def test_null_policy_text_dashes_3():
    las = read(egfn("null_policy_dashes.las"), null_policy=['-', ])
    assert las['RHOB'][1] == -2550

def test_null_policy_runon_replaced_1():
    las = read(egfn("null_policy_runon.las"), read_policy='default')
    assert numpy.isnan(las['C04'][1])
    
def test_null_policy_runon_replaced_2():
    las = read(egfn("null_policy_runon.las"), read_policy='default')
    assert numpy.isnan(las['C05'][1])

def test_null_policy_runon_ok_1():
    las = read(egfn("null_policy_runon.las"), read_policy='default')
    assert las['C04'][2] == 7.33

def test_null_policy_runon_ok_2():
    las = read(egfn("null_policy_runon.las"), read_policy='default')
    assert las['C05'][2] == -19508.961
