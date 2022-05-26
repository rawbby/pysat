from pysat import *


def test1(at_most_once_):
    a = Var()
    b = Var()
    c = Var()
    d = Var()

    j = And(Or(c, d), Not(c))
    k = Or(Imp(a, d), Imp(a, d))
    m = Imp(And(a, b), BiCo(c, b))
    n = BiCo(BiCo(c, b), Not(c))

    o = BiCo(n, Not(Or(j, k, Or(c, d), Not(And(b, c, d, And(a, b))))))
    p = Imp(Not(c), Not(BiCo(And(Not(Or(c, d)), m, n), And(Or(c, d), Not(c), a))))
    r = And(Or(j, k, Not(BiCo(Imp(a, n), And(Not(k), Or(Not(Or(c, d)), Or(c, d)))))))
    s = Or(Not(o), And(Not(p), r), Imp(r, p))
    q = Not(And(a, b, at_most_once_(k, j, m, o, p, r, s), Not(j)))

    phi = And(Not(s), Imp(s, And(p, Not(q))))
    print('phi                             = ', len(phi.variables), phi.clause_count)

    phi_ = smart_nf(phi)
    print('smart_nf(phi)                   = ', len(phi_.variables), phi_.clause_count)

    phi_ = weak_tseytin_cnf(phi_)
    print('weak_tseytin_cnf(smart_nf(phi)) = ', len(phi_.variables), phi_.clause_count)

    phi_ = strong_tseytin(phi)
    print('strong_tseytin(phi)             = ', len(phi_.variables), phi_.clause_count)

    phi_ = strong_tseytin(smart_nf(phi))
    print('strong_tseytin(smart_nf(phi))   = ', len(phi_.variables), phi_.clause_count)

    phi_ = weak_tseytin_cnf(phi)
    print('weak_tseytin_cnf(phi)           = ', len(phi_.variables), phi_.clause_count)


def main():
    print()
    print('=== AtMostOnce ===')
    test1(AtMostOnce)

    # print()
    # print('=== SmartAtMostOnce ===')
    # test1(SmartAtMostOnce)

    # print()
    # print('=== ExactlyOnce ===')
    # test1(ExactlyOnce)

    # print()
    # print('=== SmartExactlyOnce ===')
    # test1(SmartExactlyOnce)


if __name__ == '__main__':
    main()
