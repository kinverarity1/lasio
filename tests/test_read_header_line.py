# coding=utf-8

import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pprint import pprint

from lasio.reader import read_header_line


def test_time_str_and_colon_in_desc():
    line = "TIML.hh:mm 23:15 23-JAN-2001:   Time Logger: At Bottom"
    result = read_header_line(line, section_name="Parameter")
    # print('\n')
    # pprint(result)
    assert result["value"] == "23:15 23-JAN-2001"
    assert result["descr"] == "Time Logger: At Bottom"


def test_cyrillic_depth_unit():
    line = u" DEPT.метер                      :  1  DEPTH"
    result = read_header_line(line, section_name="Curves")
    assert result["unit"] == u"метер"
