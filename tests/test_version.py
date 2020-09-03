# coding=utf-8

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import re
version_regex = re.compile(r'^\d+\.\d+')

import lasio.las_version


def test_verify_default_vcs_tool():
    result = lasio.las_version._get_vcs_version()
    assert version_regex.match(result) 

def test_non_existant_vcs_tool():
    version_cmd = ["gt", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    assert result == ""


def test_explicit_existant_vcs_tool():
    version_cmd = ["git", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    assert version_regex.match(result) 
