from . import Op, Var, And, Or, Not


# noinspection DuplicatedCode
def weak_tseytin_and(root: 'And') -> ('Var', 'And'):
    """
    Generate a tseytin transformation for a clause.
    But do not replace every operation by a variable
    but every clause.

    This optimization reduces the computational effort
    and the amount of new variables and clauses.

    :param root: the clause which to tseytin transform
    :return: the replacement variable for the given clause
             and the conditions to make the replacement
             variable valid (in flat conjunctive normal form).
    """

    conditions = []
    ops = []

    # make this clause pure. meaning all children
    # have to be literals. to achieve this all non
    # literals get transformed using weak_tseytin.
    for op in root.ops:
        if isinstance(op, Or):
            v, c = weak_tseytin_or(op)
            conditions.append(c)
            ops.append(v)
        else:
            ops.append(op)

    # now weak_tseytin transform this clause itself.
    # where s is the replacement for this clause and
    # the conditions need to be added to the root and
    # clause of the formula.
    s = Var()

    # conditions are:

    # not(clause) or s -- which is trivial
    conditions.append(Or(*[Not(op) for op in ops], s))
    # not(s) or clause -- where we need to take the product
    conditions.extend([Or(Not(s), op) for op in ops])

    return s, And(conditions).flatten()


# noinspection DuplicatedCode
def weak_tseytin_or(root: 'Or') -> ('Var', 'And'):
    """
    Generate a tseytin transformation for a clause.
    But do not replace every operation by a variable
    but every clause.

    This optimization reduces the computational effort
    and the amount of new variables and clauses.

    :param root: the clause which to tseytin transform
    :return: the replacement variable for the given clause
             and the conditions to make the replacement
             variable valid (in flat conjunctive normal form).
    """

    conditions = []
    ops = []

    # make this clause pure. meaning all children
    # have to be literals. to achieve this all non
    # literals get transformed using weak_tseytin.
    for op in root.ops:
        if isinstance(op, And):
            v, c = weak_tseytin_and(op)
            conditions.append(c)
            ops.append(v)
        else:
            ops.append(op)

    # now weak_tseytin transform this clause itself.
    # where s is the replacement for this clause and
    # the conditions need to be added to the root and
    # clause of the formula.
    s = Var()

    # conditions are:

    # not(s) or clause -- which is trivial
    conditions.append(Or(Not(s), *ops))
    # not(clause) or s -- where we need to take the product
    conditions.extend([Or(Not(op), s) for op in ops])

    return s, And(conditions).flatten()


def weak_tseytin(root: 'Op') -> ('Var', 'And'):
    root = root.flatten()

    if isinstance(root, And):
        return weak_tseytin_and(root)

    if isinstance(root, Or):
        return weak_tseytin_or(root)

    return root, And()


def weak_tseytin_cnf(root: 'Op') -> 'And':
    """
    Use the weak tseytin transformation to transform a
    given formula into a cnf.

    :param root: the formula which to tseytin transform
    :return: the generated conjunctive normal form.
    """

    root = root.flatten()

    # noinspection PyShadowingNames,DuplicatedCode
    def weak_tseytin_cnf_or(root: 'Or') -> ('Or', 'And'):
        ops = []
        conditions = []

        for op in root.ops:
            if isinstance(op, And):
                v, c = weak_tseytin_and(op)
                ops.append(v)
                conditions.append(c)
            else:
                ops.append(op)

        return Or(ops), And(conditions)

    if isinstance(root, And):
        ops = []

        for op in root.ops:
            if isinstance(op, Or):
                or_op, conditions = weak_tseytin_cnf_or(op)
                ops.append(conditions)
                ops.append(or_op)
            else:
                ops.append(op)

        return And(ops).flatten()

    if isinstance(root, Or):
        # TODO this can maybe be done more efficient
        or_op, conditions = weak_tseytin_cnf_or(root)
        return And(conditions, or_op).flatten()

    return And(Or(root))
