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
    def __init__(self, mnemonic='', unit='', value='', descr=''):
        super(HeaderItem, self).__init__()

        # The original mnemonic needs to be stored for rewriting a new file.
        # it might be nothing - '' - or a duplicate e.g. two 'RHO' curves,
        # or unique - 'X11124' - or perhaps invalid??

        self.original_mnemonic = mnemonic

        # We also need to store a more useful mnemonic, which will be used
        # (technically not, but read on) for people to access the curve while
        # the LASFile object exists. For example, a curve which is unnamed
        # and has an original_mnemonic of '' will be accessed as 'UNKNOWN'.

        if mnemonic.strip() == '':
            self.useful_mnemonic = 'UNKNOWN'
        else:
            self.useful_mnemonic = mnemonic

        # But note that we need to (later) check (repeatedly) for duplicate
        # mnemonics. Any duplicates will have ':1', ':2', ':3', etc., appended
        # to them. The result of this will be stored as the
        # HeaderItem.mnemonic attribute through the below method.

        self.set_session_mnemonic_only(str(self.useful_mnemonic))

        self.unit = unit
        self.value = value
        self.descr = descr

    def set_session_mnemonic_only(self, value):
        '''Set the mnemonic for session use.

        See source comments for :class:`lasio.las_items.HeaderItem` for more
        in-depth explanation.

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
        
        # The user wants to rename the item! This means we must send their
        # new mnemonic to the original_mnemonic attribute. Remember that the
        # mnemonic attribute is for session use only.

        if key == 'mnemonic':
            super(HeaderItem, self).__setattr__('original_mnemonic', value)

        # Otherwise it's fine.

        super(HeaderItem, self).__setattr__(key, value)

    def __repr__(self):
        return (
            '%s(mnemonic=%s, unit=%s, value=%s, '
            'descr=%s, original_mnemonic=%s)' % (
                self.__class__.__name__, self.mnemonic, self.unit, self.value,
                self.descr, self.original_mnemonic))

    def _repr_pretty_(self, p, cycle):
        return p.text(self.__repr__())

    def __reduce__(self):
        return self.__class__, (self.mnemonic, self.unit, self.value, 
                                self.descr)

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

    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            self.data = np.asarray(kwargs["data"])
            del kwargs["data"]
        else:
            self.data = np.ndarray([])
        super(CurveItem, self).__init__(*args, **kwargs)

    @property
    def API_code(self):
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

    def __contains__(self, testitem):
        '''Allows testing of a mnemonic or an actual item.'''
        for item in self:
            if testitem == item.mnemonic:
                return True
            elif hasattr(testitem, 'mnemonic'):
                if testitem.mnemonic == item.mnemonic:
                    return True
            elif testitem is item:
                return True
        else:
            return False

    def keys(self):
        return [item.mnemonic for item in self]

    def values(self):
        return self

    def items(self):
        return [(item.mnemonic, item) for item in self]

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self)

    def iteritems(self):
        return iter(self.items())

    def __getitem__(self, key):
        for item in self:
            if item.mnemonic == key:
                return item
        if isinstance(key, int):
            return super(SectionItems, self).__getitem__(key)
        else:
            raise KeyError('%s not in %s' % (key, self.keys()))

    def __setitem__(self, key, newitem):
        if isinstance(newitem, HeaderItem):
            self.set_item(key, newitem)
        else:
            self.set_item_value(key, newitem)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            super(SectionItems, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
        else:
            super(SectionItems, self).__setattr__(key, value)

    def set_item(self, key, newitem):
        for i, item in enumerate(self):
            if key == item.mnemonic:

                # This is very important. We replace items where
                # 'mnemonic' is equal - i.e. we do not check useful_mnemonic
                # or original_mnemonic. Is this correct? Needs to thought
                # about and tested more carefully.

                return super(SectionItems, self).__setitem__(i, newitem)
        else:
            self.append(newitem)

    def set_item_value(self, key, value):
        self[key].value = value

    def append(self, newitem):
        '''Check to see if the item's mnemonic needs altering.'''
        super(SectionItems, self).append(newitem)

        # Check to fix the :n suffixes
        existing = [item.useful_mnemonic for item in self]
        locations = []
        for i, item in enumerate(self):
            if item.useful_mnemonic == newitem.mnemonic:
                locations.append(i)
        if len(locations) > 1:
            current_count = 1
            for i, loc in enumerate(locations):
                item = self[loc]
                # raise Exception('%s' % str(type(item)))
                item.set_session_mnemonic_only(item.useful_mnemonic + ':%d'
                                               % (i + 1))
                # item.mnemonic = item.useful_mnemonic + ':%d' % (i + 1)

    def dictview(self):
        return dict(zip(self.keys(), [i.value for i in self.values()]))

    @property
    def json(self):
        return json.dumps(
            [item.json for item in self.values()])

    @json.setter
    def json(self, value):
        raise Exception('Cannot set objects from JSON')