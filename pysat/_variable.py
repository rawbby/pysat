from typing import Optional as _Optional

from . import Op


class Var(Op):
    c: int = 0
    v: int

    def __init__(self, var: _Optional[int] = None):
        if var is None:
            Var.c += 1
            self.v = Var.c
        else:
            self.v = var

        Op.__init__(self, frozenset({self}), 1, flat=True)

    def flatten(self) -> 'Var':
        return self

    def blow(self) -> 'Var':
        return self

    def __str__(self) -> str:
        return 'a' + str(self.v)

    def __hash__(self) -> int:
        return hash(self.v)

    def __int__(self) -> int:
        return self.v
