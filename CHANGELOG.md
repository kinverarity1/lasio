# List of changes

## Version 0.13

- Other minor bug fixes inc inability to rename mnemonics in written LAS file.

## Version 0.11.2

- Fix bug with not correctly figuring out units for LASFile.write()
- Add ``LASFile.add_curve(CurveItem)`` method which automatically goes to the old
  method at ``LASFile.add_curve_raw(mnemonic=, data=, ...)`` if necessary, so it
  should be transparent to users

## Version 0.11

- Reorganise code into modules
- various 

## Version 0.10

- Internal change to SectionItems for future LAS 3.0 support
- Added JSON encoder
- Added examples for using pandas DataFrame (.df attribute)
- LAS > Excel script refined (las2excel.py)

## Version 0.9.1 (2015-11-11)

 - pandas.DataFrame now as .df attribute, bugfix

## Version 0.8 (2015-08-20)

 - numerous bug fixes, API documentation added

## Version 0.7 (2015-08-08)

 - all tests passing on Python 2.6 through 3.4

## Version 0.6 (2015-08-05)

 - bugfixes and renamed from ``las_reader`` to ``lasio``

## Version 0.5 (2015-08-01)

 - Improvements to writing LAS files

## Version 0.4 (2015-07-26)

 - Improved handling of character encodings, other internal improvements

## Version 0.3 (2015-07-23)

 - Added Python 3 support, now reads LAS 1.2 and 2.0

## Version 0.2 (2015-07-08)

 - Tidied code and published on PyPI