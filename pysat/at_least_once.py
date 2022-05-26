from . import Or


# noinspection PyPep8Naming
def AtLeastOnce(*ops) -> 'Or':
    return Or(ops)
