# lasio changelog

## version 0.10

- Internal change to SectionItems for future LAS 3.0 support
- Added JSON encoder
- Added examples for using pandas DataFrame (.df attribute)
- LAS > Excel script refined (las2excel.py)

## version 0.11

- Reorganise code into modules
- various 

### version 0.11.2

- Fix bug with not correctly figuring out units for LASFile.write()
- Add LASFile.add_curve(CurveItem) method which automatically goes to the old
  method at LASFile.add_curve_raw(mnemonic=, data=, ...) if necessary, so it
  should be transparent to users

## version 0.12

- Other minor bug fixes inc inability to rename mnemonics in written LAS file.