from itertools import combinations as _combinations

from . import And, Or, Not
from . import smart_nf
from . import weak_tseytin


# noinspection PyPep8Naming
def AtMostOncePairwise(*ops) -> 'And':
    ops = [Or(Not(op1), Not(op2)) for op1, op2 in _combinations(ops, 2)]
    return And(ops).flatten()


# noinspection PyPep8Naming
def AtMostOnceSequential(*ops) -> 'And':
    # TODO implement
    return AtMostOncePairwise(*ops)


# noinspection PyPep8Naming
def AtMostOnce(*ops) -> 'And':
    if 6 > len(ops):
        return AtMostOncePairwise(*ops)
    return AtMostOnceSequential(*ops)


# noinspection PyPep8Naming
def SmartAtMostOnce(*ops) -> 'And':
    ops = [weak_tseytin(smart_nf(op)) for op in ops]

    conditions = [op[1] for op in ops]
    ops = [op[0] for op in ops]

    if 6 > len(ops):
        return And(AtMostOncePairwise(*ops), *conditions)
    return And(AtMostOnceSequential(*ops), *conditions)
