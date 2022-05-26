from . import Clause


class And(Clause):
    def __init__(self, *ops, flat: bool = False):
        Clause.__init__(self, *ops, flat=flat)

    def flatten(self) -> 'And':
        if self.flat:
            return self

        ops = []
        for op in self.ops:
            op = op.flatten()
            if isinstance(op, And):
                ops.extend(op.ops)
            else:
                ops.append(op)

        return ops[0] if len(ops) == 1 else And(ops, flat=True)

    def blow(self) -> 'And':
        it = iter(self.ops)
        op = next(it).blow()

        for i in it:
            op = And(op, i.blow())

        return op

    def __str__(self) -> str:
        if len(self.ops) == 0:
            return 'TRUE'
        return f"({' and '.join([str(op) for op in self.ops])})"

    def __hash__(self) -> int:
        return hash(self.ops)
