import codecs

from . import read

# These tests seem to be pointless as they always pass... better ideas?

# def test_autodetect_cp437():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_cp437.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="cp437").read()

# def test_autodetect_utf8():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_utf8.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="utf8").read()

# def test_autodetect_win1252():
#     fn = r"D:\work\dewnr\logging_software\lasio\tests\examples\encoding_win1252.las"
#     l = lasio.read(fn, autodetect_encoding=True)
#     assert l._text == codecs.open(fn, mode="r", encoding="win1252").read()
