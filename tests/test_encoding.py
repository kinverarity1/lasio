import codecs

import las_reader

# These tests seem to be pointless as they always pass... better ideas?

# def test_autodetect_cp437():
#     fn = r"D:\work\dewnr\logging_software\las_reader\tests\examples\encoding_cp437.py"
#     l = las_reader.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="cp437").read()

# def test_autodetect_utf8():
#     fn = r"D:\work\dewnr\logging_software\las_reader\tests\examples\encoding_utf8.py"
#     l = las_reader.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="utf8").read()

# def test_autodetect_win1252():
#     fn = r"D:\work\dewnr\logging_software\las_reader\tests\examples\encoding_win1252.py"
#     l = las_reader.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="win1252").read()
