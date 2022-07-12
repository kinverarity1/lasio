Docstrings for the lasio package
================================

Reading LAS files
-----------------
.. autofunction:: lasio.read
.. autoclass:: lasio.LASFile
.. automethod:: lasio.LASFile.read
.. autofunction:: lasio.open_file
.. autofunction:: lasio.reader.open_with_codecs
.. autofunction:: lasio.reader.get_encoding
.. automethod:: lasio.LASFile.match_raw_section
.. autofunction:: lasio.reader.read_data_section_iterative_normal_engine
.. autofunction:: lasio.reader.read_data_section_iterative_numpy_engine
.. autofunction:: lasio.reader.get_substitutions
.. autoclass:: lasio.reader.SectionParser
.. autofunction:: lasio.reader.read_header_line
.. autoclass:: lasio.HeaderItem
.. automethod:: lasio.HeaderItem.set_session_mnemonic_only
.. autoclass:: lasio.CurveItem
.. autoclass:: lasio.SectionItems

Reading data
--------------
.. automethod:: lasio.LASFile.__getitem__
.. automethod:: lasio.LASFile.__setitem__
.. automethod:: lasio.LASFile.get_curve
.. automethod:: lasio.LASFile.keys
.. automethod:: lasio.LASFile.values
.. automethod:: lasio.LASFile.items
.. automethod:: lasio.LASFile.df
.. autoattribute:: lasio.LASFile.version
.. autoattribute:: lasio.LASFile.well
.. autoattribute:: lasio.LASFile.curves
.. autoattribute:: lasio.LASFile.curvesdict
.. autoattribute:: lasio.LASFile.params
.. autoattribute:: lasio.LASFile.other
.. autoattribute:: lasio.LASFile.index
.. autoattribute:: lasio.LASFile.depth_m
.. autoattribute:: lasio.LASFile.depth_ft
.. autoattribute:: lasio.LASFile.data
.. automethod:: lasio.LASFile.stack_curves

Reading and modifying header data
---------------------------------
.. autoclass:: lasio.SectionItems
    :members:

Modifying data
--------------
.. automethod:: lasio.LASFile.set_data
.. automethod:: lasio.LASFile.set_data_from_df
.. automethod:: lasio.LASFile.append_curve
.. automethod:: lasio.LASFile.insert_curve
.. automethod:: lasio.LASFile.delete_curve
.. automethod:: lasio.LASFile.append_curve_item
.. automethod:: lasio.LASFile.insert_curve_item
.. automethod:: lasio.LASFile.update_start_stop_step
.. automethod:: lasio.LASFile.update_units_from_index_curve

Writing data out
----------------
.. automethod:: lasio.LASFile.write
.. autofunction:: lasio.writer.write
.. autofunction:: lasio.writer.get_formatter_function
.. autofunction:: lasio.writer.get_section_order_function
.. autofunction:: lasio.writer.get_section_widths
.. automethod:: lasio.LASFile.to_csv
.. automethod:: lasio.LASFile.to_excel
.. autoclass:: lasio.excel.ExcelConverter
.. automethod:: lasio.excel.ExcelConverter.set_las
.. automethod:: lasio.excel.ExcelConverter.generate_workbook
.. automethod:: lasio.excel.ExcelConverter.write
.. automethod:: lasio.LASFile.to_json
.. autofunction:: lasio.convert_version.convert_version
.. autofunction:: lasio.convert_version.get_convert_version_parser

Defaults
--------
.. automodule:: lasio.defaults

Custom exceptions
-----------------
.. autoclass:: lasio.exceptions.LASDataError
.. autoclass:: lasio.exceptions.LASHeaderError
.. autoclass:: lasio.exceptions.LASUnknownUnitError

Test data
---------
.. autofunction:: lasio.examples.open
.. autofunction:: lasio.examples.open_github_example
.. autofunction:: lasio.examples.open_local_example
.. autofunction:: lasio.examples.get_local_examples_path

Logging
-------
.. autofunction:: lasio.add_logging_level
