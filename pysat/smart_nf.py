from . import Op, Var, And, Or, Not, Clause
from . import assignment_combinations, satisfies


def ccnf(root: 'Op') -> 'Op':
    root = root.flatten()

    if isinstance(root, Var):
        return And(Or(root))

    sat_assigns = []
    unsat_assigns = []
    for pos_assign in assignment_combinations(root.variables):
        if satisfies(root, pos_assign):
            sat_assigns.append(pos_assign)
        else:
            unsat_assigns.append(pos_assign)

    # There are less positive clauses
    # so the dnf is build here
    if len(sat_assigns) < len(unsat_assigns):
        ops = []
        for pos_assign in sat_assigns:
            neg_assign = root.variables.difference(pos_assign)
            neg_assign = [Not(v) for v in neg_assign]
            ops.append(And(*pos_assign, *neg_assign))
        return Or(ops)

    # There are less negative clauses
    # so the cnf is build here
    ops = []
    for pos_assign in unsat_assigns:
        neg_assign = root.variables.difference(pos_assign)
        neg_assign = [Not(v) for v in neg_assign]
        ops.append(And(*pos_assign, *neg_assign))
    return Not(Or(ops)).flatten()



def nf(root: 'Op') -> 'Op':
    root = root.flatten()

    if not isinstance(root, Clause):
        # Since root is not a Clause it has to be a Not or a Var.
        # As root is flat, Not and Var must be leaves and the dnf is trivial.
        return Or(And(root))

    sat_assigns = []
    unsat_assigns = []
    for pos_assign in assignment_combinations(root.variables):
        if satisfies(root, pos_assign):
            sat_assigns.append(pos_assign)
        else:
            unsat_assigns.append(pos_assign)

    # There are less positive clauses
    # so the dnf is build here
    if len(sat_assigns) < len(unsat_assigns):
        ops = []
        for pos_assign in sat_assigns:
            neg_assign = root.variables.difference(pos_assign)
            neg_assign = [Not(v) for v in neg_assign]
            ops.append(And(*pos_assign, *neg_assign))
        return Or(ops)

    # There are less negative clauses
    # so the cnf is build here
    ops = []
    for pos_assign in unsat_assigns:
        neg_assign = root.variables.difference(pos_assign)
        neg_assign = [Not(v) for v in neg_assign]
        ops.append(And(*pos_assign, *neg_assign))
    return Not(Or(ops)).flatten()


def smart_nf(root: 'Op') -> 'Op':
    root = root.flatten()

    if isinstance(root, Clause):

        variable_count = len(root.variables)
        clause_count = root.clause_count
        max_clause_count = ((2 ** variable_count) / 2)

        if 16 > clause_count > max_clause_count:
            # run dnf transformation on clauses
            # that can be reduced easily
            f = nf(root)
            return f if f.clause_count <= clause_count else root

        # recursively invoke smart_dnf on
        # all children of the clause and
        # return the new clause

        ops = [smart_nf(op) for op in root.ops]
        if isinstance(root, And):
            return And(ops)
        if isinstance(root, Or):
            return Or(ops)

    return root
