VERSION = (0, 1, 0, 'dev')


def get_version():
    return '.'.join(str(v) for v in VERSION)
