Installation
============

|Python versions| |PyPI version| |PyPI format|

``lasio`` is written to be compatible with Python 2.6+, and 3.2+. The best
way to install is using ``pip``.

.. code-block:: doscon

    (test) C:\Users\kent>pip install lasio
    Collecting lasio
      Using cached lasio-0.13-py2.py3-none-any.whl
    Collecting numpy (from lasio)
      Downloading numpy-1.13.3-cp36-none-win_amd64.whl (13.1MB)
        100% |████████████████████████████████| 13.1MB 64kB/s
    Collecting ordereddict (from lasio)
      Using cached ordereddict-1.1.tar.gz
    Building wheels for collected packages: ordereddict
      Running setup.py bdist_wheel for ordereddict ... done
      Stored in directory: C:\Users\kent\AppData\Local\pip\Cache\wheels\cf\2c\b5\a1bfd8848f7861c1588f1a2dfe88c11cf3ab5073ab7
    af08bc9
    Successfully built ordereddict
    Installing collected packages: numpy, ordereddict, lasio
    Successfully installed lasio-0.13 numpy-1.13.3 ordereddict-1.1

This will download and install lasio’s dependencies (`numpy`_ and
`ordereddict`_). 

There are some other packages which lasio will use to
provide extra functionality if they are installed (`pandas`_,
`cChardet`_ and/or `chardet`_, `openpyxl`_, and `argparse`_). I
recommend installing these too with:

.. code-block:: doscon

    (test) C:\Users\kent\Code\lasio>pip install -r optional-packages.txt
    Collecting pandas (from -r optional-packages.txt (line 1))
      Using cached pandas-0.21.0-cp36-cp36m-win_amd64.whl
    Collecting cchardet (from -r optional-packages.txt (line 2))
      Using cached cchardet-2.1.1-cp36-cp36m-win_amd64.whl
    Collecting chardet (from -r optional-packages.txt (line 3))
      Using cached chardet-3.0.4-py2.py3-none-any.whl
    Collecting openpyxl (from -r optional-packages.txt (line 4))
      Using cached openpyxl-2.4.9.tar.gz
    Collecting argparse (from -r optional-packages.txt (line 5))
      Using cached argparse-1.4.0-py2.py3-none-any.whl
    Collecting python-dateutil>=2 (from pandas->-r optional-packages.txt (line 1))
      Using cached python_dateutil-2.6.1-py2.py3-none-any.whl
    Collecting pytz>=2011k (from pandas->-r optional-packages.txt (line 1))
      Using cached pytz-2017.3-py2.py3-none-any.whl
    Requirement already satisfied: numpy>=1.9.0 in c:\users\kent\miniconda3\envs\test\lib\site-packages (from pandas->-r opt
    ional-packages.txt (line 1))
    Collecting jdcal (from openpyxl->-r optional-packages.txt (line 4))
      Using cached jdcal-1.3.tar.gz
    Collecting et_xmlfile (from openpyxl->-r optional-packages.txt (line 4))
      Using cached et_xmlfile-1.0.1.tar.gz
    Collecting six>=1.5 (from python-dateutil>=2->pandas->-r optional-packages.txt (line 1))
      Using cached six-1.11.0-py2.py3-none-any.whl
    Building wheels for collected packages: openpyxl, jdcal, et-xmlfile
      Running setup.py bdist_wheel for openpyxl ... done
      Stored in directory: C:\Users\kent\AppData\Local\pip\Cache\wheels\8d\ae\96\0b8e7890053c46c22b48d021d104b00e5544c3aedd6
    41749e1
      Running setup.py bdist_wheel for jdcal ... done
      Stored in directory: C:\Users\kent\AppData\Local\pip\Cache\wheels\0f\63\92\19ac65ed64189de4d662f269d39dd08a887258842ad
    2f29549
      Running setup.py bdist_wheel for et-xmlfile ... done
      Stored in directory: C:\Users\kent\AppData\Local\pip\Cache\wheels\99\f6\53\5e18f3ff4ce36c990fa90ebdf2b80cd9b44dc461f75
    0a1a77c
    Successfully built openpyxl jdcal et-xmlfile
    Installing collected packages: six, python-dateutil, pytz, pandas, cchardet, chardet, jdcal, et-xmlfile, openpyxl, argpa
    rse
    Successfully installed argparse-1.4.0 cchardet-2.1.1 chardet-3.0.4 et-xmlfile-1.0.1 jdcal-1.3 openpyxl-2.4.9 pandas-0.21
    .0 python-dateutil-2.6.1 pytz-2017.3 six-1.11.0

``lasio`` is now installed. See the following pages for examples of how to use the package.

To upgrade to the latest PyPI version, use:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>pip install --upgrade lasio
    Requirement already up-to-date: lasio in c:\users\kent\code\testing\lasio
    Requirement already up-to-date: numpy in c:\users\kent\miniconda3\envs\test2\lib\site-packages (from lasio)
    Requirement already up-to-date: ordereddict in c:\users\kent\miniconda3\envs\test2\lib\site-packages (from lasio)

Development version
-------------------

Installing via pip gets the latest release which has been published on `PyPI <https://pypi.python.org/pypi/lasio/>`__.

The source code for lasio is kept at:

`https://github.com/kinverarity/lasio <https://github.com/kinverarity/lasio>`__

Updates are made much more frequently to the ``master`` branch here. If you have
Git installed, you can keep up to date with these changes:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing>git clone https://github.com/kinverarity1/lasio
    Cloning into 'lasio'...
    remote: Counting objects: 2494, done.
    remote: Compressing objects: 100% (91/91), done.
    Receiving objects:  98% (2445/2494), 1.93 MiB | remote: Total 2494 (delta 92), reused 124 (delta 69), pack-reused 233251
                                                     15.00 KiB/s, done.

    Resolving deltas: 100% (1542/1542), done.

    (test2) C:\Users\kent\Code\testing>cd lasio

    (test2) C:\Users\kent\Code\testing\lasio>pip install -r requirements.txt
    Collecting numpy (from -r requirements.txt (line 1))
      Using cached numpy-1.13.3-cp36-none-win_amd64.whl
    Collecting ordereddict (from -r requirements.txt (line 2))
    Installing collected packages: numpy, ordereddict
    Successfully installed numpy-1.13.3 ordereddict-1.1

    (test2) C:\Users\kent\Code\testing\lasio>python setup.py develop
    warning: pypandoc module not found, could not convert Markdown to RST
    running develop
    running egg_info
    creating lasio.egg-info
    writing lasio.egg-info\PKG-INFO
    writing dependency_links to lasio.egg-info\dependency_links.txt
    writing entry points to lasio.egg-info\entry_points.txt
    writing requirements to lasio.egg-info\requires.txt
    writing top-level names to lasio.egg-info\top_level.txt
    writing manifest file 'lasio.egg-info\SOURCES.txt'
    reading manifest file 'lasio.egg-info\SOURCES.txt'
    writing manifest file 'lasio.egg-info\SOURCES.txt'
    running build_ext
    Creating c:\users\kent\miniconda3\envs\test2\lib\site-packages\lasio.egg-link (link to .)
    Adding lasio 0.13 to easy-install.pth file
    Installing las2excel-script.py script to C:\Users\kent\Miniconda3\envs\test2\Scripts
    Installing las2excel.exe script to C:\Users\kent\Miniconda3\envs\test2\Scripts
    Installing las2excelbulk-script.py script to C:\Users\kent\Miniconda3\envs\test2\Scripts
    Installing las2excelbulk.exe script to C:\Users\kent\Miniconda3\envs\test2\Scripts
    Installing lasio-script.py script to C:\Users\kent\Miniconda3\envs\test2\Scripts
    Installing lasio.exe script to C:\Users\kent\Miniconda3\envs\test2\Scripts

    Installed c:\users\kent\code\testing\lasio
    Processing dependencies for lasio==0.13
    Searching for ordereddict==1.1
    Best match: ordereddict 1.1
    Adding ordereddict 1.1 to easy-install.pth file

    Using c:\users\kent\miniconda3\envs\test2\lib\site-packages
    Searching for numpy==1.13.3
    Best match: numpy 1.13.3
    Adding numpy 1.13.3 to easy-install.pth file

    Using c:\users\kent\miniconda3\envs\test2\lib\site-packages
    Finished processing dependencies for lasio==0.13

    (test2) C:\Users\kent\Code\testing\lasio>

To update your version with the latest changes on GitHub:

.. code-block:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>git pull origin master
    From https://github.com/kinverarity1/lasio
     * branch            master     -> FETCH_HEAD
    Updating 760a929..857f455
    Fast-forward
     .gitignore                                         |   6 +
     CONTRIBUTING.md                                    |   4 +-
     README.md                                          |  21 +-
     docs/requirements.txt                              |   2 +
     docs/source/basic-example.rst                      | 240 +++++++++++++
     docs/source/conf.py                                |   9 +-
     docs/source/excel.rst                              | 269 ++++++++++++++
     docs/source/figures/excel_curves.png               | Bin 0 -> 20048 bytes
     docs/source/figures/excel_header.png               | Bin 0 -> 58575 bytes
     docs/source/figures/pandas_gamn_hist.png           | Bin 0 -> 6879 bytes
     docs/source/figures/tutorial1.png                  | Bin 0 -> 18045 bytes
     docs/source/index.rst                              |  42 +--
     docs/source/lasio.rst                              |  61 ++--
     docs/source/modules.rst                            |   7 -
     docs/source/pandas.rst                             | 176 ++++++++++
     docs/source/writing.rst                            | 380 ++++++++++++++++++++
     docs/v0.10_changelog.txt                           | Bin 26562 -> 0 bytes
     lasio/__init__.py                                  |  26 +-
     lasio/defaults.py                                  |   8 +-
     lasio/excel.py                                     |  63 +++-
     lasio/las.py                                       | 385 +++++++++++++++------
     lasio/las_items.py                                 | 164 +++++++--
     lasio/reader.py                                    | 296 ++++++++++------
     lasio/writer.py                                    |  61 +++-
     requirements.txt                                   |   1 -
     sample.xlsx                                        | Bin 0 -> 6647 bytes
     setup.py                                           |  21 +-
     ...ended_chars_cp1252.las => encodings_cp1252.las} |   0
     ...d_chars_iso88591.las => encodings_iso88591.las} |   0
     ...ded_chars_utf16be.las => encodings_utf16be.las} | Bin
     ...ars_utf16bebom.las => encodings_utf16bebom.las} | Bin
     ...ded_chars_utf16le.las => encodings_utf16le.las} | Bin
     ...ars_utf16lebom.las => encodings_utf16lebom.las} | Bin
     ..._extended_chars_utf8.las => encodings_utf8.las} |   0
     ...d_chars_utf8wbom.las => encodings_utf8wbom.las} |   0
     tests/examples/missing_null.las                    |  45 +++
     tests/examples/missing_vers.las                    |  45 +++
     tests/examples/missing_wrap.las                    |  45 +++
     tests/test_encoding.py                             |  57 +--
     tests/test_read.py                                 |  38 ++
     tests/test_write.py                                |  13 +
     41 files changed, 2076 insertions(+), 409 deletions(-)
     create mode 100644 docs/requirements.txt
     create mode 100644 docs/source/basic-example.rst
     create mode 100644 docs/source/excel.rst
     create mode 100644 docs/source/figures/excel_curves.png
     create mode 100644 docs/source/figures/excel_header.png
     create mode 100644 docs/source/figures/pandas_gamn_hist.png
     create mode 100644 docs/source/figures/tutorial1.png
     delete mode 100644 docs/source/modules.rst
     create mode 100644 docs/source/pandas.rst
     create mode 100644 docs/source/writing.rst
     delete mode 100644 docs/v0.10_changelog.txt
     create mode 100644 sample.xlsx
     rename tests/examples/{sample_extended_chars_cp1252.las => encodings_cp1252.las} (100%)
     rename tests/examples/{sample_extended_chars_iso88591.las => encodings_iso88591.las} (100%)
     rename tests/examples/{sample_extended_chars_utf16be.las => encodings_utf16be.las} (100%)
     rename tests/examples/{sample_extended_chars_utf16bebom.las => encodings_utf16bebom.las} (100%)
     rename tests/examples/{sample_extended_chars_utf16le.las => encodings_utf16le.las} (100%)
     rename tests/examples/{sample_extended_chars_utf16lebom.las => encodings_utf16lebom.las} (100%)
     rename tests/examples/{sample_extended_chars_utf8.las => encodings_utf8.las} (100%)
     rename tests/examples/{sample_extended_chars_utf8wbom.las => encodings_utf8wbom.las} (100%)
     create mode 100644 tests/examples/missing_null.las
     create mode 100644 tests/examples/missing_vers.las
     create mode 100644 tests/examples/missing_wrap.las

    (test2) C:\Users\kent\Code\testing\lasio>

.. _numpy: http://numpy.org/
.. _ordereddict: https://pypi.python.org/pypi/ordereddict
.. _pandas: https://pypi.python.org/pypi/pandas
.. _cChardet: https://github.com/PyYoshi/cChardet
.. _chardet: https://github.com/chardet/chardet
.. _openpyxl: https://openpyxl.readthedocs.io/en/default/
.. _argparse: https://github.com/ThomasWaldmann/argparse/

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/lasio.svg
   :target: https://www.python.org/downloads/
.. |PyPI version| image:: http://img.shields.io/pypi/v/lasio.svg
   :target: https://pypi.python.org/pypi/lasio/
.. |PyPI format| image:: https://img.shields.io/pypi/format/lasio.svg
   :target: https://pypi.python.org/pypi/lasio

Testing
-------

|Build Status|

Every time ``lasio`` is updated, all the automated tests are run at `Travis
CI`_ against Python versions 2.7, 3.3, 3.4, 3.5, and 3.6. ``lasio`` should
also work on Python 2.6 and 3.2, but these are tested only
occassionally.

To run tests yourself, first install the testing framework and all the
optional packages:

.. code:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>pip install pytest
    Collecting pytest
      Downloading pytest-3.2.3-py2.py3-none-any.whl (187kB)
        100% |████████████████████████████████| 194kB 937kB/s
    Collecting py>=1.4.33 (from pytest)
      Downloading py-1.4.34-py2.py3-none-any.whl (84kB)
        100% |████████████████████████████████| 92kB 1.2MB/s
    Requirement already satisfied: setuptools in c:\users\kent\miniconda3\envs\test2\lib\site-packages (from pytest)
    Collecting colorama; sys_platform == "win32" (from pytest)
      Downloading colorama-0.3.9-py2.py3-none-any.whl
    Installing collected packages: py, colorama, pytest
    Successfully installed colorama-0.3.9 py-1.4.34 pytest-3.2.3

    (test2) C:\Users\kent\Code\testing\lasio>pip install -r optional-packages.txt
    Collecting pandas (from -r optional-packages.txt (line 1))
      Using cached pandas-0.21.0-cp36-cp36m-win_amd64.whl
    Collecting cchardet (from -r optional-packages.txt (line 2))
      Using cached cchardet-2.1.1-cp36-cp36m-win_amd64.whl
    Collecting chardet (from -r optional-packages.txt (line 3))
      Using cached chardet-3.0.4-py2.py3-none-any.whl
    Collecting openpyxl (from -r optional-packages.txt (line 4))
    Collecting argparse (from -r optional-packages.txt (line 5))
      Using cached argparse-1.4.0-py2.py3-none-any.whl
    Requirement already satisfied: numpy>=1.9.0 in c:\users\kent\miniconda3\envs\test2\lib\site-packages (from pandas->-r op
    tional-packages.txt (line 1))
    Collecting python-dateutil>=2 (from pandas->-r optional-packages.txt (line 1))
      Using cached python_dateutil-2.6.1-py2.py3-none-any.whl
    Collecting pytz>=2011k (from pandas->-r optional-packages.txt (line 1))
      Using cached pytz-2017.3-py2.py3-none-any.whl
    Collecting jdcal (from openpyxl->-r optional-packages.txt (line 4))
    Collecting et-xmlfile (from openpyxl->-r optional-packages.txt (line 4))
    Collecting six>=1.5 (from python-dateutil>=2->pandas->-r optional-packages.txt (line 1))
      Using cached six-1.11.0-py2.py3-none-any.whl
    Installing collected packages: six, python-dateutil, pytz, pandas, cchardet, chardet, jdcal, et-xmlfile, openpyxl, argpa
    rse
    Successfully installed argparse-1.4.0 cchardet-2.1.1 chardet-3.0.4 et-xmlfile-1.0.1 jdcal-1.3 openpyxl-2.4.9 pandas-0.21
    .0 python-dateutil-2.6.1 pytz-2017.3 six-1.11.0

    (test2) C:\Users\kent\Code\testing\lasio>

And then run tests:

.. code:: doscon

    (test2) C:\Users\kent\Code\testing\lasio>py.test
    ============================= test session starts =============================
    platform win32 -- Python 3.6.2, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
    rootdir: C:\Users\kent\Code\testing\lasio, inifile:
    collected 88 items

    tests\test_add_curve.py .
    tests\test_api.py .......
    tests\test_delete_curve.py .
    tests\test_encoding.py .........
    tests\test_enhancements.py ...........
    tests\test_json.py ...
    tests\test_open_file.py .....
    tests\test_read.py ..................................
    tests\test_rename_curve.py .
    tests\test_serialization.py .
    tests\test_wrapped.py ...
    tests\test_write.py ............

    ========================== 88 passed in 7.07 seconds ==========================

    (test2) C:\Users\kent\Code\testing\lasio>

.. _Travis CI: https://travis-ci.org/kinverarity1/lasio

.. |Build Status| image:: https://travis-ci.org/kinverarity1/lasio.svg?branch=master
   :target: https://travis-ci.org/kinverarity1/lasio