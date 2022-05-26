from . import Op, And, Or, Var


class Not(Op):
    a: 'Op'

    def __init__(self, a: 'Op'):
        variables = a.variables
        clause_count = a.clause_count + 1
        Op.__init__(self, variables, clause_count)
        self.a = a

    def flatten(self) -> 'Op':
        if isinstance(self.a, And):
            return Or([Not(op) for op in self.a.ops]).flatten()

        if isinstance(self.a, Or):
            return And([Not(op) for op in self.a.ops]).flatten()

        if isinstance(self.a, Not):
            return self.a.a.flatten()

        if isinstance(self.a, Var):
            return Var(-self.a.v)

    def blow(self) -> 'Not':
        return Not(self.a.blow())

    def __str__(self) -> str:
        return f'-{str(self.a)}'

    def __hash__(self) -> int:
        return -hash(self.a)

    def __int__(self) -> int:
        assert isinstance(self.a, Var)
        return -self.a.v
