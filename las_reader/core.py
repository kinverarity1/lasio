import codecs
import datetime
import os
import logging
import re
import io
import urllib.request, urllib.error, urllib.parse

import numpy
import pandas

import logging
logger = logging.getLogger(__name__)

url_regexp = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

sections_default = {
        '~V': {'VERS': {'data': '2.0', 'descr': 'CWLS LOG ASCII STANDARD - VERSION 1.2', 'name': 'VERS', 'unit': None},
               'WRAP': {'data': 'NO', 'descr': 'One line per depth step', 'name': 'WRAP', 'unit': None},
               'DLM': {'data': 'SPACE', 'descr': '', 'name': 'DLM', 'unit': None}},
        '~W': {},
        '~O': {'lines': []},
        }

class LASFile(object):
    '''A log from a LAS file.

    See read() method for how to read data in.

    '''
    def __init__(self, file=None, title='', autodetect_null=False, **kwargs):
        self.sections = dict(sections_default)
        self.title = title
        self.fail_silently = False
        self.autodetect_null = autodetect_null
        if 'fail_silently' in kwargs:
            self.fail_silently = kwargs['fail_silently']
            del kwargs['fail_silently']

        if not file is None:
            self.read(file, **kwargs)

    def read(self, file_obj, **kwargs):
        '''Read LAS file.

        Args:
            - *file_obj*: either a filename, URL, file-like object, or a string which
                      is the ASCII content of a LAS file

        Kwargs: passed to either codecs.open() or urllib2.urlopen() if relevant

        Returns: las_reader.LASFile object

        '''
        f, self.provenance = open_file(file_obj, **kwargs)
        self.fn = self.provenance['path']
        file_contents = f.read()
        f.close()
        reader = LASFileReader(file_contents)

        section_names = reader.get_section_names()
        self.sections['~V'].update(reader.read_section('~V'))
        if self.version < 3:
            for section in section_names:
                s = section[:2]
                if not s in self.sections:
                    self.sections[s] = {}
                if s == '~A':
                    continue
                elif s in ('~C'):
                    self.sections[s] = reader.read_section(s)
                else:
                    self.sections[s].update(reader.read_section(s))
        else:
            raise NotImplementedError('Cannot read LAS 3.0 files yet')

        # Read data sections
        if self.version < 3:
            self.data, self.sections['~A'] = reader.read_data(
                    wrap=self.wrap, curve_names=self.curve_names,
                    null=self.null, autodetect_null=self.autodetect_null)
        else:
            raise NotImplementedError('Cannot read LAS 3.0 files yet')

    def metadata_list(self):
        ml = []
        fn = self.provenance['path']
        for section_name, data in list(self.sections.items()):
            if isinstance(data, dict):
                for key, value in list(data.items()):
                    if section_name == '~O' and key == 'lines':
                        continue
                    if key == 'Azimuth degrees':
                        continue
                    ml.append(metadata(data[key], version=self.version))
        return ml

    def curves(self):
        curves = []
        for i, curve_name in enumerate(self.curve_names):
            curves.append([curve_name, self.data[curve_name]])
        return curves

    def sampling_intervals(self):
        return [self.sample_interval for i in self.curves()]

    def name(self):
        name = self.fn
        if name:
            return os.path.basename(name)
        else:
            return ''

    @property
    def version(self):
        return float(self.sections['~V']['VERS']['data'])

    @version.setter
    def version(self, value):
        self.sections['~V']['VERS']['data'] = str(value)

    @property
    def wrap(self):
        return bool(self.sections['~V']['WRAP']['data'] == 'yes')

    @wrap.setter
    def wrap(self, value):
        if value:
            value = 'YES'
        else:
            value = 'NO'
        self.sections['~V']['WRAP']['data']

    _delimiter_map = {'COMMA': ',', 'TAB': '\t', 'SPACE': ' '}
    _delimiter_map_inv = dict((v, k) for k, v in _delimiter_map.items())

    @property
    def delimiter(self):
        return self._delimiter_map[self.sections['~V']['DLM']['data']]

    @delimiter.setter
    def delimiter(self, value):
        self.sections['~V']['DLM']['data'] = self._delimiter_map_inv[value]

    @property
    def curve_names(self):
        return [d['name'] for d in self.sections['~C']]

    @curve_names.setter
    def curve_names(self, value):
        raise NotImplementedError('You cannot set curve names like this.')

    @property
    def sample_interval(self):
        return float(self.sections['~W']['STEP']['data'])

    @sample_interval.setter
    def sample_interval(self, value):
        self.sections['~W']['STEP'] = '%1.4f' % value

    @property
    def null(self):
        return self.sections['~W']['NULL']

    @null.setter
    def null(self, value):
        self.sections['~W']['NULL'] = value



class LASFileReader(object):
    def __init__(self, text):
        self.lines = text.split('\n')

    def get_section_names(self):
        names = []
        for line in self.lines:
            line = line.strip().strip('\t').strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('~'):
                names.append(line)
        return names

    def read_section(self, section):
        d = {}
        if section.startswith('~C'):
            d = []
        in_section = False
        for line in self.lines:
            line = line.strip().strip('\t').strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(section):
                in_section = True
                continue
            if line.lower().startswith('~') and in_section:
                return d
            if in_section:
                if section.startswith('~O'):

                    # Some software puts LAS-style data lines in the ~Other
                    # section, whereas others use it as free text. The standard
                    # allows both, so try to parse both styles.
                    try:
                        name, unit, data, descr = read_line(line)
                        di = dict(name=name, unit=unit, data=data, descr=descr)
                        self.assign_item(name, d, di)
                    except:
                        d['lines'].append(line)
                else:
                    try:
                        name, unit, data, descr = read_line(line)
                    except:
                        raise Exception('Failed to read in NAME.UNIT DATA:DESCR for:\n\t%s' % line)
                    di = dict(name=name, unit=unit, data=data, descr=descr)

                    # Retain order for ~Curves section.
                    if section.startswith('~C'):
                        d.append(di)
                    else:
                        self.assign_item(name, d, di)
        return d

    def assign_item(self, name, d, new):
        if name in d:
            existing = d[name]
            if isinstance(existing['data'], str):
                d[name]['data'] += '\n' + new['data']
            if isinstance(existing['descr'], str):
                d[name]['descr'] += '\n' + new['descr']
        else:
            d[name] = new

    def read_data(self, wrap=False, curve_names=None, null=None,
                  autodetect_null=False):
        if wrap:
            return self.read_wrapped_data(curve_names)
        s = self.read_data_string()
        try:
            arr = numpy.loadtxt(io.StringIO(s))
        except ValueError:
            lines = s.splitlines()
            sobj = io.StringIO('\n'.join(lines[:-1]))
            arr = numpy.loadtxt(sobj)
        if not arr.shape or (arr.ndim == 1 and arr.shape[0] == 0):
            logger.warning('No data present.')
            return None, None
        df_dict = {}
        arr[arr == null] = numpy.nan
        for i in range(arr.shape[1]):
            if curve_names:
                name = curve_names[i]
            else:
                name = str(i)
            data = arr[:, i]
            if autodetect_null and name != 'DEPT':
                data = remove_possible_null_values(data, name)
            series = pandas.Series(data, index=arr[:, 0], name=name)
            df_dict[name] = series
        return pandas.DataFrame(df_dict), arr

    def read_wrapped_data(self, curve_names=None):
        raise NotImplementedError('Cannot read wrapped data yet.')

    def read_data_string(self):
        for i, line in enumerate(self.lines):
            line = line.strip().strip('\t').strip()
            if line.lower().startswith('~a'):
                start_data = i + 1
                break
        s = '\n'.join(self.lines[start_data:])
        s = re.sub(r'(\d)-(\d)', r'\1 -\2', s)
        s = re.sub('-?\d*\.\d*\.\d*', ' NaN NaN ', s)
        s = re.sub('NaN.\d*', ' NaN NaN ', s)
        return s



def open_file(file_obj, **kwargs):
    provenance = {'path': None,
                  'name': None,
                  'url': None,
                  'time_opened': datetime.datetime.now()}
    if isinstance(file_obj, str):
        if os.path.exists(file_obj):
            f = codecs.open(file_obj, mode='r', **kwargs)
            provenance['name'] = os.path.basename(file_obj)
            provenance['path'] = file_obj
        elif url_regexp.match(file_obj):
            f = urllib.request.urlopen(file_obj, **kwargs)
            provenance['name'] = file_obj.split('/')[-1]
            provenance['url'] = file_obj
        else:
            f = io.StringIO(file_obj)
    else:
        f = file_obj
        try:
            provenance['name'] = f.name.split(os.sep)[-1]
            if os.path.exists(f.name):
                provenance['path'] = f.name
        except:
            pass
    return f, provenance


def read_line(line):
    if ':' in line and '.' in line.split(':', 1)[0]:
        split_period = line.split('.')
        name = split_period[0].strip()
        rest = '.'.join(split_period[1:])
        if not rest.startswith(' '):
            unit = rest.split()[0].strip()
            rest = rest[len(unit):]
        else:
            unit = None
        split_colon = rest.split(':')
        descr = split_colon[-1].strip()
        data = ':'.join(split_colon[:-1]).strip()
        return name, unit, data, descr
    elif ':' in line and not '.' in line.split(':', 1)[0]:
        split_colon = line.split(':')
        name = split_colon[0].strip()
        descr = ':'.join(split_colon[1:]).strip()
        return name, None, descr, descr
    elif '.' in line and not ':' in line:
        split_period = line.split('.')
        name = split_period[0].strip()
        descr = '.'.join(split_period[1:])
        return name, None, descr, descr


def convert_number(item):
    try:
        return int(item)
    except:
        try:
            return float(item)
        except:
            return numpy.nan


def metadata(d, version=0):
    for key_name in ['name', 'data', 'descr']:
        assert key_name in d
    key = d['name'].strip()
    if not d['descr']:
        return [key, d['data']]
    else:
        if version >= 2:
            return [key, d['data']]
        return [key, d['descr']]

def itemfreq(a):
    items, inv = np.unique(a, return_inverse=True)
    freq = np.bincount(inv)
    return np.array([items, freq]).T

def remove_possible_null_values(arr, key=''):
    lower_p = numpy.percentile(arr, 10)
    upper_p = numpy.percentile(arr, 90)
    freqs = numpy.asarray(sorted(itemfreq(arr), key=lambda r: r[1], reverse=True))
    freqs_upper_p = numpy.percentile(freqs[:, 1], 95)
    for value, freq in freqs:
        if freq >= freqs_upper_p and (value <= lower_p or value >= upper_p):
            arr[arr == value] = numpy.nan
            logger.info('Automatically removed %s from %s for being a '
                        'suspected NULL value.' % (value, key))
    return arr


class ExcelConverter(object):
    def __init__(self, las):
        self.las = las

    def write_excel(self, xlsfn):
        import xlwt
        wb = xlwt.Workbook()
        md_sheet = wb.add_sheet('Metadata')
        curves_sheet = wb.add_sheet('Curves')

        for i, (key, value) in enumerate(self.las.metadata_list()):
            md_sheet.write(i, 0, key)
            md_sheet.write(i, 1, value)

        for i, (name, data) in enumerate(self.las.curves()):
            curves_sheet.write(0, i, name)
            for j, value in enumerate(data):
                curves_sheet.write(j + 1, i, value)

        wb.save(xlsfn)
