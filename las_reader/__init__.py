import las


def read(file, **kwargs):
    return las.Las(file)