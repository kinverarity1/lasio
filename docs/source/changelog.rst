List of changes
===============================

Version 0.29 (14 April 2021)
------------------------------
- Fix `#404`_ (lasio changes STEP with imprecise floating-point number behaviour; `#432`_)
- Add option ``len_numeric_field=-1``, ``lhs_spacer=" "``, and ``spacer=" "`` to writer.py:write (see `#412`_; PR `#418`_)
- Fix `#271`_ (Read quoted strings in data section properly; `#423`_)
- Fix `#427`_ (Change null_policy to handle small non-zero values; `#429`_)
- Fix `#417`_ (Fix parsing for empty ~Other section; `#430`_)
- Fix `#402`_ (fixes issue when unit starts with dot; `#403`_)
- Fix `#395`_ (Update doc examples to reflect new HeaderItem repr; `#410`_)
- Fix `#426`_ (Update urllib.request to be the preferred urllib; `#428`_)
- Add check for pushed tag version to version tests (`#396`_)
- Update GitHub Action Python CI testing (`#399`_, `#400`_)
- Improve ``las_items.py:HeaderItem.__repr__`` truncation logic (`#397`_)
- Remove codecs import (unused) and fix typo (`#406`_)
- Exclude LAS files from GitHubs Language Stats (`#411`_)
- Re-add try-except check around call to reader.read_data_section_iterative() (`#401`_)
- Remove reader.py:read_file_contents - unused code (see `#401`_; `#393`_)
- Add test for timestring with colon in ~Well section (see `#419`_ - PR `#420`_)
- Fix SyntaxWarning in writer.py (`#425`_)
- Add bugfix and feature request issue templates to GitHub repository
- Apply ``black`` code style to all Python files (`#438`_, `#398`_)
- Update `demo notebook for using logging levels <>`_ with current behaviour
- Update `contributing guide <https://github.com/kinverarity1/lasio/blob/master/docs/source/contributing.rst>`_ (`#437`_, `#441`_)

Version 0.28 (12 September 2020)
--------------------------------
- Major re-write of reader code working towards LAS 3.0 support (`#327`_; `#347`_, `#345`_, `#353`_, `#355`_, `#358`_, `#367`_, `#368`_, `#369`_)
- Fix `#377`_ (writing "None" as the value instead of ""; `#377`_)
- Fix `#373`_ (enable GitHub Actions CI testing on MacOS, Windows, Ubuntu; `#374`_, `#387`_)
- Fix `#363`_ (parse composite units such as "1000 lbf" correctly; `#390`_)
- Fix `#319`_ (allow skipping comment lines in data sections; `#391`_)
- Avoid unnecessary exceptions on reading LAS 3.0 data sections (`#385`_)
- Fix broken ReadTheDocs build

Version 0.27 (4 September 2020)
-------------------------------
- Fix `#380`_ (install failed without git installed; `#382`_)

Version 0.26 (31 August 2020)
-----------------------------
- This is the final version which works on Python 2.7 (`#364`_)
- Fix `#333`_ (header lines not parsed when colon is in description; `#335`_)
- Fix `#359`_ (sections not found when leading whitespace in line; `#360`_, `#361`_)
- Fix `#350`_ (bug with NULL; `#352`_)
- Fix `#339`_ (0.1IN not recognised as index unit; `#340`_, `#349`_)
- Fix `#31`_ (add command-line script to convert between LAS versions; `#329`_)
- Fix `#75`_ (add Cyrillic variant for metres; `#330`_)
- Fix `#326`_ (Support header-only LAS files--don't lose the last header section before a missing ~A section)
- Improve documentation regarding deleting items and curves (`#315`_, `#325`_)
- Add deprecation markers (`#331`_)
- Align json.dumps and LASFile.to_json() (`#328`_)
- Fixes and updates to setup.py relating to the adoption of setuptools_scm (`#312`_, `#317`_, `#318`_)
- Clean up and background changes related to future LAS 3.0 support: `#334`_, `#337`_, `#338`_, `#341`_, `#342`_, `#346`_, `#348`_, `#372`_

Version 0.25.1 (1 May 2020)
-------------------------------------------
- Shift to setuptools_scm (`#311`_)
- Fix `#321`_ (EOF character causes error on read)
- Fix `#182`_ (remove side-effect LASFile.write causing LASFile.version.VERS to change)
- Fix `#310`_ (remove LASFile.metadata which was not working)

Version 0.25 (28 March 2020)
--------------------------------------------
- Add stack_curves() method to allow joining a set of curves into a 2D array (issue `#284`_, PR `#293`_)
- Add lasio.examples module (`#296`_)
- Fix `#278`_ (leading zeroes were being stripped from API/UWI numbers)
- Fix `#286`_ (error on trying to write a file with one row of data)
- Fix `#258`_ (do not catch Ctrl+C when reading file)
- Fix `#292`_ (improve error checking for when trying to write non-2D data)
- Fix `#277`_ (allow pathlib objects to lasio.read)
- Fix `#264`_ (allow periods in mnemonics to be retained in specific cases)
- Fix `#201`_ (adjust descr parsing in \~P section to allow times in the descr, see PR `#298`_)
- Fix `#302`_ (change in str(datetime) handling)
- Fixes to JSON output (`#300`_, `#303`_)
- Fix `#304`_ (add column_fmt argument to LASFile.write method)

Version 0.24
--------------------------------------------
- Fix `#256`_ (parse units in brackets and add index_unit kwarg)

Version 0.23
--------------------------------------------
- Fix `#259`_ (error when encoding missing from URL response headers)
- Fix `#262`_ (broken build due to cchardet dependency)

Version 0.22
--------------------------------------------
- Fix `#252`_ (removing case sensitivity in index_unit checks)
- Fix `#249`_ (fix bug producing df without converting to floats)
- Attempt to fix Lasso classification on GitHub

Version 0.21
--------------------------------------------
- Fix `#236`_ and `#237`_ (can now read ASCII in ~Data section)
- Fix `#239`_ (Petrel can't read lasio output)

Version 0.20
--------------------------------------------
- Fix `#233`_ (pickling error lost Curve.data during multiprocessing)
- Fix `#226`_ (do not issue warning on empty ~Parameter section)
- Revised default behaviour to using null_policy='strict' (ref. `#227`_)
- Fix `#221`_ (depths > 10000 were being rounded by default)
- Fix `#225`_ (file handle leaked if exception during parsing)

Version 0.19
--------------------------------------------
- Fix `#223`_ (critical version/installation bug)

Version 0.18
--------------------------------------------
- Fix version numbering setup
- Fix `#92`_ (can ignore blah blah lines in ~C section)
- Fix `#209`_ (can now add curves with LASFile['mnemonic'] = [1, 2, 3])
- Fix `#213`_ (LASFile.data is now a lazily generated property, with setter)
- Fix `#218`_ (LASFile.append_curve was not adding data=[...] properly)
- Fix `#216`_ (LASFile now raises KeyError for missing mnemonics)
- Fix `#214`_ (first duplicate mnemonic when added was missing the :1)

Version 0.17
--------------------------------------------
- Add Appveyor continuous integration testing
- Add example notebook for how to use python logging module
- Fix `#160`_ (add methods to LASFile for inserting curves)
- Fix `#155`_ (implement del keyword for header items)
- Fix `#142`_ (implement slicing for SectionItems)
- Fix `#135`_ (UWI numbers losing their leading zeros)
- Fix `#153`_ (fix SectionItems pprint repr in Python 3)
- Fix `#81`_ (accept header items with missing colon)
- Fix `#71`_ (add Docker build for lasio to DockerHub)
- Fix `#210`_ (allow upper/lowercase standardization of mnemonics on read)
- Document recent additions (nearly up to date) (in Sphinx docs)

Version 0.16
--------------------------------------------
- Add read_policy and null_policy keywords - see documentation for details
- Fix bugs around files with missing ~V ~W ~P or ~C sections (`#84`_ `#85`_ `#78`_)
- Fix `#17`_ involving files with commas as a decimal mark
- Improve LASHeaderError traceback message
- Fix bug involving files with ~A but no data lines following
- Fix bug with blank line at start of file
- Fix bug involving missing or duplicate STRT, STOP and STEP mnemonics

Version 0.15.1
--------------------------------------------
- Major performance improvements with both memory and speed
- Major improvement to read parser, now using iteration
- Add ``LASFile.to_excel()`` and ``LASFile.to_csv()`` export methods
- Improve ``las2excelbulk.py`` script
- Published new and updated Sphinx documentation
- Improved character encoding handling when ``chardet`` not installed
- ``autodetect_encoding=True`` by default
- Allow reading of multiple non-standard header sections (`#167`_, `#168`_)
- Add flexibility in reading corrupted headers (``ignore_header_errors=True``)
- Add ability to avoid reading in data (``ignore_data=True``)
- Remove excessive debugging messages
- Fix bug `#164`_ where ``FEET`` was not recognised as ``FT``
- Fix major globals() bug `#141`_ affecting LASFile.add_curve
- Add command-line version script ``$ lasio`` to show version number.

Version 0.14 and 0.15 skipped due to broken PyPI upload.

Version 0.13
--------------------------------------------
- Other minor bug fixes inc inability to rename mnemonics in written LAS file.

Version 0.11.2
--------------------------------------------
- Fix bug with not correctly figuring out units for LASFile.write()
- Add ``LASFile.add_curve(CurveItem)`` method which automatically goes to the old
  method at ``LASFile.add_curve_raw(mnemonic=, data=, ...)`` if necessary, so it
  should be transparent to users

Version 0.11
--------------------------------------------
- Reorganise code into modules
- various

Version 0.10
--------------------------------------------
- Internal change to SectionItems for future LAS 3.0 support
- Added JSON encoder
- Added examples for using pandas DataFrame (.df attribute)
- LAS > Excel script refined (las2excel.py)

Version 0.9.1 (2015-11-11)
--------------------------------------------
 - pandas.DataFrame now as .df attribute, bugfix

Version 0.8 (2015-08-20)
--------------------------------------------
 - numerous bug fixes, API documentation added

Version 0.7 (2015-08-08)
--------------------------------------------
 - all tests passing on Python 2.6 through 3.4

Version 0.6 (2015-08-05)
--------------------------------------------
 - bugfixes and renamed from ``las_reader`` to ``lasio``

Version 0.5 (2015-08-01)
--------------------------------------------
 - Improvements to writing LAS files

Version 0.4 (2015-07-26)
--------------------------------------------
 - Improved handling of character encodings, other internal improvements

Version 0.3 (2015-07-23)
--------------------------------------------
 - Added Python 3 support, now reads LAS 1.2 and 2.0

Version 0.2 (2015-07-08)
--------------------------------------------
 - Tidied code and published on PyPI

 .. `#404`_: https://github.com/kinverarity1/lasio/issues/404
 .. `#432`_: https://github.com/kinverarity1/lasio/issues/432
 .. `#412`_: https://github.com/kinverarity1/lasio/issues/412
 .. `#418`_: https://github.com/kinverarity1/lasio/issues/418
 .. `#271`_: https://github.com/kinverarity1/lasio/issues/271
 .. `#423`_: https://github.com/kinverarity1/lasio/issues/423
 .. `#427`_: https://github.com/kinverarity1/lasio/issues/427
 .. `#429`_: https://github.com/kinverarity1/lasio/issues/429
 .. `#417`_: https://github.com/kinverarity1/lasio/issues/417
 .. `#430`_: https://github.com/kinverarity1/lasio/issues/430
 .. `#402`_: https://github.com/kinverarity1/lasio/issues/402
 .. `#403`_: https://github.com/kinverarity1/lasio/issues/403
 .. `#395`_: https://github.com/kinverarity1/lasio/issues/395
 .. `#410`_: https://github.com/kinverarity1/lasio/issues/410
 .. `#426`_: https://github.com/kinverarity1/lasio/issues/426
 .. `#428`_: https://github.com/kinverarity1/lasio/issues/428
 .. `#396`_: https://github.com/kinverarity1/lasio/issues/396
 .. `#399`_: https://github.com/kinverarity1/lasio/issues/399
 .. `#400`_: https://github.com/kinverarity1/lasio/issues/400
 .. `#397`_: https://github.com/kinverarity1/lasio/issues/397
 .. `#406`_: https://github.com/kinverarity1/lasio/issues/406
 .. `#411`_: https://github.com/kinverarity1/lasio/issues/411
 .. `#401`_: https://github.com/kinverarity1/lasio/issues/401
 .. `#401`_: https://github.com/kinverarity1/lasio/issues/401
 .. `#393`_: https://github.com/kinverarity1/lasio/issues/393
 .. `#419`_: https://github.com/kinverarity1/lasio/issues/419
 .. `#420`_: https://github.com/kinverarity1/lasio/issues/420
 .. `#425`_: https://github.com/kinverarity1/lasio/issues/425
 .. `#438`_: https://github.com/kinverarity1/lasio/issues/438
 .. `#398`_: https://github.com/kinverarity1/lasio/issues/398
 .. `#437`_: https://github.com/kinverarity1/lasio/issues/437
 .. `#441`_: https://github.com/kinverarity1/lasio/issues/441
 .. `#327`_: https://github.com/kinverarity1/lasio/issues/327
 .. `#347`_: https://github.com/kinverarity1/lasio/issues/347
 .. `#345`_: https://github.com/kinverarity1/lasio/issues/345
 .. `#353`_: https://github.com/kinverarity1/lasio/issues/353
 .. `#355`_: https://github.com/kinverarity1/lasio/issues/355
 .. `#358`_: https://github.com/kinverarity1/lasio/issues/358
 .. `#367`_: https://github.com/kinverarity1/lasio/issues/367
 .. `#368`_: https://github.com/kinverarity1/lasio/issues/368
 .. `#369`_: https://github.com/kinverarity1/lasio/issues/369
 .. `#377`_: https://github.com/kinverarity1/lasio/issues/377
 .. `#377`_: https://github.com/kinverarity1/lasio/issues/377
 .. `#373`_: https://github.com/kinverarity1/lasio/issues/373
 .. `#374`_: https://github.com/kinverarity1/lasio/issues/374
 .. `#387`_: https://github.com/kinverarity1/lasio/issues/387
 .. `#363`_: https://github.com/kinverarity1/lasio/issues/363
 .. `#390`_: https://github.com/kinverarity1/lasio/issues/390
 .. `#319`_: https://github.com/kinverarity1/lasio/issues/319
 .. `#391`_: https://github.com/kinverarity1/lasio/issues/391
 .. `#385`_: https://github.com/kinverarity1/lasio/issues/385
 .. `#380`_: https://github.com/kinverarity1/lasio/issues/380
 .. `#382`_: https://github.com/kinverarity1/lasio/issues/382
 .. `#364`_: https://github.com/kinverarity1/lasio/issues/364
 .. `#333`_: https://github.com/kinverarity1/lasio/issues/333
 .. `#335`_: https://github.com/kinverarity1/lasio/issues/335
 .. `#359`_: https://github.com/kinverarity1/lasio/issues/359
 .. `#360`_: https://github.com/kinverarity1/lasio/issues/360
 .. `#361`_: https://github.com/kinverarity1/lasio/issues/361
 .. `#350`_: https://github.com/kinverarity1/lasio/issues/350
 .. `#352`_: https://github.com/kinverarity1/lasio/issues/352
 .. `#339`_: https://github.com/kinverarity1/lasio/issues/339
 .. `#340`_: https://github.com/kinverarity1/lasio/issues/340
 .. `#349`_: https://github.com/kinverarity1/lasio/issues/349
 .. `#31`_: https://github.com/kinverarity1/lasio/issues/31
 .. `#329`_: https://github.com/kinverarity1/lasio/issues/329
 .. `#75`_: https://github.com/kinverarity1/lasio/issues/75
 .. `#330`_: https://github.com/kinverarity1/lasio/issues/330
 .. `#326`_: https://github.com/kinverarity1/lasio/issues/326
 .. `#315`_: https://github.com/kinverarity1/lasio/issues/315
 .. `#325`_: https://github.com/kinverarity1/lasio/issues/325
 .. `#331`_: https://github.com/kinverarity1/lasio/issues/331
 .. `#328`_: https://github.com/kinverarity1/lasio/issues/328
 .. `#312`_: https://github.com/kinverarity1/lasio/issues/312
 .. `#317`_: https://github.com/kinverarity1/lasio/issues/317
 .. `#318`_: https://github.com/kinverarity1/lasio/issues/318
 .. `#334`_: https://github.com/kinverarity1/lasio/issues/334
 .. `#337`_: https://github.com/kinverarity1/lasio/issues/337
 .. `#338`_: https://github.com/kinverarity1/lasio/issues/338
 .. `#341`_: https://github.com/kinverarity1/lasio/issues/341
 .. `#342`_: https://github.com/kinverarity1/lasio/issues/342
 .. `#346`_: https://github.com/kinverarity1/lasio/issues/346
 .. `#348`_: https://github.com/kinverarity1/lasio/issues/348
 .. `#372`_: https://github.com/kinverarity1/lasio/issues/372
 .. `#311`_: https://github.com/kinverarity1/lasio/issues/311
 .. `#321`_: https://github.com/kinverarity1/lasio/issues/321
 .. `#182`_: https://github.com/kinverarity1/lasio/issues/182
 .. `#310`_: https://github.com/kinverarity1/lasio/issues/310
 .. `#284`_: https://github.com/kinverarity1/lasio/issues/284
 .. `#293`_: https://github.com/kinverarity1/lasio/issues/293
 .. `#296`_: https://github.com/kinverarity1/lasio/issues/296
 .. `#278`_: https://github.com/kinverarity1/lasio/issues/278
 .. `#286`_: https://github.com/kinverarity1/lasio/issues/286
 .. `#258`_: https://github.com/kinverarity1/lasio/issues/258
 .. `#292`_: https://github.com/kinverarity1/lasio/issues/292
 .. `#277`_: https://github.com/kinverarity1/lasio/issues/277
 .. `#264`_: https://github.com/kinverarity1/lasio/issues/264
 .. `#201`_: https://github.com/kinverarity1/lasio/issues/201
 .. `#298`_: https://github.com/kinverarity1/lasio/issues/298
 .. `#302`_: https://github.com/kinverarity1/lasio/issues/302
 .. `#300`_: https://github.com/kinverarity1/lasio/issues/300
 .. `#303`_: https://github.com/kinverarity1/lasio/issues/303
 .. `#304`_: https://github.com/kinverarity1/lasio/issues/304
 .. `#256`_: https://github.com/kinverarity1/lasio/issues/256
 .. `#259`_: https://github.com/kinverarity1/lasio/issues/259
 .. `#262`_: https://github.com/kinverarity1/lasio/issues/262
 .. `#252`_: https://github.com/kinverarity1/lasio/issues/252
 .. `#249`_: https://github.com/kinverarity1/lasio/issues/249
 .. `#236`_: https://github.com/kinverarity1/lasio/issues/236
 .. `#237`_: https://github.com/kinverarity1/lasio/issues/237
 .. `#239`_: https://github.com/kinverarity1/lasio/issues/239
 .. `#233`_: https://github.com/kinverarity1/lasio/issues/233
 .. `#226`_: https://github.com/kinverarity1/lasio/issues/226
 .. `#227`_: https://github.com/kinverarity1/lasio/issues/227
 .. `#221`_: https://github.com/kinverarity1/lasio/issues/221
 .. `#225`_: https://github.com/kinverarity1/lasio/issues/225
 .. `#223`_: https://github.com/kinverarity1/lasio/issues/223
 .. `#92`_: https://github.com/kinverarity1/lasio/issues/92
 .. `#209`_: https://github.com/kinverarity1/lasio/issues/209
 .. `#213`_: https://github.com/kinverarity1/lasio/issues/213
 .. `#218`_: https://github.com/kinverarity1/lasio/issues/218
 .. `#216`_: https://github.com/kinverarity1/lasio/issues/216
 .. `#214`_: https://github.com/kinverarity1/lasio/issues/214
 .. `#160`_: https://github.com/kinverarity1/lasio/issues/160
 .. `#155`_: https://github.com/kinverarity1/lasio/issues/155
 .. `#142`_: https://github.com/kinverarity1/lasio/issues/142
 .. `#135`_: https://github.com/kinverarity1/lasio/issues/135
 .. `#153`_: https://github.com/kinverarity1/lasio/issues/153
 .. `#81`_: https://github.com/kinverarity1/lasio/issues/81
 .. `#71`_: https://github.com/kinverarity1/lasio/issues/71
 .. `#210`_: https://github.com/kinverarity1/lasio/issues/210
 .. `#84`_: https://github.com/kinverarity1/lasio/issues/84
 .. `#85`_: https://github.com/kinverarity1/lasio/issues/85
 .. `#78`_: https://github.com/kinverarity1/lasio/issues/78
 .. `#17`_: https://github.com/kinverarity1/lasio/issues/17
 .. `#167`_: https://github.com/kinverarity1/lasio/issues/167
 .. `#168`_: https://github.com/kinverarity1/lasio/issues/168
 .. `#164`_: https://github.com/kinverarity1/lasio/issues/164
 .. `#141`_: https://github.com/kinverarity1/lasio/issues/141
