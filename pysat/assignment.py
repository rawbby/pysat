from itertools import chain as _chain
from itertools import combinations as _combinations
from typing import FrozenSet as _FrozenSet

from . import Op, Var, And, Or, Not


def assignment_combinations(variables: _FrozenSet['Var']):
    """
    :param variables: the variables to generate an iterator over all assignment combinations
    :return: an iterator over all assignment combinations for a set of variables
    """
    lengths = range(len(variables) + 1)
    combinations = [_combinations(variables, r) for r in lengths]
    return _chain.from_iterable(combinations)


def satisfies(root: 'Op', assignment) -> bool:
    if isinstance(root, And):
        for op in root.ops:
            if not satisfies(op, assignment):
                return False
        return True

    if isinstance(root, Or):
        for op in root.ops:
            if satisfies(op, assignment):
                return True
        return False

    if isinstance(root, Not):
        return not (root.a in assignment)

    if isinstance(root, Var):
        return root in assignment
