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


class LASFile(object):
    def __init__(self, provenance=None):
        self.provenance = provenance
        
        
def read(file, **kwargs):
    '''Read LAS file.
    
    Args:
        - *file*: either a filename, URL, file-like object, or a string which
                  is the ASCII content of a LAS file
                  
    Kwargs: passed to either codecs.open() or urllib2.urlopen() if relevant
    
    Returns: las_reader.LASFile object
    
    '''
    f, provenance = open_file(file, **kwargs)
    log = LASFile(provenance=provenance)
    lines = f.read().splitlines()
    f.close()
    log.version = read_version_section(lines)
    log.well = read_well_section(lines, log=log)
    return log
    
    
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
    mnemonic = split_period[0].strip()
    rest = '.'.join(split_period[1:])
    if not rest.startswith(' '):
        unit = rest.split()[0].strip()
        rest = rest[len(unit):]
    else:
        unit = None
    split_colon = rest.split(':')
    description = split_colon[-1].strip()
    data = ':'.join(split_colon[:-1]).strip()
    return mnemonic, unit, data, description
    
    
def convert_number(item):
    try:
        return int(item)
    except:
        try:
            return float(item)
        except:
            return np.nan
    
    
def read_version_section(lines):
    version = {'VERS': None, 'WRAP': None, 'DLM': ' '}
    in_section = False
    for line in lines:
        line = line.strip().strip('\t').strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('~v'):
            in_section = True
            continue
        if line.lower().startswith('~') and in_section:
            return version
        if in_section:
            mnemonic, unit, data, description = read_line(line)
            if mnemonic == 'VERS':
                version['VERS'] = float(data)
            elif mnemonic == 'WRAP':
                if data.lower() == 'yes':
                    version['WRAP'] = True
                else:
                    version['WRAP'] = False
            elif mnemonic == 'DLM':
                if data == 'COMMA':
                    version['DLM'] = ','
                elif data == 'TAB':
                    version['DLM'] = '\t'
            else:
                version[mnemonic] = data
    return version
    
    
def read_well_section(lines, log):
    well = {'STRT': None,
            'STOP': None,
            'STEP': None,
            'NULL': None,
            'COMP': None,
            'WELL': None,
            'FLD': None,
            'LOC': None,
            'SRVC': None,
            'CTRY': None,
            'DATE': None}
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
                    well[mnemonic + '.UNIT'] = unit
            else:
                # Deal with the crazy change swapping the position of 
                # information at version 2.0:
                if log.version['VERS'] >= 2.:
                    well[mnemonic] = data
                else:
                    well[mnemonic] = description
            # ... and now be version-agnostic:
            value = well[mnemonic]
            if mnemonic == 'NULL':
                well['NULL'] = convert_number(data)
                if well['STOP'] == well['NULL']:
                    well['STOP'] = np.nan
            if mnemonic in ('X', 'Y'):
                well[mnemonic] = convert_number(value)
    return well
    
    
    
