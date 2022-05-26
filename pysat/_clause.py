from itertools import chain as _chain
from typing import FrozenSet as _FrozenSet

from . import Op


class Clause(Op):
    ops: _FrozenSet['Op']

    def __init__(self, *ops, flat: bool = False):
        if len(ops) == 0:
            self.ops = frozenset()

        elif len(ops) == 1 and hasattr(ops[0], '__iter__'):
            self.ops = frozenset(ops[0])

        else:
            self.ops = frozenset(ops)

        variables = frozenset(_chain(*[op.variables for op in self.ops]))
        clause_count = sum([op.clause_count for op in self.ops])
        flat = flat or len(ops) == 0

        Op.__init__(self, variables, clause_count, flat=flat)
