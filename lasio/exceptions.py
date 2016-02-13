class LASDataError(Exception):

    '''Error during reading of numerical data from LAS file.'''
    pass


class LASHeaderError(Exception):

    '''Error during reading of header data from LAS file.'''
    pass


class LASUnknownUnitError(Exception):

    '''Error of unknown unit in LAS file.'''
    pass
