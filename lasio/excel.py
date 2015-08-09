import argparse

import xlwt

from . import las


class ExcelConverter(object):

    def __init__(self, las):
        self.las = las

    def write_excel(self, xlsfn):
        wb = xlwt.Workbook()
        md_sheet = wb.add_sheet("Header")
        curves_sheet = wb.add_sheet("Curves")

        md_sheet.write(0, 0, "Mnemonic")
        md_sheet.write(0, 1, "Value")
        for i, (key, value) in enumerate(self.las.metadata.items()):
            md_sheet.write(i + 1, 0, key)
            md_sheet.write(i + 1, 1, value)

        for i, curve in enumerate(self.las.curves):
            curves_sheet.write(0, i, curve.mnemonic)
            for j, value in enumerate(curve.data):
                curves_sheet.write(j + 1, i, value)

        wb.save(xlsfn)


def main():
    args = get_parser().parse_args(sys.argv[1:])
    lasfn = args.LAS_filename
    xlsfn = args.Excel_filename

    l = las.LASFile(lasfn)
    converter = ExcelConverter(l)
    converter.write_excel(xlsfn)


def get_parser():
    parser = argparse.ArgumentParser('Convert LAS file to Excel')
    parser.add_argument('LAS_filename')
    parser.add_argument('Excel_filename')
    return parser


if __name__ == '__main__':
    main()
