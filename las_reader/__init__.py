import codecs
import datetime
import os
import re
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import urllib2

import numpy as np


url_regexp = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        
class dict2(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        
        

class LASFile(object):
    '''A log from a LAS file.
    
    See read() method for how to read data in.
    
    '''
    sections = {'~V': {'VERS': {'data': '2.0'},
                       'WRAP': {'data': 'NO'},
                       'DLM': {'data': 'SPACE'}},
                '~W': {},
                }

    def __init__(self, file=None, **kwargs):
        if not file is None:
            self.read(file, **kwargs)
        
    def read(self, file, **kwargs):
        '''Read LAS file.
        
        Args:
            - *file*: either a filename, URL, file-like object, or a string which
                      is the ASCII content of a LAS file
                      
        Kwargs: passed to either codecs.open() or urllib2.urlopen() if relevant
        
        Returns: las_reader.LASFile object
        
        '''
        f, self.provenance = open_file(file, **kwargs)
        reader = LASFileReader(f.read().splitlines())
        f.close()
        
        section_names = reader.get_section_names()
        self.sections['~V'].update(reader.read_section('~V'))
        if self.version < 3:
            for section in section_names:
                s = section[:2]
                if not s in self.sections:
                    self.sections[s] = {}
                if s == '~A':
                    continue
                elif s == '~O':
                    self.sections[s] = reader.read_section(s)
                else:
                    self.sections[s].update(reader.read_section(s))
        else:
            raise NotImplementedError('Cannot read LAS 3.0 files yet')
    
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
    _delimiter_map_inv = dict((v, k) for k, v in _delimiter_map.iteritems())
        
    @property
    def delimiter(self):
        return self._delimiter_map[self.sections['~V']['DLM']['data']]
    
    @delimiter.setter
    def delimiter(self, value):
        self.sections['~V']['DLM']['data'] = self._delimiter_map_inv[value]
    
    
    
class LASFileReader(object):
    def __init__(self, lines):
        self.lines = lines
        
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
        if section.startswith('~O'):
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
                    d.append(line)
                else:
                    name, unit, data, descr = read_line(line)
                    d[name] = dict(name=name, unit=unit, data=data, descr=descr)
        return d
    
    
    
def open_file(file, **kwargs):
    provenance = {'path': None,
                  'name': None,
                  'url': None,
                  'time_opened': datetime.datetime.now()}
    if isinstance(file, basestring):
        if os.path.exists(file):
            f = codecs.open(file, mode='r', **kwargs)
            provenance['name'] = os.path.basename(file)
            provenance['path'] = file
        elif url_regexp.match(file):
            f = urllib2.urlopen(file, **kwargs)
            provenance['name'] = file.split('/')[-1]
            provenance['url'] = file
        else:
            f = StringIO.StringIO(file)
    else:
        f = file
        try:
            provenance['name'] = f.name.split(os.sep)[-1]
            if os.path.exists(f.name):
                provenance['path'] = f.name
        except:
            pass
    return f, provenance
            
    
def read_line(line):
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
    
    
def convert_number(item):
    try:
        return int(item)
    except:
        try:
            return float(item)
        except:
            return np.nan
    
    
def read_well_section(lines, log):
    well = dict2(STRT=None, STOP=None, STEP=None, NULL=None, COMP=None, 
                 WELL=None, FLD=None, LOC=None, SRVC=None, CTRY=None, DATE=None)
    in_section = False
    for line in lines:
        line = line.strip().strip('\t').strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('~w'):
            in_section = True
            continue
        if line.lower().startswith('~') and in_section:
            return well
        if in_section:
            mnemonic, unit, data, description = read_line(line)
            if mnemonic in ('STRT', 'STOP', 'STEP'):
                value = convert_number(data)
                if mnemonic == 'STEP' and value == 0:
                    value = np.nan
                well[mnemonic] = value
                if unit:
                    well[mnemonic + '-UNIT'] = unit
            else:
                # Deal with the crazy change swapping the position of 
                # information at version 2.0:
                if log.version >= 2.:
                    well[mnemonic] = data
                else:
                    well[mnemonic] = description
            # ... and now be version-agnostic:
            value = well[mnemonic]
            if mnemonic == 'NULL':
                well.NULL = convert_number(data)
                if well.STOP == well.NULL:
                    well.STOP = np.nan
            if mnemonic in ('X', 'Y'):
                well[mnemonic] = convert_number(value)
    return well
    
    

    
    