import os

import xlwt

from lasio import read, ExcelConverter

stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "test_examples", vers, fn)


def test_v12_xlwt():
    lasfn = stegfn("1.2", "sample.las")
    xlsfn = "sample_12.xls"
    l = read(lasfn)
    c = ExcelConverter(l)
    c.write_excel(xlsfn)
    os.remove(xlsfn)
