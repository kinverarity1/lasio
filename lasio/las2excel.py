try:
    import argparse
except ImportError:
    argparse = None
import sys

from . import las


class ExcelConverter(object):

    def __init__(self, las):
        self.las = las

    def write_excel(self, xlsfn):
        try:
            import pandas
            self.write_excel_pandas(self, xlsfn)
        except ImportError:
            try:
                import xlwt
                self.write_excel_xlwt(self, xlsfn)
            except ImportError:
                raise ImportError("Either pandas or xlwt are "
                                  "required to create Excel files")

    def write_excel_pandas(self):
        pass

    def write_excel_xlwt(self):
        wb = xlwt.Workbook()
        md_sheet = wb.add_sheet('Metadata')
        curves_sheet = wb.add_sheet('Curves')

        for i, (key, value) in enumerate(self.las.metadata_list()):
            md_sheet.write(i, 0, key)
            md_sheet.write(i, 1, value)

        for i, curve in enumerate(self.las.curves):
            curves_sheet.write(0, i, curve.name)
            for j, value in enumerate(curve.data):
                curves_sheet.write(j + 1, i, value)

        wb.save(xlsfn)


def main():
    if argparse:
        args = get_parser().parse_args(sys.argv[1:])
        lasfn = args.LAS_filename
        xlsfn = args.Excel_filename
    else:
        if len(sys.argv >= 3):
            lasfn = sys.argv[1]
            xlsfn = sys.argv[2]
        else:
            print('Convert LAS file to Excel.\n\n'
                  'Usage:\n\n'
                  'las2excel.py example.las output.xls')
            sys.exit(1)

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
