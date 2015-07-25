from . import las


def read(file, **kwargs):
    return las.LASFile(file, **kwargs)

