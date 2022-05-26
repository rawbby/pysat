from . import And, AtLeastOnce, AtMostOnce
from . import weak_tseytin, smart_nf


# noinspection PyPep8Naming
def ExactlyOnce(*ops) -> 'And':
    return And(AtLeastOnce(*ops), AtMostOnce(*ops))


# noinspection PyPep8Naming
def SmartExactlyOnce(*ops) -> 'And':
    ops = [weak_tseytin(smart_nf(op)) for op in ops]

    conditions = [op[1] for op in ops]
    ops = [op[0] for op in ops]

    return And(AtLeastOnce(*ops), AtMostOnce(*ops), *conditions)
