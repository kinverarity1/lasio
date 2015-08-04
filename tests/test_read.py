import os


import las_reader

test_dir = os.path.dirname(__file__)


def test_dodgy_param_sect():
    fn = os.path.join(test_dir, "examples", "dodgy_param_sect.las")
    l = las_reader.read(fn)
