import logging
import os

# Convoluted import for StringIO in order to support:
#
# - Python 3 - io.StringIO
# - Python 2 (optimized) - cStringIO.StringIO
# - Python 2 (all) - StringIO.StringIO

try:
    import cStringIO as StringIO
except ImportError:
    try:  # cStringIO not available on this system
        import StringIO
    except ImportError:  # Python 3
        from io import StringIO
    else:
        from StringIO import StringIO
else:
    from StringIO import StringIO

from .las import LASFile


logger = logging.getLogger(__name__)


def open(filename, **kwargs):
    """Open an example LAS file from lasio's test suite.

    Args:
        filename (str): forward-slash separated filename of a LAS file from
            lasio's test suite, starting from the "tests/examples" subfolder
            e.g. "1001178549.las" or "2.0/sample_2.0.las"

    Other keyword arguments are passed to `lasio.LASFile`. If lasio has been
    installed locally from source, then the local version of the example file
    will be opened. If lasio has not been installed from source then the LAS
    file will be downloaded from GitHub.

    Returns: LASFile object

    """
    local_path = get_local_examples_path()
    if os.path.isdir(local_path):
        return open_local_example(filename, **kwargs)
    else:
        return open_github_example(filename, **kwargs)


def open_github_example(
    filename,
    url_prefix="https://raw.githubusercontent.com/kinverarity1/lasio/master/tests/examples/",
    **kwargs
):
    """Open an example LAS file from lasio's test suite on GitHub

    Args:
        filename (str): forward-slash separated filename of a LAS file from
            lasio's test suite, starting from the "tests/examples" subfolder
            e.g. "1001178549.las" or "2.0/sample_2.0.las"

    Other keyword arguments are passed to `lasio.LASFile`.

    Returns: LASFile object

    """
    url = url_prefix + filename
    try:
        import urllib2

        response = urllib2.urlopen(url)
        encoding = response.headers.getparam("charset")
        file_ref = StringIO(response.read())
        logger.debug("Retrieved data had encoding {}".format(encoding))
    except ImportError:
        import urllib.request

        response = urllib.request.urlopen(url)
        if response.headers.get_content_charset() is None:
            if "encoding" in encoding_kwargs:
                encoding = encoding_kwargs["encoding"]
            else:
                encoding = "utf-8"
        else:
            encoding = response.headers.get_content_charset()
        # newline=None causes StringIO to use universal-newline:
        # Lines in the input can end in '\n', '\r', or '\r\n', and these are
        # translated into '\n' before being returned to the caller.
        file_ref = StringIO(response.read().decode(encoding), newline=None)
    return LASFile(file_ref, **kwargs)


def open_local_example(filename, **kwargs):
    """Open an example LAS file from lasio's test suite.

    Args:
        filename (str): forward-slash separated filename of a LAS file from
            lasio's test suite, starting from the "tests/examples" subfolder
            e.g. "1001178549.las" or "2.0/sample_2.0.las"

    Other keyword arguments are passed to `lasio.LASFile`. If lasio has not been
    installed from source then an exception will be raised.

    Returns: LASFile object

    """
    examples_path = get_local_examples_path()
    return LASFile(os.path.join(examples_path, *filename.split("/")), **kwargs)


def get_local_examples_path():
    """Return the path to the examples from lasio's test suite, if it is
    installed locally.

    Returns: path as str.

    """
    import lasio

    return os.path.join(
        os.path.dirname(os.path.dirname(lasio.__file__)), "tests", "examples"
    )
