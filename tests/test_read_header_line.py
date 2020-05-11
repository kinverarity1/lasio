# coding=utf-8

import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pprint import pprint

from lasio.reader import read_header_line


def test_time_str_and_colon_in_desc():
    line = "TIML.hh:mm 23:15 23-JAN-2001:   Time Logger: At Bottom"
    result = read_header_line(line, section_name="Parameter")
    assert result["value"] == "23:15 23-JAN-2001"
    assert result["descr"] == "Time Logger: At Bottom"


def test_cyrillic_depth_unit():
    line = u" DEPT.метер                      :  1  DEPTH"
    result = read_header_line(line, section_name="Curves")
    assert result["unit"] == u"метер"


def test_value_field_with_num_colon():
    line = "RUN . 01: RUN NUMBER"
    result = read_header_line(line, section_name="Parameter")
    assert result["value"] == "01"
    assert result["descr"] == "RUN NUMBER"


def test_non_delimiter_colon_in_desc():
    line = "QI     .      :         Survey quality: GOOD or BAD versus criteria"
    result = read_header_line(line, section_name="Parameter")
    assert result["value"] == ""
    assert result["descr"] == "Survey quality: GOOD or BAD versus criteria"
