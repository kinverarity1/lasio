try:
    import argparse
except ImportError:
    argparse = None
import sys

from . import las


class ExcelConverter(object):

    def __init__(self, las):
        self.las = las

    def write_excel(self, xlsfn, lib=None):
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
        import pandas
        keys, values = zip(*self.las.metadata.items())
        md_df = pandas.DataFrame(
            data=[keys, values], columns=["Mnemonic", "Value"])
        c_df = pandas.DataFrame(
            data=[c.data for c in self.las.curves],
            columns=[c.mnemonic for c in self.las.curves])
        with pandas.ExcelWriter(xlsfn) as writer:
            md_df.to_excel(writer, sheet_name='Metadata')
            c_df.to_excel(writer, sheet_name='Curves')

    def write_excel_xlwt(self):
        import xlwt
        wb = xlwt.Workbook()
        md_sheet = wb.add_sheet('Metadata')
        curves_sheet = wb.add_sheet('Curves')

        md_sheet.write(0, 0, "Mnemonic")
        md_sheet.write(0, 1, "Value")
        for i, (key, value) in enumerate(self.las.metadata.items()):
            md_sheet.write(i + 1, 0, key)
            md_sheet.write(i + 1, 1, value)

        for i, curve in enumerate(self.las.curves):
            curves_sheet.write(0, i, curve.name)
            for j, value in enumerate(curve.data):
                curves_sheet.write(j + 1, i, value)

        wb.save(xlsfn)


def main():
    args = get_parser().parse_args(sys.argv[1:])
    lasfn = args.LAS_filename
    xlsfn = args.Excel_filename
    lib = args.lib

    l = las.LASFile(lasfn)
    converter = ExcelConverter(l, lib=lib)
    converter.write_excel(xlsfn)


def get_parser():
    parser = argparse.ArgumentParser('Convert LAS file to Excel')
    parser.add_argument('LAS_filename')
    parser.add_argument('Excel_filename')
    parser.add_argument("-l", "--lib", choices=("pandas", "xlwt"),
                        help="Python library to use for writing Excel files")
    return parser


if __name__ == '__main__':
    main()
