from . import Op, Or, Not


# noinspection PyPep8Naming
def Imp(a: 'Op', b: 'Op'):
    return Or(Not(a), b)
