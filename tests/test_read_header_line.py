# coding=utf-8

# 02-20-2023: dcs: leaving this commented out for now, in case it needs to be
# restored. Remove after 05-2023
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lasio.reader import read_header_line


def test_time_str_and_colon_in_desc():
    line = "TIML.hh:mm 23:15 23-JAN-2001:   Time Logger: At Bottom"
    result = read_header_line(line, section_name="Parameter")
    assert result["value"] == "23:15 23-JAN-2001"
    assert result["descr"] == "Time Logger: At Bottom"


def test_time_str_and_colon_in_desc_2():
    # https://github.com/kinverarity1/lasio/issues/419
    line = "STRT.DateTime 2012-09-16T07:44:12-05:00 : START DEPTH"
    result = read_header_line(line, section_name="Well")
    assert result["value"] == "2012-09-16T07:44:12-05:00"
    assert result["descr"] == "START DEPTH"
    assert result["unit"] == "DateTime"


def test_cyrillic_depth_unit():
    line = u" DEPT.метер                      :  1  DEPTH"
    result = read_header_line(line, section_name="Curves")
    assert result["unit"] == u"метер"


def test_unit_stat_with_dot():
    line = u" TDEP  ..1IN                      :  0.1-in"
    result = read_header_line(line, section_name="Curves")
    assert result["unit"] == u".1IN"


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


def test_dot_in_name():
    """issue_264"""
    line = "I. Res..OHM-M                  "
    result = read_header_line(line, section_name="Curves")
    assert result["name"] == "I. Res."


def test_pattern_arg():
    line = "DEPT.M                      :  1  DEPTH"

    name_re = "\\.?(?P<name>[^.]*)"
    unit_re = "\\.(?P<unit>[^\\s]*)"
    value_re = "(?P<value>.*)"
    colon_delim = ":"
    descr_re = "(?P<descr>.*)"

    pattern_re = "".join((name_re, unit_re, value_re, colon_delim, descr_re))

    result = read_header_line(line, section_name="Curves", pattern=pattern_re)

    assert result["name"] == "DEPT"
    assert result["unit"] == "M"
    assert result["value"] == ""


def test_unit_with_space():
    line = "HKLA            .1000 lbf                                  :(RT)"
    result = read_header_line(line, section_name="Parameter")
    assert result["name"] == "HKLA"
    assert result["unit"] == "1000 lbf"
    assert result["value"] == ""
    assert result["descr"] == "(RT)"


def test_line_without_period():
    line = "              DRILLED  :12/11/2010"
    result = read_header_line(line)
    assert result["name"] == "DRILLED"
    assert result["value"] == "12/11/2010"


def test_line_without_period_with_space():
    line = "              PERM DAT :1"
    result = read_header_line(line)
    assert result["name"] == "PERM DAT"
    assert result["value"] == "1"


def test_line_without_period_with_colon():
    line = "			  TIME     :14:00:32"
    result = read_header_line(line)
    assert result["name"] == "TIME"
    assert result["value"] == "14:00:32"


def test_line_without_period_with_decimal_value():
    line = "              HOLE DIA :85.7"
    result = read_header_line(line)
    assert result["name"] == "HOLE DIA"
    assert result["value"] == "85.7"
