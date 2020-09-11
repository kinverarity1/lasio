# coding=utf-8

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import re
version_regex = re.compile(r'^\d+\.\d+')

import lasio.las_version


def test_verify_default_vcs_tool():
    result = lasio.las_version._get_vcs_version()
    if 'GITHUB_WORKFLOW' in os.environ:
        assert result == ""
    else:
        assert version_regex.match(result) 

def test_non_existent_vcs_tool():
    version_cmd = ["gt", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    assert result == ""


def test_explicit_existent_vcs_tool():
    version_cmd = ["git", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    if 'GITHUB_WORKFLOW' in os.environ:
        assert result == ""
    else:
        assert version_regex.match(result) 
