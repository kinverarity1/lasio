'''_logging : utility functions for logging of debug/info/warning messages

'''
import logging

def get_logger_level(logger):
    level = logger.getEffectiveLevel()
    if level >= 50:
        return 'CRITICAL'
    elif level >= 40:
        return 'ERROR'
    elif level >= 30:
        return 'WARNING'
    elif level >= 20:
        return 'INFO'
    elif level >= 10:
        return 'DEBUG'
    else:
        return 'ALL'


logging.basicConfig(format=('%(relativeCreated)d %(name)s'
                            ':%(lineno)d %(funcName)s : %(message)s'), 
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)                 
logger.debug('Initiated logging of calls >= %s' % get_logger_level(logger))
