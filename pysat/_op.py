from typing import FrozenSet as _FrozenSet


class Op:
    # noinspection PyUnresolvedReferences
    variables: _FrozenSet['Var']
    clause_count: int
    flat: bool

    # noinspection PyUnresolvedReferences
    def __init__(self, variables: _FrozenSet['Var'], clause_count: int, flat: bool = False):
        self.variables = variables
        self.clause_count = clause_count
        self.flat = flat

    def flatten(self) -> 'FlatOp':
        pass

    def blow(self) -> 'Op':
        pass

    def __str__(self) -> str:
        pass

    def __hash__(self) -> int:
        pass

    def __eq__(self, other: 'Op') -> bool:
        return hash(self) == hash(other)

    def __ne__(self, other: 'Op') -> bool:
        return hash(self) != hash(other)
