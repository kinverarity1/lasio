# coding=utf-8

import os
import re
# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import lasio.las_version

version_regex = re.compile(r"^\d+\.\d+")


def test_non_existent_vcs_tool():
    version_cmd = ["gt", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    assert result == ""


# ------------------------------------------------------------------------------
# Most of the time GITHUB_WORKFLOW will install the lasio repo with the
# '--no-tag' option. In those cases tags won't be available and the resulting
# version is expected to be an empty string.
#
# Occationally a release version will be pushed and in those cases
# GITHUB_WORKFLOW will specifically make the refs/tag/<pushed-tag> available
# and the resulting version is expected to be a regular version string.
#
# So we check for both of those cases when testing in GITHUB_WORKFLOW
# environment.
# ------------------------------------------------------------------------------
def test_verify_default_vcs_tool():
    result = lasio.las_version._get_vcs_version()
    if "GITHUB_WORKFLOW" in os.environ:
        assert result == "" or version_regex.match(result)
    else:
        assert version_regex.match(result)


def test_explicit_existent_vcs_tool():
    version_cmd = ["git", "describe", "--tags", "--match", "v*"]
    result = lasio.las_version._get_vcs_version(version_cmd)
    if "GITHUB_WORKFLOW" in os.environ:
        assert result == "" or version_regex.match(result)
    else:
        assert version_regex.match(result)
