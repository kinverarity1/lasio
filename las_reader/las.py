'''las.py - read Log ASCII Standard files

'''
import codecs
import collections
import datetime
import os
import logging
import re
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import urllib2

import numpy



logger = logging.getLogger(__name__)

sections_default = {
        '~V': {'VERS': {'value': '2.0', 
                        'descr': 'CWLS LOG ASCII STANDARD - VERSION 1.2', 
                        'name': 'VERS', 
                        'unit': None},
               'WRAP': {'value': 'NO', 
                        'descr': 'One line per depth step', 
                        'name': 'WRAP', 
                        'unit': None},
               'DLM': {'value': 'SPACE', 
                       'descr': '', 
                       'name': 'DLM', 
                       'unit': None}},
        '~W': {},
        '~O': {'text': ''},
        }


    

def open_file(file_obj, **kwargs):
    provenance = {'path': None,
                  'name': None,
                  'url': None,
                  'time_opened': datetime.datetime.now()}
    if isinstance(file_obj, basestring):
        if os.path.exists(file_obj):
            f = codecs.open(file_obj, mode='r', **kwargs)
            provenance['name'] = os.path.basename(file_obj)
            provenance['path'] = file_obj
        elif url_regexp.match(file_obj):
            f = urllib2.urlopen(file_obj, **kwargs)
            provenance['name'] = file_obj.split('/')[-1]
            provenance['url'] = file_obj
        else:
            f = StringIO.StringIO(file_obj)
    else:
        f = file_obj
        try:
            provenance['name'] = f.name.split(os.sep)[-1]
            if os.path.exists(f.name):
                provenance['path'] = f.name
        except:
            pass
    return f, provenance


    
class Las(object):
    '''Read LAS file.

    Args:
        - *file*: open file object or filename

    '''
    def __init__(self, file, **kwargs):
        f, provenance = open_file(file, **kwargs)
        self.provenance = provenance
        self._text = f.read()
        reader = Reader(self._text)
        
        self.version = reader.read_section('~V')
        
        # Set version
        reader.version = self.version['VERS']

        self.well = reader.read_section('~W')
        self.curves = reader.read_section('~C')
        self.params = reader.read_section('~P')
        self.other = reader.read_raw_text('~O')

        # Set null value
        reader.null = self.well['NULL']

        self.data = reader.read_data()

        for i, (key, value) in enumerate(self.curves.items()):
            self[key] = self.data[:, i]



class SectionParser(object):

    Curve = collections.namedtuple('Curve', ['unit', 'API_code', 'descr'])
    Parameter = collections.namedtuple('Parameter', ['unit', 'value', 'descr'])


    def __init__(self, section_name, version=1.2):
        if section_name.startswith('~C'):
            self.func = self.curves
        elif section_name.startswith('~P'):
            self.func = self.params
        else:
            self.func = self.metadata
        self.version = version


    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        return num(r, default=r)


    def num(x, default=None):
        if default is None:
            default = x
        try:
            return numpy.int(x)
        except:
            try:
                return numpy.float(x)
            except:
                return default


    def metadata(self, section_name, **keys):
        if self.version >= 2:
            if (keys['name'] in ['STRT', 'STOP', 'STEP', 'NULL']
                or section_name.startswith('~V')):
                return keys['value']
            else:
                return keys['descr']
        else:
            return keys['value']


    def curves(self, section_name, **keys):
        return self.Curve(keys['unit'], keys['value'], keys['descr'])


    def params(self, section_name, **keys):
        return self.Parameter(keys['unit'], keys['value'], keys['descr'])



class Reader(object):
    def __init__(self, text):
        self.lines = text.split('\n')
        self.version = 1.2
        self.null = numpy.nan
        

    @property
    def section_names(self):
        names = []
        for line in self.lines:
            line = line.strip().strip('\t').strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('~'):
                names.append(line)
        return names


    def iter_section_lines(self, section_name):
        in_section = False
        for line in self.lines:
            line = line.strip().strip('\t').strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(section_name):
                in_section = True
                continue
            if line.lower().startswith('~') and in_section:
                # Start of the next section; we're done here.
                break
            if in_section:
                yield line
        
    def read_raw_text(self, section_name):
        return '\n'.join(self.iter_section_lines(section_name))
        
    def read_section(self, section_name):
        is_section = lambda txt: section_name.startswith(txt)

        parser = SectionParser(section_name, version=self.version)
        d = collections.OrderedDict()
        in_section = False
        for line in self.iter_section_lines(section_name):            
            try:
                values = read_line(line)
            except:
                logger.warning('Failed to read in NAME.UNIT VALUE:DESCR'
                                ' from:\n\t%s' % line)
            print('values=%s' % (str(values)))
            d[name] = parser(values)
        return d
    

    def read_data(self, curve_names, wrap=False, null=None,
                  autodetect_null=False):
        s = self.read_data_string()
        try:
            arr = numpy.loadtxt(StringIO.StringIO(s))
        except ValueError:
            logger.debug('Unable to read array straight from text section')
            lines = s.splitlines()
            if wrap:
                sobj = StringIO.StringIO(' '.join(lines[:-1]))
                n = len(arr)
                j = len(curve_names)
                arr = numpy.reshape(arr, (-1, j))
            else:
                sobj = StringIO.StringIO('\n'.join(lines[:-1]))
                arr = numpy.loadtxt(sobj)
        if not arr.shape or (arr.ndim == 1 and arr.shape[0] == 0):
            logger.warning('No data present.')
            return None, None
        else:
            logger.info('Las file shape = %s' % str(arr.shape))
        df_dict = {}
        arr[arr == null] = numpy.nan
        return arr
        

    def read_data_string(self):
        for i, line in enumerate(self.lines):
            line = line.strip().strip('\t').strip()
            if line.startswith('~A'):
                start_data = i + 1
                break
        s = '\n'.join(self.lines[start_data:])
        s = re.sub(r'(\d)-(\d)', r'\1 -\2', s)
        s = re.sub('-?\d*\.\d*\.\d*', ' NaN NaN ', s)
        s = re.sub('NaN.\d*', ' NaN NaN ', s)
        return s


        
def read_line(line):
    d = {'name': None,
         'unit': None,
         'value': None,
         'descr': None}
    if ':' in line and '.' in line.split(':', 1)[0]:
        split_period = line.split('.')
        d['name'] = split_period[0].strip()
        rest = '.'.join(split_period[1:])
        if not rest.startswith(' '):
            d['unit'] = rest.split()[0].strip()
            rest = rest[len(unit):]
        split_colon = rest.split(':')
        d['descr'] = split_colon[-1].strip()
        d['value'] = ':'.join(split_colon[:-1]).strip()
    elif ':' in line and not '.' in line.split(':', 1)[0]:
        split_colon = line.split(':')
        d['name'] = split_colon[0].strip()
        d['descr'] = ':'.join(split_colon[1:]).strip()
        d['value'] = d['descr']
    elif '.' in line and not ':' in line:
        split_period = line.split('.')
        d['name'] = split_period[0].strip()
        d['descr'] = '.'.join(split_period[1:])
        d['value'] = d['descr']
    else:
        d['descr'] = line
    return d
  


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
            
        for i, curve in enumerate(self.las.curves):
            curves_sheet.write(0, i, curve.name)
            for j, value in enumerate(curve.data):
                curves_sheet.write(j + 1, i, value)
        
        wb.save(xlsfn)

