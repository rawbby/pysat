from . import Op, Var, And, Or, Not


def _strong_tseytin_and(root: 'And') -> ('Var', 'And'):
    s = Var()
    it = iter(root.ops)
    a1, c1 = _strong_tseytin_dispatch(next(it))
    a2, c2 = _strong_tseytin_dispatch(next(it))
    c = And(Or(Not(a1), Not(a2), s), Or(Not(s), a1), Or(Not(s), a2))
    return s, And(c, c1, c2)


def _strong_tseytin_or(root: 'Or') -> ('Var', 'And'):
    s = Var()
    it = iter(root.ops)
    a1, c1 = _strong_tseytin_dispatch(next(it))
    a2, c2 = _strong_tseytin_dispatch(next(it))
    c = And(Or(Not(s), a1, a2), Or(Not(a1), s), Or(Not(a2), s))
    return s, And(c, c1, c2)


def _strong_tseytin_not(root: 'Not') -> ('Var', 'And'):
    a, c = _strong_tseytin_dispatch(root.a)
    return Var(-a.v), c


def _strong_tseytin_dispatch(root: 'Op') -> ('Var', 'And'):
    if isinstance(root, And):
        return _strong_tseytin_and(root)
    if isinstance(root, Or):
        return _strong_tseytin_or(root)
    if isinstance(root, Not):
        return _strong_tseytin_not(root)
    return root, And()


def strong_tseytin(root: 'Op') -> ('Var', 'And'):
    root = root.blow()
    return And(_strong_tseytin_dispatch(root))
