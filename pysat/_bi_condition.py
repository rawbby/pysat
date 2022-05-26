from . import Op, And, Imp


# noinspection PyPep8Naming
def BiCo(a: 'Op', b: 'Op'):
    return And(Imp(a, b), Imp(b, a))
