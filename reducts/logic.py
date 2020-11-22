import numpy as np


class RoughSet:

    def __init__(self, U):
        self.U = np.array(U)
        self.C_hash = {}
        self.D_hash = {}

    def C(self, c):
        c = tuple(c)
        if c not in self.C_hash:
            self.C_hash[c] = [tuple(x) for x in self.U[:, list(c)]]
        return self.C_hash[c]

    def D(self, d):
        d = tuple(d)
        if d not in self.D_hash:
            self.D_hash[d] = [tuple(x) for x in self.U[:, list(d)]]
        return self.D_hash[d]

    def equivalence_partition(self, c, d):
        classes = {}

        for idx, c in enumerate(self.C(c)):
            if c in classes:
                classes[c].append(self.D(d)[idx])
            else:
                classes[c] = [self.D(d)[idx]]

        return classes

    def __len__(self):
        return len(self.U)

    def gamma(self, c, d):
        ep = self.equivalence_partition(c, d)
        top_count = 0
        for k, v in ep.items():
            if len(set(v)) == 1:
                top_count += len(v)
        return top_count / len(self)


def qreduct(U, C, D):
    R = set()
    while True:
        T = R
        for x in C - R:
            RuX = R.union(set([x]))
            if U.gamma(RuX, D) > U.gamma(T, D):
                T = RuX

        R = T
        if U.gamma(T, D) == U.gamma(C, D):
            break
    return R


def reduct(U, C, D):
    R = set([frozenset(C)])
    while True:
        changed = False
        for_deletion = set()
        for_addition = set()
        for c in R:
            for x in c:
                if U.gamma(c, D) <= U.gamma(set(c) - set([x]), D):
                    if frozenset(set(c) - set([x])) not in R:
                        for_deletion.add(c)
                        for_addition.add(frozenset(set(c) - set([x])))
                        changed = True
        for _del in for_deletion:
            R.remove(_del)
        for _add in for_addition:
            R.add(_add)
        if not changed:
            break
    return R
