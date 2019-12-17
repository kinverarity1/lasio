import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import numpy as np

import lasio.examples

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)


def test_local_path():
	assert os.path.isdir(lasio.examples.get_local_examples_path())

def test_local():
	l1 = lasio.read(egfn("sample.las"))
	l2 = lasio.examples.open_local_example("sample.las")
	assert l1._text == l2._text

def test_github():
	l1 = lasio.read(egfn("sample.las"))
	l2 = lasio.examples.open_github_example("sample.las")
	assert l1._text == l2._text

def test_open():
	l1 = lasio.read(egfn("sample.las"))
	l2 = lasio.examples.open("sample.las")
	assert l1._text == l2._text