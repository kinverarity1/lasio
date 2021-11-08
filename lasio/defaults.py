# coding=utf-8

import re

import numpy as np

from .las_items import HeaderItem, SectionItems, OrderedDict


def get_default_items():
    return {
        "Version": SectionItems(
            [
                HeaderItem("VERS", "", 2.0, "CWLS log ASCII Standard -VERSION 2.0"),
                HeaderItem("WRAP", "", "NO", "One line per depth step"),
                HeaderItem("DLM", "", "SPACE", "Column Data Section Delimiter"),
            ]
        ),
        "Well": SectionItems(
            [
                HeaderItem("STRT", "m", np.nan, "START DEPTH"),
                HeaderItem("STOP", "m", np.nan, "STOP DEPTH"),
                HeaderItem("STEP", "m", np.nan, "STEP"),
                HeaderItem("NULL", "", -9999.25, "NULL VALUE"),
                HeaderItem("COMP", "", "", "COMPANY"),
                HeaderItem("WELL", "", "", "WELL"),
                HeaderItem("FLD", "", "", "FIELD"),
                HeaderItem("LOC", "", "", "LOCATION"),
                HeaderItem("PROV", "", "", "PROVINCE"),
                HeaderItem("CNTY", "", "", "COUNTY"),
                HeaderItem("STAT", "", "", "STATE"),
                HeaderItem("CTRY", "", "", "COUNTRY"),
                HeaderItem("SRVC", "", "", "SERVICE COMPANY"),
                HeaderItem("DATE", "", "", "DATE"),
                HeaderItem("UWI", "", "", "UNIQUE WELL ID"),
                HeaderItem("API", "", "", "API NUMBER"),
            ]
        ),
        "Curves": SectionItems([]),
        "Parameter": SectionItems([]),
        "Other": "",
        "Data": np.zeros(shape=(0, 1)),
    }


ORDER_DEFINITIONS = {
    1.2: OrderedDict(
        [
            ("Version", ["value:descr"]),
            (
                "Well",
                [
                    "descr:value",
                    (
                        "value:descr",
                        [
                            "STRT",
                            "STOP",
                            "STEP",
                            "NULL",
                            "strt",
                            "stop",
                            "step",
                            "null",
                        ],
                    ),
                ],
            ),
            ("Curves", ["value:descr"]),
            ("Parameter", ["value:descr"]),
        ]
    ),
    2.0: OrderedDict(
        [
            ("Version", ["value:descr"]),
            ("Well", ["value:descr"]),
            ("Curves", ["value:descr"]),
            ("Parameter", ["value:descr"]),
        ]
    ),
    2.1: OrderedDict(
        [
            ("Version", ["value:descr"]),
            ("Well", ["value:descr"]),
            ("Curves", ["value:descr"]),
            ("Parameter", ["value:descr"]),
        ]
    ),
    3.0: OrderedDict(
        [
            ("Version", ["value:descr"]),
            ("Well", ["value:descr"]),
            ("Curves", ["value:descr"]),
            ("Parameter", ["value:descr"]),
        ]
    ),
}

DEPTH_UNITS = {
    "FT": ("FT", "F", "FEET", "FOOT"),
    "M": ("M", "METER", "METERS", "METRE", "METRES", u"метер", u"м"),
    ".1IN": (".1IN", "0.1IN", ".1INCH", "0.1INCH"),
}

READ_POLICIES = {
    # Note: `run-on(NaN.)` is now covered by `run-on(.)`
    "default": ["comma-decimal-mark", "run-on(-)", "run-on(.)"],
    "comma-delimiter": ["run-on(-)", "run-on(.)", "run-on(NaN.)"]
}

READ_SUBS = {
    "comma-decimal-mark": [(re.compile(r"(\d),(\d)"), r"\1.\2")],
    "run-on(-)": [(re.compile(r"(\d)-(\d)"), r"\1 -\2")],
    "run-on(.)": [(re.compile(r"-?\d*\.\d*\.\d*|NaN[\.-]\d+"), " NaN NaN ")],
}

NULL_POLICIES = {
    "none": [],
    "strict": ["NULL"],
    "common": ["NULL", "(null)", "-", "9999.25", "999.25", "NA", "INF", "IO", "IND"],
    "aggressive": [
        "NULL",
        "(null)",
        "--",
        "9999.25",
        "999.25",
        "NA",
        "INF",
        "IO",
        "IND",
        "999",
        "999.99",
        "9999",
        "9999.99" "2147483647",
        "32767",
        "-0.0",
    ],
    "all": [
        "NULL",
        "(null)",
        "-",
        "9999.25",
        "999.25",
        "NA",
        "INF",
        "IO",
        "IND",
        "999",
        "999.99",
        "9999",
        "9999.99" "2147483647",
        "32767",
        "-0.0",
        "numbers-only",
    ],
    "numbers-only": ["numbers-only"],
}

NULL_SUBS = {
    "NULL": [None],  # special case to be handled in LASFile.read()
    "999.25": [-999.25, 999.25],
    "9999.25": [-9999.25, 9999.25],
    "999.99": [-999.99, 999.99],
    "9999.99": [-9999.99, 9999.99],
    "999": [-999, 999],
    "9999": [-9999, 9999],
    "2147483647": [-2147483647, 2147483647],
    "32767": [-32767, 32767],
    "(null)": [
        (re.compile(r" \(null\)|\(null\) | \(NULL\)|\(NULL\) | null|null | NULL|NULL "), " NaN "),
    ],
    "-": [(re.compile(r" -+ "), " NaN ")],
    "NA": [(re.compile(r"(#N/A)[ ]|[ ](#N/A)"), " NaN ")],
    "INF": [
        (re.compile(r"(-?1\.#INF)[ ]|[ ](-?1\.#INF[0-9]*)"), " NaN "),
    ],
    "IO": [
        (re.compile(r"(-?1\.#IO)[ ]|[ ](-?1\.#IO)"), " NaN "),
    ],
    "IND": [
        (re.compile(r"(-?1\.#IND)[ ]|[ ](-?1\.#IND[0-9]*)"), " NaN "),
    ],
    "-0.0": [
        (re.compile(r"(-0\.0)[ ]|[ ](-0\.00*[^1-9])"), " NaN "),
    ],
    "numbers-only": [
        (re.compile(r"([^ 0-9.\-+]+)[ ]|[ ]([^ 0-9.\-+]+)"), " NaN "),
    ],
}
