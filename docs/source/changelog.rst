.. _ChangeLog:

List of changes
===============================

Unreleased changes (Available on GitHub)
----------------------------------------

Version 0.31 (18 May 2023)
--------------------------
- Many improvements to code style and formatting, and the documentation
- `#555`_ - Fix problem when writing with changed data (different number of depths)
- `#554`_ / `#556`_ - Enable DLM (delimiter) TAB
- `#552`_ - Remove or replace cchardet with chardet
- `#530`_ - Detect hyphens in data section and adjust regexp_subs as needed
- Fix `#322`_ - provide a way to consistently retrieve header items which may
  or may not be present in the header:

  If you try ordinary item-style access, as is normal in Python, a KeyError exception will be raised if it is missing:

  .. code-block:: python

      >>> permit = las.well['PRMT']
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "c:\devapps\kinverarity\projects\lasio\lasio\las_items.py", line 313, in __getitem__
          raise KeyError("%s not in %s" % (key, self.keys()))
      KeyError: "PRMT not in ['STRT', 'STOP', 'STEP', 'NULL', 'COMP', 'WELL', 'FLD', 'LOC', 'PROV', 'SRVC', 'DATE', 'UWI']"

  A better pattern is to use the :meth:`lasio.SectionItems.get` method, which
  allows you to specify a default value in the case of it missing:

  .. code-block:: python

      >>> permit = las.well.get('PRMT', 'unknown')
      >>> permit
      HeaderItem(mnemonic="PRMT", unit="", value="unknown", descr="")

  You can use the ``add=True`` keyword argument if you would like this 
  header item to be added, as well as returned:

  .. code-block:: python

      >>> permit = las.well.get('PRMT', 'unknown', add=True)
      >>> las.well
      [HeaderItem(mnemonic="STRT", unit="M", value="0.05", descr="FIRST INDEX VALUE"),
      HeaderItem(mnemonic="STOP", unit="M", value="136.6", descr="LAST INDEX VALUE"),
      HeaderItem(mnemonic="STEP", unit="M", value="0.05", descr="STEP"),
      HeaderItem(mnemonic="NULL", unit="", value="-99999", descr="NULL VALUE"),
      HeaderItem(mnemonic="COMP", unit="", value="", descr="COMP"),
      HeaderItem(mnemonic="WELL", unit="", value="Scorpio E1", descr="WELL"),
      HeaderItem(mnemonic="FLD", unit="", value="", descr=""),
      HeaderItem(mnemonic="LOC", unit="", value="Mt Eba", descr="LOC"),
      HeaderItem(mnemonic="SRVC", unit="", value="", descr=""),
      HeaderItem(mnemonic="CTRY", unit="", value="", descr=""),
      HeaderItem(mnemonic="STAT", unit="", value="SA", descr="STAT"),
      HeaderItem(mnemonic="CNTY", unit="", value="", descr=""),
      HeaderItem(mnemonic="DATE", unit="", value="15/03/2015", descr="DATE"),
      HeaderItem(mnemonic="UWI", unit="", value="6038-187", descr="WUNT"),
      HeaderItem(mnemonic="PRMT", unit="", value="unknown", descr="")]

Version 0.30 (12 May 2022)
--------------------------
- Fixes for `#446`_ (Implement a numpy-based reader for the data section; `#452`_) and 
  `#444`_ (Provide a way to benchmark speed performance of LASFile.read; `#449`_). This leads to
  a more than two-fold improvement in speed (e.g. from 1091 msec to 341 msec for
  a large sample file).
- Fixes for `#439`_ (Data section containing non-numeric chars is parsed entirely as str) and `#227`_
  (NULL value replacing valid value in DEPT) by allowing different data types
  for different columns (PRs `#459`_, `#460`_, `#461`_)
- Partially fix `#375`_ (allow writing mnemonics in ~ASCII line; PRs `#466`_, `#471`_, `#465`_)
- Partial fix for `#265`_ (Parse comma-delimited ~ASCII sections; `#485`_)
- Fix `#83`_ (LAS file with more curves defined in ~C section than available in ~A section; `#480`_)
- Improve visibility and access to the Code of Conduct (`#469`_)
- Fix `#453`_ (rounding issues when writing LAS file) (`#455`_)
- Fix `#268`_ (remove side-effects from writer) (`#447`_, `#451`_)
- Documentation updates (`#475`_, `#477`_, `#481`_, `#501`_, `#498`_, `#500`_)
- Fix `#473`_ (Header lines without a period are discarded unnecessarily)
- Fix `#472`_ (Detect and raise IOError exception for LiDAR files; `#482`_)
- Fix `#483`_ (perfomance decrease in DEBUG logging level; `#484`_)
- Fix `#478`_ (:1 :2 should only be appended to mnemonics when using LASFile.read) with `#479`_: 
  Add update_curve and replace_curve_item methods to LASFile
- Fix `#490`_ (LAS 2.1 reading error; `#491`_)
- Fix `#486`_ (Adding a citation file, and maybe a DOI; `#487`_)
- Fix `#392`_ (ignore_comments not mentioned in documentation; `#495`_)
- Fix `#332`_: Describe default read_policies in docstring, with `#489`_
- Fix `#502`_ (NumPy type conversion alias deprecation; `#503`_)
- minor performance improvements (`#470`_, )

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
- Update `demo notebook for using logging levels <https://github.com/kinverarity1/lasio/blob/main/notebooks/set%20logging%20level%20for%20lasio.ipynb>`_ with current behaviour
- Update `contributing guide <https://github.com/kinverarity1/lasio/blob/main/docs/source/contributing.rst>`_ (`#437`_, `#441`_)

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

.. _#17: https://github.com/kinverarity1/lasio/issues/17
.. _#31: https://github.com/kinverarity1/lasio/issues/31
.. _#71: https://github.com/kinverarity1/lasio/issues/71
.. _#75: https://github.com/kinverarity1/lasio/issues/75
.. _#78: https://github.com/kinverarity1/lasio/issues/78
.. _#81: https://github.com/kinverarity1/lasio/issues/81
.. _#83: https://github.com/kinverarity1/lasio/issues/83
.. _#84: https://github.com/kinverarity1/lasio/issues/84
.. _#85: https://github.com/kinverarity1/lasio/issues/85
.. _#92: https://github.com/kinverarity1/lasio/issues/92
.. _#135: https://github.com/kinverarity1/lasio/issues/135
.. _#141: https://github.com/kinverarity1/lasio/issues/141
.. _#142: https://github.com/kinverarity1/lasio/issues/142
.. _#153: https://github.com/kinverarity1/lasio/issues/153
.. _#155: https://github.com/kinverarity1/lasio/issues/155
.. _#160: https://github.com/kinverarity1/lasio/issues/160
.. _#164: https://github.com/kinverarity1/lasio/issues/164
.. _#167: https://github.com/kinverarity1/lasio/issues/167
.. _#168: https://github.com/kinverarity1/lasio/pull/168
.. _#182: https://github.com/kinverarity1/lasio/issues/182
.. _#201: https://github.com/kinverarity1/lasio/issues/201
.. _#209: https://github.com/kinverarity1/lasio/issues/209
.. _#210: https://github.com/kinverarity1/lasio/issues/210
.. _#213: https://github.com/kinverarity1/lasio/issues/213
.. _#214: https://github.com/kinverarity1/lasio/issues/214
.. _#216: https://github.com/kinverarity1/lasio/issues/216
.. _#218: https://github.com/kinverarity1/lasio/issues/218
.. _#221: https://github.com/kinverarity1/lasio/pull/221
.. _#223: https://github.com/kinverarity1/lasio/issues/223
.. _#225: https://github.com/kinverarity1/lasio/pull/225
.. _#226: https://github.com/kinverarity1/lasio/issues/226
.. _#227: https://github.com/kinverarity1/lasio/issues/227
.. _#233: https://github.com/kinverarity1/lasio/issues/233
.. _#236: https://github.com/kinverarity1/lasio/issues/236
.. _#237: https://github.com/kinverarity1/lasio/issues/237
.. _#239: https://github.com/kinverarity1/lasio/pull/239
.. _#249: https://github.com/kinverarity1/lasio/pull/249
.. _#252: https://github.com/kinverarity1/lasio/pull/252
.. _#256: https://github.com/kinverarity1/lasio/issues/256
.. _#258: https://github.com/kinverarity1/lasio/pull/258
.. _#259: https://github.com/kinverarity1/lasio/issues/259
.. _#262: https://github.com/kinverarity1/lasio/issues/262
.. _#264: https://github.com/kinverarity1/lasio/issues/264
.. _#271: https://github.com/kinverarity1/lasio/issues/271
.. _#277: https://github.com/kinverarity1/lasio/issues/277
.. _#278: https://github.com/kinverarity1/lasio/issues/278
.. _#284: https://github.com/kinverarity1/lasio/issues/284
.. _#286: https://github.com/kinverarity1/lasio/pull/286
.. _#292: https://github.com/kinverarity1/lasio/pull/292
.. _#293: https://github.com/kinverarity1/lasio/pull/293
.. _#296: https://github.com/kinverarity1/lasio/pull/296
.. _#298: https://github.com/kinverarity1/lasio/pull/298
.. _#300: https://github.com/kinverarity1/lasio/pull/300
.. _#302: https://github.com/kinverarity1/lasio/pull/302
.. _#303: https://github.com/kinverarity1/lasio/issues/303
.. _#304: https://github.com/kinverarity1/lasio/issues/304
.. _#310: https://github.com/kinverarity1/lasio/issues/310
.. _#311: https://github.com/kinverarity1/lasio/pull/311
.. _#312: https://github.com/kinverarity1/lasio/issues/312
.. _#315: https://github.com/kinverarity1/lasio/issues/315
.. _#317: https://github.com/kinverarity1/lasio/pull/317
.. _#318: https://github.com/kinverarity1/lasio/pull/318
.. _#319: https://github.com/kinverarity1/lasio/issues/319
.. _#321: https://github.com/kinverarity1/lasio/issues/321
.. _#322: https://github.com/kinverarity1/lasio/issues/322
.. _#325: https://github.com/kinverarity1/lasio/pull/325
.. _#326: https://github.com/kinverarity1/lasio/pull/326
.. _#327: https://github.com/kinverarity1/lasio/pull/327
.. _#328: https://github.com/kinverarity1/lasio/pull/328
.. _#329: https://github.com/kinverarity1/lasio/pull/329
.. _#330: https://github.com/kinverarity1/lasio/pull/330
.. _#331: https://github.com/kinverarity1/lasio/pull/331
.. _#333: https://github.com/kinverarity1/lasio/issues/333
.. _#334: https://github.com/kinverarity1/lasio/pull/334
.. _#335: https://github.com/kinverarity1/lasio/pull/335
.. _#337: https://github.com/kinverarity1/lasio/pull/337
.. _#338: https://github.com/kinverarity1/lasio/pull/338
.. _#339: https://github.com/kinverarity1/lasio/issues/339
.. _#340: https://github.com/kinverarity1/lasio/pull/340
.. _#341: https://github.com/kinverarity1/lasio/pull/341
.. _#342: https://github.com/kinverarity1/lasio/pull/342
.. _#345: https://github.com/kinverarity1/lasio/pull/345
.. _#346: https://github.com/kinverarity1/lasio/pull/346
.. _#347: https://github.com/kinverarity1/lasio/pull/347
.. _#348: https://github.com/kinverarity1/lasio/pull/348
.. _#349: https://github.com/kinverarity1/lasio/pull/349
.. _#350: https://github.com/kinverarity1/lasio/issues/350
.. _#352: https://github.com/kinverarity1/lasio/pull/352
.. _#353: https://github.com/kinverarity1/lasio/pull/353
.. _#355: https://github.com/kinverarity1/lasio/pull/355
.. _#358: https://github.com/kinverarity1/lasio/pull/358
.. _#359: https://github.com/kinverarity1/lasio/issues/359
.. _#360: https://github.com/kinverarity1/lasio/pull/360
.. _#361: https://github.com/kinverarity1/lasio/pull/361
.. _#363: https://github.com/kinverarity1/lasio/issues/363
.. _#364: https://github.com/kinverarity1/lasio/issues/364
.. _#367: https://github.com/kinverarity1/lasio/pull/367
.. _#368: https://github.com/kinverarity1/lasio/pull/368
.. _#369: https://github.com/kinverarity1/lasio/pull/369
.. _#372: https://github.com/kinverarity1/lasio/pull/372
.. _#373: https://github.com/kinverarity1/lasio/issues/373
.. _#374: https://github.com/kinverarity1/lasio/pull/374
.. _#377: https://github.com/kinverarity1/lasio/issues/377
.. _#380: https://github.com/kinverarity1/lasio/issues/380
.. _#382: https://github.com/kinverarity1/lasio/pull/382
.. _#385: https://github.com/kinverarity1/lasio/pull/385
.. _#387: https://github.com/kinverarity1/lasio/pull/387
.. _#390: https://github.com/kinverarity1/lasio/pull/390
.. _#391: https://github.com/kinverarity1/lasio/pull/391
.. _#393: https://github.com/kinverarity1/lasio/pull/393
.. _#395: https://github.com/kinverarity1/lasio/issues/395
.. _#396: https://github.com/kinverarity1/lasio/pull/396
.. _#397: https://github.com/kinverarity1/lasio/pull/397
.. _#398: https://github.com/kinverarity1/lasio/pull/398
.. _#399: https://github.com/kinverarity1/lasio/pull/399
.. _#400: https://github.com/kinverarity1/lasio/pull/400
.. _#401: https://github.com/kinverarity1/lasio/pull/401
.. _#402: https://github.com/kinverarity1/lasio/issues/402
.. _#403: https://github.com/kinverarity1/lasio/pull/403
.. _#404: https://github.com/kinverarity1/lasio/issues/404
.. _#406: https://github.com/kinverarity1/lasio/pull/406
.. _#410: https://github.com/kinverarity1/lasio/pull/410
.. _#411: https://github.com/kinverarity1/lasio/pull/411
.. _#412: https://github.com/kinverarity1/lasio/issues/412
.. _#417: https://github.com/kinverarity1/lasio/issues/417
.. _#418: https://github.com/kinverarity1/lasio/pull/418
.. _#419: https://github.com/kinverarity1/lasio/issues/419
.. _#420: https://github.com/kinverarity1/lasio/pull/420
.. _#423: https://github.com/kinverarity1/lasio/pull/423
.. _#425: https://github.com/kinverarity1/lasio/pull/425
.. _#426: https://github.com/kinverarity1/lasio/issues/426
.. _#427: https://github.com/kinverarity1/lasio/issues/427
.. _#428: https://github.com/kinverarity1/lasio/pull/428
.. _#429: https://github.com/kinverarity1/lasio/pull/429
.. _#430: https://github.com/kinverarity1/lasio/pull/430
.. _#432: https://github.com/kinverarity1/lasio/pull/432
.. _#437: https://github.com/kinverarity1/lasio/pull/437
.. _#438: https://github.com/kinverarity1/lasio/pull/438
.. _#441: https://github.com/kinverarity1/lasio/pull/441
.. _#447: https://github.com/kinverarity1/lasio/pull/447
.. _#449: https://github.com/kinverarity1/lasio/pull/449
.. _#268: https://github.com/kinverarity1/lasio/issues/268
.. _#451: https://github.com/kinverarity1/lasio/pull/451
.. _#453: https://github.com/kinverarity1/lasio/issues/453
.. _#455: https://github.com/kinverarity1/lasio/pull/455
.. _#265: https://github.com/kinverarity1/lasio/issues/265
.. _#332: https://github.com/kinverarity1/lasio/issues/332
.. _#375: https://github.com/kinverarity1/lasio/issues/375
.. _#392: https://github.com/kinverarity1/lasio/issues/392
.. _#439: https://github.com/kinverarity1/lasio/issues/439
.. _#444: https://github.com/kinverarity1/lasio/issues/444
.. _#446: https://github.com/kinverarity1/lasio/issues/446
.. _#452: https://github.com/kinverarity1/lasio/pull/452
.. _#459: https://github.com/kinverarity1/lasio/pull/459
.. _#460: https://github.com/kinverarity1/lasio/pull/460
.. _#461: https://github.com/kinverarity1/lasio/pull/461
.. _#465: https://github.com/kinverarity1/lasio/pull/465
.. _#466: https://github.com/kinverarity1/lasio/pull/466
.. _#469: https://github.com/kinverarity1/lasio/pull/469
.. _#470: https://github.com/kinverarity1/lasio/pull/470
.. _#471: https://github.com/kinverarity1/lasio/pull/471
.. _#472: https://github.com/kinverarity1/lasio/issues/472
.. _#473: https://github.com/kinverarity1/lasio/issues/473
.. _#475: https://github.com/kinverarity1/lasio/pull/475
.. _#477: https://github.com/kinverarity1/lasio/issues/477
.. _#478: https://github.com/kinverarity1/lasio/issues/478
.. _#479: https://github.com/kinverarity1/lasio/pull/479
.. _#480: https://github.com/kinverarity1/lasio/pull/480
.. _#481: https://github.com/kinverarity1/lasio/pull/481
.. _#482: https://github.com/kinverarity1/lasio/pull/482
.. _#483: https://github.com/kinverarity1/lasio/issues/483
.. _#484: https://github.com/kinverarity1/lasio/pull/484
.. _#485: https://github.com/kinverarity1/lasio/pull/485
.. _#486: https://github.com/kinverarity1/lasio/issues/486
.. _#487: https://github.com/kinverarity1/lasio/pull/487
.. _#489: https://github.com/kinverarity1/lasio/pull/489
.. _#490: https://github.com/kinverarity1/lasio/issues/490
.. _#491: https://github.com/kinverarity1/lasio/pull/491
.. _#495: https://github.com/kinverarity1/lasio/pull/495
.. _#498: https://github.com/kinverarity1/lasio/pull/498
.. _#500: https://github.com/kinverarity1/lasio/pull/500
.. _#501: https://github.com/kinverarity1/lasio/pull/501
.. _#502: https://github.com/kinverarity1/lasio/issues/502
.. _#503: https://github.com/kinverarity1/lasio/pull/503
.. _#168: https://github.com/kinverarity1/lasio/issues/168
.. _#221: https://github.com/kinverarity1/lasio/issues/221
.. _#225: https://github.com/kinverarity1/lasio/issues/225
.. _#239: https://github.com/kinverarity1/lasio/issues/239
.. _#249: https://github.com/kinverarity1/lasio/issues/249
.. _#252: https://github.com/kinverarity1/lasio/issues/252
.. _#258: https://github.com/kinverarity1/lasio/issues/258
.. _#286: https://github.com/kinverarity1/lasio/issues/286
.. _#292: https://github.com/kinverarity1/lasio/issues/292
.. _#293: https://github.com/kinverarity1/lasio/issues/293
.. _#296: https://github.com/kinverarity1/lasio/issues/296
.. _#298: https://github.com/kinverarity1/lasio/issues/298
.. _#300: https://github.com/kinverarity1/lasio/issues/300
.. _#302: https://github.com/kinverarity1/lasio/issues/302
.. _#311: https://github.com/kinverarity1/lasio/issues/311
.. _#317: https://github.com/kinverarity1/lasio/issues/317
.. _#318: https://github.com/kinverarity1/lasio/issues/318
.. _#325: https://github.com/kinverarity1/lasio/issues/325
.. _#326: https://github.com/kinverarity1/lasio/issues/326
.. _#327: https://github.com/kinverarity1/lasio/issues/327
.. _#328: https://github.com/kinverarity1/lasio/issues/328
.. _#329: https://github.com/kinverarity1/lasio/issues/329
.. _#330: https://github.com/kinverarity1/lasio/issues/330
.. _#331: https://github.com/kinverarity1/lasio/issues/331
.. _#334: https://github.com/kinverarity1/lasio/issues/334
.. _#335: https://github.com/kinverarity1/lasio/issues/335
.. _#337: https://github.com/kinverarity1/lasio/issues/337
.. _#338: https://github.com/kinverarity1/lasio/issues/338
.. _#340: https://github.com/kinverarity1/lasio/issues/340
.. _#341: https://github.com/kinverarity1/lasio/issues/341
.. _#342: https://github.com/kinverarity1/lasio/issues/342
.. _#345: https://github.com/kinverarity1/lasio/issues/345
.. _#346: https://github.com/kinverarity1/lasio/issues/346
.. _#347: https://github.com/kinverarity1/lasio/issues/347
.. _#348: https://github.com/kinverarity1/lasio/issues/348
.. _#349: https://github.com/kinverarity1/lasio/issues/349
.. _#352: https://github.com/kinverarity1/lasio/issues/352
.. _#353: https://github.com/kinverarity1/lasio/issues/353
.. _#355: https://github.com/kinverarity1/lasio/issues/355
.. _#358: https://github.com/kinverarity1/lasio/issues/358
.. _#360: https://github.com/kinverarity1/lasio/issues/360
.. _#361: https://github.com/kinverarity1/lasio/issues/361
.. _#367: https://github.com/kinverarity1/lasio/issues/367
.. _#368: https://github.com/kinverarity1/lasio/issues/368
.. _#369: https://github.com/kinverarity1/lasio/issues/369
.. _#372: https://github.com/kinverarity1/lasio/issues/372
.. _#374: https://github.com/kinverarity1/lasio/issues/374
.. _#382: https://github.com/kinverarity1/lasio/issues/382
.. _#385: https://github.com/kinverarity1/lasio/issues/385
.. _#387: https://github.com/kinverarity1/lasio/issues/387
.. _#390: https://github.com/kinverarity1/lasio/issues/390
.. _#391: https://github.com/kinverarity1/lasio/issues/391
.. _#393: https://github.com/kinverarity1/lasio/issues/393
.. _#396: https://github.com/kinverarity1/lasio/issues/396
.. _#397: https://github.com/kinverarity1/lasio/issues/397
.. _#398: https://github.com/kinverarity1/lasio/issues/398
.. _#399: https://github.com/kinverarity1/lasio/issues/399
.. _#400: https://github.com/kinverarity1/lasio/issues/400
.. _#401: https://github.com/kinverarity1/lasio/issues/401
.. _#403: https://github.com/kinverarity1/lasio/issues/403
.. _#406: https://github.com/kinverarity1/lasio/issues/406
.. _#410: https://github.com/kinverarity1/lasio/issues/410
.. _#411: https://github.com/kinverarity1/lasio/issues/411
.. _#418: https://github.com/kinverarity1/lasio/issues/418
.. _#420: https://github.com/kinverarity1/lasio/issues/420
.. _#423: https://github.com/kinverarity1/lasio/issues/423
.. _#425: https://github.com/kinverarity1/lasio/issues/425
.. _#428: https://github.com/kinverarity1/lasio/issues/428
.. _#429: https://github.com/kinverarity1/lasio/issues/429
.. _#430: https://github.com/kinverarity1/lasio/issues/430
.. _#432: https://github.com/kinverarity1/lasio/issues/432
.. _#437: https://github.com/kinverarity1/lasio/issues/437
.. _#438: https://github.com/kinverarity1/lasio/issues/438
.. _#441: https://github.com/kinverarity1/lasio/issues/441
.. _#447: https://github.com/kinverarity1/lasio/issues/447
.. _#449: https://github.com/kinverarity1/lasio/issues/449
.. _#451: https://github.com/kinverarity1/lasio/issues/451
.. _#452: https://github.com/kinverarity1/lasio/issues/452
.. _#455: https://github.com/kinverarity1/lasio/issues/455
.. _#459: https://github.com/kinverarity1/lasio/issues/459
.. _#460: https://github.com/kinverarity1/lasio/issues/460
.. _#461: https://github.com/kinverarity1/lasio/issues/461
.. _#465: https://github.com/kinverarity1/lasio/issues/465
.. _#466: https://github.com/kinverarity1/lasio/issues/466
.. _#469: https://github.com/kinverarity1/lasio/issues/469
.. _#470: https://github.com/kinverarity1/lasio/issues/470
.. _#471: https://github.com/kinverarity1/lasio/issues/471
.. _#475: https://github.com/kinverarity1/lasio/issues/475
.. _#479: https://github.com/kinverarity1/lasio/issues/479
.. _#480: https://github.com/kinverarity1/lasio/issues/480
.. _#481: https://github.com/kinverarity1/lasio/issues/481
.. _#482: https://github.com/kinverarity1/lasio/issues/482
.. _#484: https://github.com/kinverarity1/lasio/issues/484
.. _#485: https://github.com/kinverarity1/lasio/issues/485
.. _#487: https://github.com/kinverarity1/lasio/issues/487
.. _#489: https://github.com/kinverarity1/lasio/issues/489
.. _#491: https://github.com/kinverarity1/lasio/issues/491
.. _#495: https://github.com/kinverarity1/lasio/issues/495
.. _#498: https://github.com/kinverarity1/lasio/issues/498
.. _#500: https://github.com/kinverarity1/lasio/issues/500
.. _#501: https://github.com/kinverarity1/lasio/issues/501
.. _#503: https://github.com/kinverarity1/lasio/issues/503
.. _#530: https://github.com/kinverarity1/lasio/issues/530
.. _#552: https://github.com/kinverarity1/lasio/issues/552
.. _#554: https://github.com/kinverarity1/lasio/issues/554
.. _#555: https://github.com/kinverarity1/lasio/issues/555
.. _#556: https://github.com/kinverarity1/lasio/issues/556
