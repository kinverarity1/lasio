import logging
import textwrap

import numpy as np

from .las_items import HeaderItem, CurveItem, SectionItems, OrderedDict
from . import defaults
from . import exceptions

logger = logging.getLogger(__name__)


def write(
    las,
    file_object,
    version=None,
    wrap=None,
    STRT=None,
    STOP=None,
    STEP=None,
    fmt="%.5f",
    len_numeric_field=None,
    data_width=79,
    header_width=60,
):
    """Write a LAS files.

    Arguments:
        las (:class:`lasio.las.LASFile`)
        file_object (file-like object open for writing): output
        version (float or None): version of written file, either 1.2 or 2.
            If this is None, ``las.version.VERS.value`` will be used.
        wrap (bool or None): whether to wrap the output data section.
            If this is None, ``las.version.WRAP.value`` will be used.
        STRT (float or None): value to use as STRT (note the data will not
            be clipped). If this is None, the data value in the first column,
            first row will be used.
        STOP (float or None): value to use as STOP (note the data will not
            be clipped). If this is None, the data value in the first column,
            last row will be used.
        STEP (float or None): value to use as STEP (note the data will not
            be resampled and/or interpolated). If this is None, the STEP will
            be estimated from the first two rows of the first column.
        fmt (str): Python string formatting operator for numeric data to be
            used.
        len_numeric_field (int): width of each numeric field column (must be
            greater than than all the formatted numeric values in the file).
        data_width (79): width of data field in characters

    Creating an output file is not the only side-effect of this function. It
    will also modify the STRT, STOP and STEP HeaderItems so that they correctly
    reflect the ~Data section's units and the actual first, last, and interval
    values.

    You should avoid calling this function directly - instead use the
    :meth:`lasio.las.LASFile.write` method.

    """
    if wrap is None:
        wrap = las.version["WRAP"] == "YES"
    elif wrap is True:
        las.version["WRAP"] = HeaderItem(
            "WRAP", "", "YES", "Multiple lines per depth step"
        )
    elif wrap is False:
        las.version["WRAP"] = HeaderItem("WRAP", "", "NO", "One line per depth step")
    lines = []

    assert version in (1.2, 2, None)
    if version is None:
        version = las.version["VERS"].value
    if version == 1.2:
        las.version["VERS"] = HeaderItem(
            "VERS", "", 1.2, "CWLS LOG ASCII STANDARD - VERSION 1.2"
        )
    elif version == 2:
        las.version["VERS"] = HeaderItem(
            "VERS", "", 2.0, "CWLS log ASCII Standard -VERSION 2.0"
        )

    if STRT is None:
        STRT = las.index[0]
    if STOP is None:
        STOP = las.index[-1]
    if STEP is None:
        if STOP != STRT: #prevents an error being thrown in the case of only a single sample being written
            STEP = las.index[1] - las.index[0]  # Faster than np.gradient

    las.well["STRT"].value = STRT
    las.well["STOP"].value = STOP
    las.well["STEP"].value = STEP

    # Check units
    if las.curves[0].unit:
        unit = las.curves[0].unit
    else:
        unit = las.well["STRT"].unit
    las.well["STRT"].unit = unit
    las.well["STOP"].unit = unit
    las.well["STEP"].unit = unit
    las.curves[0].unit = unit

    # Write each section.
    # get_formatter_function ( ** get_section_widths )

    # ~Version
    logger.debug("LASFile.write Version section")
    lines.append("~Version ".ljust(header_width, "-"))
    order_func = get_section_order_function("Version", version)
    section_widths = get_section_widths("Version", las.version, version, order_func)
    for header_item in las.version.values():
        mnemonic = header_item.original_mnemonic
        # logger.debug('LASFile.write ' + str(header_item))
        order = order_func(mnemonic)
        # logger.debug('LASFile.write order = %s' % (order, ))
        logger.debug(
            "LASFile.write %s order=%s section_widths=%s"
            % (header_item, order, section_widths)
        )
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Well
    logger.debug("LASFile.write Well section")
    lines.append("~Well ".ljust(header_width, "-"))
    order_func = get_section_order_function("Well", version)
    section_widths = get_section_widths("Well", las.well, version, order_func)
    # logger.debug('LASFile.write well section_widths=%s' % section_widths)
    for header_item in las.well.values():
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        logger.debug(
            "LASFile.write %s order=%s section_widths=%s"
            % (header_item, order, section_widths)
        )
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Curves
    logger.debug("LASFile.write Curves section")
    lines.append("~Curve Information ".ljust(header_width, "-"))
    order_func = get_section_order_function("Curves", version)
    section_widths = get_section_widths("Curves", las.curves, version, order_func)
    for header_item in las.curves:
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Params
    logger.debug("LASFile.write Params section")
    lines.append("~Params ".ljust(header_width, "-"))
    order_func = get_section_order_function("Parameter", version)
    section_widths = get_section_widths("Parameter", las.params, version, order_func)
    for header_item in las.params.values():
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Other
    logger.debug("LASFile.write Other section")
    lines.append("~Other ".ljust(header_width, "-"))
    lines += las.other.splitlines()

    logger.debug("LASFile.write ASCII section")
    lines.append("~ASCII ".ljust(header_width, "-"))

    file_object.write("\n".join(lines))
    file_object.write("\n")
    line_counter = len(lines)

    # data_arr = np.column_stack([c.data for c in las.curves])
    data_arr = las.data
    nrows, ncols = data_arr.shape
    logger.debug("Data section shape: {}".format((nrows, ncols)))

    logger.debug("len_numeric_field = {}".format(len_numeric_field))
    if len_numeric_field is None:
        logger.debug("Calculating len_numeric_field. fmt = {}".format(fmt))
        len_numeric_field = 10
        test_fmt = fmt % np.pi
        while len(test_fmt) > (len_numeric_field - 1):
            logger.debug("test_fmt = {}".format(test_fmt))
            len_numeric_field += 1

    def format_data_section_line(n, fmt, l=len_numeric_field, spacer=" "):
        try:
            if np.isnan(n):
                return spacer + str(las.well["NULL"].value).rjust(l)
            else:
                return spacer + (fmt % n).rjust(l)
        except TypeError:
            return spacer + str(n).rjust(l)

    twrapper = textwrap.TextWrapper(width=data_width)

    for i in range(nrows):
        logger.debug("Writing data array row {} of {}".format(i + 1, nrows))
        depth_slice = ""
        for j in range(ncols):
            depth_slice += format_data_section_line(data_arr[i, j], fmt)

        if wrap:
            lines = twrapper.wrap(depth_slice)
            logger.debug(
                "LASFile.write Wrapped %d lines out of %s" % (len(lines), depth_slice)
            )
        else:
            lines = [depth_slice]

        for line in lines:
            if las.version["VERS"].value == 1.2 and len(line) > 255:
                logger.warning(
                    "[v1.2] line #{} has {} chars (>256)".format(
                        line_counter + 1, len(line)
                    )
                )
            file_object.write(line + "\n")
            line_counter += 1


def get_formatter_function(order, left_width=None, middle_width=None):
    """Create function to format a LAS header item for output.

    Arguments:
        order: format of item, either 'descr:value' or 'value:descr'

    Keyword Arguments:
        left_width (int): number of characters to the left hand side of the
            first period
        middle_width (int): total number of characters minus 1 between the
            first period from the left and the first colon from the left.

    Returns:
        A function which takes a header item
        (e.g. :class:`lasio.las_items.HeaderItem`) as its single argument and
        which in turn returns a string which is the correctly formatted LAS
        header line.

    """
    if left_width is None:
        left_width = 10
    if middle_width is None:
        middle_width = 40
    mnemonic_func = lambda mnemonic: mnemonic.ljust(left_width)
    middle_func = lambda unit, right_hand_item: (
        unit
        + " " * (middle_width - len(str(unit)) - len(right_hand_item))
        + right_hand_item
    )
    if order == "descr:value":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.descr)),
            item.value,
        )
    elif order == "value:descr":
        return lambda item: "%s.%s : %s" % (
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.value)),
            item.descr,
        )


def get_section_order_function(
    section, version, order_definitions=defaults.ORDER_DEFINITIONS
):
    """Get a function that returns the order per the mnemonic and section.

    Arguments:
        section (str): either 'well', 'params', 'curves', 'version'
        version (float): either 1.2 and 2.0

    Keyword Arguments:
        order_definitions (dict): see source of defaults.py for more information

    Returns:
        A function which takes a mnemonic (str) as its only argument, and
        in turn returns the order 'value:descr' or 'descr:value'.

    """
    section_orders = order_definitions[version][section]
    default_order = section_orders[0]
    orders = {}
    for order, mnemonics in section_orders[1:]:
        for mnemonic in mnemonics:
            orders[mnemonic] = order
    return lambda mnemonic: orders.get(mnemonic, default_order)


def get_section_widths(section_name, items, version, order_func):
    """Find minimum section widths fitting the content in *items*.

    Arguments:
        section_name (str): either 'version', 'well', 'curves', or 'params'
        items (SectionItems): section items
        version (float): either 1.2 or 2.0
        order_func (func): see :func:`lasio.writer.get_section_order_function`

    """
    section_widths = {"left_width": None, "middle_width": None}
    if len(items) > 0:
        section_widths["left_width"] = max([len(i.original_mnemonic) for i in items])
        middle_widths = []
        for i in items:
            order = order_func(i.mnemonic)
            rhs_element = order.split(":")[0]
            logger.debug(
                "get_section_widths %s\n\torder=%s rhs_element=%s"
                % (i, order, rhs_element)
            )
            middle_widths.append(len(str(i.unit)) + 1 + len(str(i[rhs_element])))
        section_widths["middle_width"] = max(middle_widths)
    return section_widths
