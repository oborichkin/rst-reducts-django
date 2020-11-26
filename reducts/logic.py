import numpy as np


class RoughSet:
    """Класс для представления нечетких множеств

        params:
            U - двумерный массив в формате, принимаемом np.array
    """
    def __init__(self, U):
        self.U = np.array(U)
        self.C_hash = {}
        self.D_hash = {}

    def C(self, c):
        """Возвращает список кортежей условных атрибутов объектов по индексам атрибутов.
        C_hash - словарь (хэш), для сохранения результатов функции.
        Если функция уже была вызвана с такими параметрами - результат просто будет взят из хэша.
        Хэш добавлен для оптимизации работы алгоритмов, чтобы избежать множественного преобразования данных.

            params:
                c - множество индексов атрибутов
            returns:
                List[Tuple]
        """
        c = tuple(c)
        if c not in self.C_hash:
            self.C_hash[c] = [tuple(x) for x in self.U[:, list(c)]]
        return self.C_hash[c]

    def D(self, d):
        """Возвращает список кортежей целевых атрибутов объектов по индексам атрибутов.
        Параметры и суть работы такие же как в функции `C`.
        Эта функция раньше отличалась от `C`, но в процессе разработки пришла к виду аналогичному `C`.
        Я не убирал её и не стал пользоваться эксклюзивно функцией `C`
        т.к. в дальнейшем реализация может измениться (+ это добавляет читаемости).
        """
        d = tuple(d)
        if d not in self.D_hash:
            self.D_hash[d] = [tuple(x) for x in self.U[:, list(d)]]
        return self.D_hash[d]

    def equivalence_partition(self, c, d):
        """Возвращает словарь классов эквивалентности, где
            ключи - класс эквивалентности (условные атрибуты)
            значения - кортежи целевых атрибутов, принадлежащих данному классу эквивалентности

        c, d - множества индексов условных и целевых атрибутов соответственно.
        """
        classes = {}

        for idx, c in enumerate(self.C(c)):
            if c in classes:
                classes[c].append(self.D(d)[idx])
            else:
                classes[c] = [self.D(d)[idx]]

        return classes

    def __len__(self):
        """Возвращает кардинальность всего множества.
        Синтаксический сахар чтобы можно было вызывать len(U)"""
        return len(self.U)

    def gamma(self, c, d):
        """Коэффициент устойчивости при заданных условных и целевых атрибутах.
            c - условные атрибуты
            d - целевые атрибуты
        """
        ep = self.equivalence_partition(c, d)
        top_count = 0
        for k, v in ep.items():
            if len(set(v)) == 1:        # условие не фальсифицирования, означающее, что в ключе более одного типа целевой переменной
                top_count += len(v)     # добавляем число элементов в данном классе в число не входящих в Boundary Region (|U| - |BR|)
        return top_count / len(self)    # Возвращаем (|U| - |BR|) / |U|


def qreduct(U, C, D):
    """Реализация алгоритма QuickReduct
        U - объект типа RoughSet
        C - множество индексов условных атрибутов
        D - множество индексов целевых атрибутов
    Возвращает:
        R - найденый редукт
    """
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
    """Реализация алгоритма FindReducts
        U - объект типа RoughSet
        C - множество индексов условных атрибутов
        D - множество индексов целевых атрибутов
    Возвращает:
        R - множество найденых редуктов
    """
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
