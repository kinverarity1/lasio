import json
import logging

# The standard library OrderedDict was introduced in Python 2.7 so
# we have a third-party option to support Python 2.6

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import numpy as np

logger = logging.getLogger(__name__)


class HeaderItem(OrderedDict):

    '''Dictionary/namedtuple-style object for a LAS header line.

    Arguments:
        mnemonic (str): the mnemonic
        unit (str): the unit (no whitespace!)
        value (str): value
        descr (str): description

    These arguments are available for use as either items or attributes of the
    object.

    '''
    def __init__(self, mnemonic='', unit='', value='', descr='', data=None):
        super(HeaderItem, self).__init__()

        # The original mnemonic needs to be stored for rewriting a new file.
        # it might be nothing - '' - or a duplicate e.g. two 'RHO' curves,
        # or unique - 'X11124' - or perhaps invalid??
        # It will be used only when exporting.

        self.original_mnemonic = mnemonic

        # We also need to store a more useful mnemonic, which will be used
        # (technically not, but read on) for people to access the curve while
        # the LASFile object exists. For example, a curve which is unnamed
        # and has an original_mnemonic of '' will be accessed as 'UNKNOWN'.
        # It is used in contexts where duplicate mnemonics are acceptable.

        # see property HeaderItem.useful_mnemonic

        # But note that we need to (later) check (repeatedly) for duplicate
        # mnemonics. Any duplicates will have ':1', ':2', ':3', etc., appended
        # to them. The result of this will be stored as the
        # HeaderItem.mnemonic attribute through the below method.
        # It is used in contexts where duplicate mnemonics cannot exist.

        self.set_session_mnemonic_only(self.useful_mnemonic)

        self.unit = unit
        self.value = value
        self.descr = descr
        self.data = data

    @property
    def useful_mnemonic(self):
        if self.original_mnemonic.strip() == '':
            return 'UNKNOWN'
        else:
            return self.original_mnemonic

    @useful_mnemonic.setter
    def useful_mnemonic(self, value):
        raise ValueError('Cannot set read-only attribute; try .mnemonic instead')

    def set_session_mnemonic_only(self, value):
        '''Set the mnemonic for session use.

        See source comments for :class:`lasio.las_items.HeaderItem.__init__`
        for a more in-depth explanation.

        '''
        super(HeaderItem, self).__setattr__('mnemonic', value)

    def __getitem__(self, key):
        '''Provide item dictionary-like access.'''
        if key == 'mnemonic':
            return self.mnemonic
        elif key == 'original_mnemonic':
            return self.original_mnemonic
        elif key == 'useful_mnemonic':
            return self.useful_mnemonic
        elif key == 'unit':
            return self.unit
        elif key == 'value':
            return self.value
        elif key == 'descr':
            return self.descr
        else:
            raise KeyError(
                'CurveItem only has restricted items (not %s)' % key)

    def __setattr__(self, key, value):

        if key == 'mnemonic':

            # The user wants to rename the item! This means we must send their
            # new mnemonic to the original_mnemonic attribute. Remember that the
            # mnemonic attribute is for session use only.

            self.original_mnemonic = value
            self.set_session_mnemonic_only(self.useful_mnemonic)
        else:
            super(HeaderItem, self).__setattr__(key, value)

    def __repr__(self):
        result = (
            '%s(mnemonic=%s, unit=%s, value=%s, '
            'descr=%s)' % (
                self.__class__.__name__, self.mnemonic, self.unit, self.value,
                self.descr))
        if len(result) > 80:
            return result[:76] + '...)'
        else:
            return result

    def _repr_pretty_(self, p, cycle):
        return p.text(self.__repr__())

    def __reduce__(self):
        return self.__class__, (self.mnemonic, self.unit, self.value,
                                self.descr, self.data)

    @property
    def json(self):
        return json.dumps({
            '_type': self.__class__.__name__,
            'mnemonic': self.original_mnemonic,
            'unit': self.unit,
            'value': self.value,
            'descr': self.descr
            })

    @json.setter
    def json(self, value):
        raise Exception('Cannot set objects from JSON')


class CurveItem(HeaderItem):

    '''Dictionary/namedtuple-style object for a LAS curve.

    See :class:`lasio.las_items.HeaderItem`` for the (keyword) arguments.

    Keyword Arguments:
        data (array-like, 1-D): the curve's data.

    '''

    def __init__(self, mnemonic='', unit='', value='', descr='', data=None):
        if data is None:
            data = []
        super(CurveItem, self).__init__(mnemonic, unit, value, descr)
        self.data = np.asarray(data)

    @property
    def API_code(self):
        '''Equivalent to the ``value`` attribute.'''
        return self.value

    def __repr__(self):
        return (
            '%s(mnemonic=%s, unit=%s, value=%s, '
            'descr=%s, original_mnemonic=%s, data.shape=%s)' % (
                self.__class__.__name__, self.mnemonic, self.unit, self.value,
                self.descr, self.original_mnemonic, self.data.shape))

    @property
    def json(self):
        return json.dumps({
            '_type': self.__class__.__name__,
            'mnemonic': self.original_mnemonic,
            'unit': self.unit,
            'value': self.value,
            'descr': self.descr,
            'data': list(self.data),
            })

    @json.setter
    def json(self, value):
        raise Exception('Cannot set objects from JSON')


class SectionItems(list):

    '''Variant of a ``list`` which is used to represent a LAS section.

    '''
    def __init__(self, *args, **kwargs):
        super(SectionItems, self).__init__(*args, **kwargs)
        super(SectionItems, self).__setattr__('mnemonic_transforms', False)

    def __str__(self):
        rstr_lines = []
        data = [['Mnemonic', 'Unit', 'Value', 'Description'],
                ['--------', '----', '-----', '-----------']]
        data += [[str(x) for x in [item.mnemonic, item.unit, item.value,
                                   item.descr]] for item in self]
        col_widths = []
        for i in range(len(data[0])):
            col_widths.append(max([len(row[i]) for row in data]))
        for row in data:
            line_items = []
            for i, item in enumerate(row):
                line_items.append(item.ljust(col_widths[i] + 2))
            rstr_lines.append(''.join(line_items))
        return '\n'.join(rstr_lines)

    def mnemonic_compare(self, one, two):
        if self.mnemonic_transforms:
            try:
                if one.upper() == two.upper():
                    return True
            except AttributeError:
                pass
        else:
            if one == two:
                return True
        return False

    def __contains__(self, testitem):
        '''Check whether a header item or mnemonic is in the section.

        Arguments:
            testitem (HeaderItem, CurveItem, str): either an item or a mnemonic

        Returns:
            bool

        '''
        for item in self:
            if self.mnemonic_compare(testitem, item.mnemonic):
                return True
            elif hasattr(testitem, 'mnemonic'):
                if self.mnemonic_compare(testitem.mnemonic, item.mnemonic):
                    return True
            elif testitem is item:
                return True
        else:
            return False

    def keys(self):
        '''Return mnemonics of all the HeaderItems in the section.'''
        return [item.mnemonic for item in self]

    def values(self):
        '''Return HeaderItems in the section.'''
        return self

    def items(self):
        '''Return pairs of (mnemonic, HeaderItem) from the section.'''
        return [(item.mnemonic, item) for item in self]

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self)

    def iteritems(self):
        return iter(self.items())

    def __getslice__(self, i0, i1):
        '''For Python 2.7 compatibility.'''
        return self.__getitem__(slice(i0, i1))

    def __getitem__(self, key):
        '''Item-style access by either mnemonic or index.

        Arguments:
            key (str, int, slice): either a mnemonic or the index to the list.

        Returns:
            item from the list (either HeaderItem or CurveItem)

        '''
        if isinstance(key, slice):
            return SectionItems(super(SectionItems, self).__getitem__(key))
        for item in self:
            if self.mnemonic_compare(item.mnemonic, key):
                return item
        if isinstance(key, int):
            return super(SectionItems, self).__getitem__(key)
        else:
            raise KeyError('%s not in %s' % (key, self.keys()))

    def __delitem__(self, key):
        '''Delete item by either mnemonic or index.

        Arguments:
            key (str, int): either a mnemonic or the index to the list.

        '''
        for ix, item in enumerate(self):
            if self.mnemonic_compare(item.mnemonic, key):
                super(SectionItems, self).__delitem__(ix)
                return
        if isinstance(key, int):
            super(SectionItems, self).__delitem__(key)
            return
        else:
            raise KeyError('%s not in %s' % (key, self.keys()))

    def __setitem__(self, key, newitem):
        '''Either replace the item or its value.

        Arguments:
            key (int, str): either the mnemonic or the index.
            newitem (HeaderItem or str/float/int): the thing to be set.

        If ``newitem`` is a :class:`lasio.las_items.HeaderItem` then the
        existing item will be replaced. Otherwise the existing item's ``value``
        attribute will be replaced.

        i.e. this allows us to do

            >>> from lasio import SectionItems, HeaderItem
            >>> section = SectionItems(
            ...     [HeaderItem(mnemonic="OPERATOR", value="John")]
            ... )
            >>> section.OPERATOR
            HeaderItem(mnemonic=OPERATOR, unit=, value=John, descr=)
            >>> section.OPERATOR = 'Kent'
            >>> section.OPERATOR
            HeaderItem(mnemonic=OPERATOR, unit=, value=Kent, descr=)

        See :meth:`lasio.las_items.SectionItems.set_item` and
        :meth:`lasio.las_items.SectionItems.set_item_value`.

        '''
        if isinstance(newitem, HeaderItem):
            self.set_item(key, newitem)
        else:
            self.set_item_value(key, newitem)

    def __getattr__(self, key):
        '''Provide attribute access via __contains__ e.g.

            >>> from lasio import SectionItems, HeaderItem
            >>> section = SectionItems(
            ...     [HeaderItem(mnemonic="VERS", value=1.2)]
            ... )
            >>> section['VERS']
            HeaderItem(mnemonic=VERS, unit=, value=1.2, descr=)
            >>> 'VERS' in section
            True
            >>> section.VERS
            HeaderItem(mnemonic=VERS, unit=, value=1.2, descr=)

        '''
        known_attrs = ['mnemonic_transforms', ]
        if not key in known_attrs:
            if key in self:
                return self[key]
        super(SectionItems, self).__getattr__(key)

    def __setattr__(self, key, value):
        '''Allow access to :meth:`lasio.las_items.SectionItems.__setitem__`
        via attribute access.

        '''
        if key in self:
            self[key] = value
        else:
            super(SectionItems, self).__setattr__(key, value)

    def set_item(self, key, newitem):
        '''Replace an item by comparison of session mnemonics.

        Arguments:
            key (str): the item mnemonic (or HeaderItem with mnemonic)
                you want to replace.
            newitem (HeaderItem): the new item

        If **key** is not present, it appends **newitem**.

        '''
        for i, item in enumerate(self):
            if self.mnemonic_compare(key, item.mnemonic):

                # This is very important. We replace items where
                # 'mnemonic' is equal - i.e. we do not check
                # against useful_mnemonic or original_mnemonic.

                return super(SectionItems, self).__setitem__(i, newitem)
        else:
            self.append(newitem)

    def set_item_value(self, key, value):
        '''Set the ``value`` attribute of an item.

        Arguments:
            key (str): the mnemonic of the item (or HeaderItem with the
                mnemonic) you want to edit
            value (str, int, float): the new value.

        '''
        self[key].value = value

    def append(self, newitem):
        '''Append a new HeaderItem to the object.'''
        super(SectionItems, self).append(newitem)
        self.assign_duplicate_suffixes(newitem.useful_mnemonic)

    def insert(self, i, newitem):
        '''Insert a new HeaderItem to the object.'''
        super(SectionItems, self).insert(i, newitem)
        self.assign_duplicate_suffixes(newitem.useful_mnemonic)

    def assign_duplicate_suffixes(self, test_mnemonic=None):
        '''Check and re-assign suffixes for duplicate mnemonics.

        Arguments:
            test_mnemonic (str, optional): check for duplicates of
                this mnemonic. If it is None, check all mnemonics.

        '''
        if test_mnemonic is None:
            for test_mnemonic in {i.useful_mnemonic for i in self}:
                self.assign_duplicate_suffixes(test_mnemonic)
        else:
            existing = [item.useful_mnemonic for item in self]
            locations = []
            for i, item in enumerate(self):
                if self.mnemonic_compare(item.useful_mnemonic, test_mnemonic):
                    locations.append(i)
            if len(locations) > 1:
                current_count = 1
                for i, loc in enumerate(locations):
                    item = self[loc]
                    item.set_session_mnemonic_only(item.useful_mnemonic + ':%d'
                                                % (i + 1))

    def dictview(self):
        '''View of mnemonics and values as a dict.

        Returns:
            dict - keys are the mnemonics and the values are the ``value``
            attributes.
        '''
        return dict(zip(self.keys(), [i.value for i in self.values()]))

    @property
    def json(self):
        return json.dumps(
            [item.json for item in self.values()])

    @json.setter
    def json(self, value):
        raise Exception('Cannot set objects from JSON')