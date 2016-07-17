import logging
import textwrap

import numpy as np

from .las_items import (
    HeaderItem, CurveItem, SectionItems, OrderedDict)
from . import defaults
from . import exceptions

logger = logging.getLogger(__name__)


def write(las, file_object, version=None, wrap=None, STRT=None,
          STOP=None, STEP=None, fmt='%10.5g'):
    if wrap is None:
        wrap = las.version['WRAP'] == 'YES'
    elif wrap is True:
        las.version['WRAP'] = HeaderItem(
            'WRAP', '', 'YES', 'Multiple lines per depth step')
    elif wrap is False:
        las.version['WRAP'] = HeaderItem(
            'WRAP', '', 'NO', 'One line per depth step')
    lines = []

    assert version in (1.2, 2, None)
    if version is None:
        version = las.version['VERS'].value
    if version == 1.2:
        las.version['VERS'] = HeaderItem(
            'VERS', '', 1.2, 'CWLS LOG ASCII STANDARD - VERSION 1.2')
    elif version == 2:
        las.version['VERS'] = HeaderItem(
            'VERS', '', 2.0, 'CWLS log ASCII Standard -VERSION 2.0')

    if STRT is None:
        STRT = las.index[0]
    if STOP is None:
        STOP = las.index[-1]
    if STEP is None:
        STEP = las.index[1] - las.index[0]  # Faster than np.gradient
    las.well['STRT'].value = STRT
    las.well['STOP'].value = STOP
    las.well['STEP'].value = STEP

    # Check units
    if las.curves[0].unit:
        unit = las.curves[0].unit
    else:
        unit = las.well['STRT'].unit
    las.well['STRT'].unit = unit
    las.well['STOP'].unit = unit
    las.well['STEP'].unit = unit
    las.curves[0].unit = unit

    # Check for any changes in the pandas dataframe and if there are,
    # create new curves so they are reflected in the output LAS file.

    # if las.use_pandas:
    #     curve_names = lambda: [ci.mnemonic for ci in las.curves]
    #     for df_curve_name in list(las.df.columns.values):
    #         if not df_curve_name in curve_names():
    #             las.add_curve(df_curve_name, las.df[df_curve_name])

    # Write each section.

    # ~Version
    logger.debug('LASFile.write Version section')
    lines.append('~Version '.ljust(60, '-'))
    order_func = get_section_order_function('Version', version)
    section_widths = get_section_widths(
        'Version', las.version, version, order_func)
    for header_item in las.version.values():
        mnemonic = header_item.original_mnemonic
        # logger.debug('LASFile.write ' + str(header_item))
        order = order_func(mnemonic)
        # logger.debug('LASFile.write order = %s' % (order, ))
        logger.debug('LASFile.write %s\norder=%s section_widths=%s' % (
            header_item, order, section_widths))
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Well
    logger.debug('LASFile.write Well section')
    lines.append('~Well '.ljust(60, '-'))
    order_func = get_section_order_function('Well', version)
    section_widths = get_section_widths(
        'Well', las.well, version, order_func)
    # logger.debug('LASFile.write well section_widths=%s' % section_widths)
    for header_item in las.well.values():
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        logger.debug('LASFile.write %s\norder=%s section_widths=%s' % (
            header_item, order, section_widths))
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Curves
    logger.debug('LASFile.write Curves section')
    lines.append('~Curves '.ljust(60, '-'))
    order_func = get_section_order_function('Curves', version)
    section_widths = get_section_widths(
        'Curves', las.curves, version, order_func)
    for header_item in las.curves:
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Params
    lines.append('~Params '.ljust(60, '-'))
    order_func = get_section_order_function('Parameter', version)
    section_widths = get_section_widths(
        'Parameter', las.params, version, order_func)
    for header_item in las.params.values():
        mnemonic = header_item.original_mnemonic
        order = order_func(mnemonic)
        formatter_func = get_formatter_function(order, **section_widths)
        line = formatter_func(header_item)
        lines.append(line)

    # ~Other
    lines.append('~Other '.ljust(60, '-'))
    lines += las.other.splitlines()

    lines.append('~ASCII '.ljust(60, '-'))

    file_object.write('\n'.join(lines))
    file_object.write('\n')

    # data_arr = np.column_stack([c.data for c in las.curves])
    data_arr = las.data
    nrows, ncols = data_arr.shape

    def format_data_section_line(n, fmt, l=10, spacer=' '):
        try:
            if np.isnan(n):
                return spacer + str(las.well['NULL'].value).rjust(l)
            else:
                return spacer + (fmt % n).rjust(l)
        except TypeError:
            return spacer + str(n).rjust(l)

    twrapper = textwrap.TextWrapper(width=79)
    for i in range(nrows):
        depth_slice = ''
        for j in range(ncols):
            depth_slice += format_data_section_line(data_arr[i, j], fmt)

        if wrap:
            lines = twrapper.wrap(depth_slice)
            logger.debug('LASFile.write Wrapped %d lines out of %s' %
                         (len(lines), depth_slice))
        else:
            lines = [depth_slice]

        if las.version['VERS'].value == 1.2:
            for line in lines:
                if len(line) > 255:
                    logger.warning(
                        'LASFile.write Data line > 256 chars: %s' % line)

        for line in lines:
            file_object.write(line + '\n')


def get_formatter_function(order, left_width=None, middle_width=None):
    '''Create function to format a LAS header item.

    Arguments:
        order: format of item, either 'descr:value' or 'value:descr' -- see
            LAS 1.2 and 2.0 specifications for more information.

    Keyword Arguments:
        left_width (int): number of characters to the left hand side of the
            first period
        middle_width (int): total number of characters minus 1 between the
            first period from the left and the first colon from the left.

    Returns:
        A function which takes a header item (e.g. LASHeaderItem or Curve)
        as its single argument and which in turn returns a string which is
        the correctly formatted LAS header line.

    '''
    if left_width is None:
        left_width = 10
    if middle_width is None:
        middle_width = 40
    mnemonic_func = lambda mnemonic: mnemonic.ljust(left_width)
    middle_func = lambda unit, right_hand_item: (
        unit
        + ' ' * (middle_width - len(str(unit)) - len(right_hand_item))
        + right_hand_item
    )
    if order == 'descr:value':
        return lambda item: '%s.%s : %s' % (
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.descr)),
            item.value
        )
    elif order == 'value:descr':
        return lambda item: '%s.%s : %s' % (
            mnemonic_func(item.original_mnemonic),
            middle_func(str(item.unit), str(item.value)),
            item.descr
        )


def get_section_order_function(section, version,
                               order_definitions=defaults.ORDER_DEFINITIONS):
    '''Get a function that returns the order per mnemonic and section.

    Arguments:
        section (str): either 'well', 'params', 'curves', 'version'
        version (float): either 1.2 and 2.0

    Keyword Arguments:
        order_definitions (dict): ...

    Returns:
        A function which takes a mnemonic (str) as its only argument, and 
        in turn returns the order 'value:descr' or 'descr:value'.

    '''
    section_orders = order_definitions[version][section]
    default_order = section_orders[0]
    orders = {}
    for order, mnemonics in section_orders[1:]:
        for mnemonic in mnemonics:
            orders[mnemonic] = order
    return lambda mnemonic: orders.get(mnemonic, default_order)


def get_section_widths(section_name, items, version, order_func,
                       middle_padding=5):
    '''Find minimum section widths fitting the content in *items*.

    Arguments:
        section_name (str): either 'version', 'well', 'curves', or 'params'
        items (SectionItems): section items
        version (float): either 1.2 or 2.0

    '''
    section_widths = {
        'left_width': None,
        'middle_width': None
    }
    if len(items) > 0:
        section_widths['left_width'] = max(
            [len(i.original_mnemonic) for i in items])
        middle_widths = []
        for i in items:
            order = order_func(i.mnemonic)
            rhs_element = order.split(':')[0]
            logger.debug(
                'get_section_widths %s\n\torder=%s rhs_element=%s' % (
                    i, order, rhs_element))
            middle_widths.append(
                len(str(i.unit)) + 1 + len(str(i[rhs_element])))
        section_widths['middle_width'] = max(middle_widths)
    return section_widths
