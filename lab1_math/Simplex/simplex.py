from typing import Any


def min_check(seq):
    x = 0
    while x < len(seq):
        while x < len(seq) and seq[x] == '-1':
            seq.pop(x)
        x += 1
    if not seq:
        assert False, "Невозможно найти решение, ибо функция бесконечно растущая"
    return min(seq)

def my_simplex(a: list[float], b: list[float], c: list[Any], flip: bool, saveslack: bool, counter: int):
    if flip:
        for x in range(0, len(c)):
            c[x] = -c[x]
    bases = []
    symbols = []
    for x in range(0, len(a)):
        index = len(a[x]) - 1
        if type(a[x][index]) is str:
            symbols.append(a[x][index])
            a[x].pop(index)
        else:
            symbols.append(a[x][index])
    for x in range(0, len(a)):
        if symbols[x] == '<':
            c.append(0)
            counter += 1
            for y in range(0, len(a)):
                if y != x:
                    a[y].append(0)
                else:
                    a[y].append(1)
        elif symbols[x] == '>':
            c.append(0)
            counter += 1
            for y in range(0, len(a)):
                if y != x:
                    a[y].append(0)
                else:
                    a[y].append(-1)
    for x in range(0, len(a[0])):
        y = 0
        baseIndex = -1
        isBase = True
        while isBase and y < len(b):
            isBase = a[y][x] == 0 or a[y][x] == 1
            if a[y][x] == 1:
                if baseIndex > -1:
                    isBase = False
                    baseIndex = -1
                else:
                    baseIndex = y
            y += 1
        if isBase:
            bases.append(baseIndex)
        else:
            bases.append(-1)
    baseExists = []
    for x in range(0, len(b)):
        baseExists.append(False)
    for x in range(0, len(a[0])):
        if bases[x] > -1:
            baseExists[bases[x]] = True
    for x in range(0, len(b)):
        if not baseExists[x]:
            c.append(1)
            counter += 1
            for y in range(0, len(b)):
                a[y].append(0)
            a[x][len(a[0]) - 1] = 1
            bases.append(x)
    bases_prime = []
    for x in range(0, len(bases)):
        if bases[x] > -1:
            bases_prime.append(x)
    success = False
    deltas = []
    for y in range(0, len(a[0])):
        d = 0
        for x in range(0, len(bases)):
            if bases[x] > -1:
                d += a[bases[x]][y] * c[x]
        d -= c[y]
        deltas.append(d)
    success = True
    for x in range(1, len(deltas)):
        success = deltas[x] <= 0 and success
    while not success:
        index = deltas.index(max(deltas))
        potential = []
        for y in range(0, len(b)):
            if a[y][index] > 0:
                potential.append(b[y] / a[y][index])
            else:
                potential.append('-1')
        potential_prime = []
        for x in range(0, len(potential)):
            potential_prime.append(potential[x])
        minp = min_check(potential)
        index2 = potential_prime.index(minp)
        index3 = bases.index(index2)
        bases[index] = index2
        bases[index3] = -1
        divider = a[index2][index]
        for x in range(0, len(a[0])):
            a[index2][x] /= divider
        b[index2] /= divider
        for y in range(0, len(a)):
            if y != index2:
                multiplier = -a[y][index]
                for x in range(0, len(a[0])):
                    a[y][x] += a[index2][x] * multiplier
                b[y] += b[index2] * multiplier
        deltas = []
        for y in range(0, len(a[0])):
            d = 0
            for x in range(0, len(bases)):
                if bases[x] > -1:
                    d += a[bases[x]][y] * c[x]
            d -= c[y]
            deltas.append(d)
        success = True
        for x in range(0, len(deltas)):
            success = deltas[x] <= 0 and success
    result = []
    bases = bases[:len(bases) - counter]
    if not saveslack:
        for x in range(0, len(a)):
            a[x] = a[x][:len(a[x]) - counter]
        c = c[: len(c) - counter]
    for x in range(0, len(bases)):
        if bases[x] > -1:
            result.append(b[bases[x]])
        else:
            result.append(0)
    f = 0
    for x in range(0, len(bases)):
        if bases[x] > -1:
            f += b[bases[x]] * c[x]
    if flip:
        f = -f
    return [a, b, bases_prime, bases, f, result, c, counter]


def my_simplex_double(a, b, c, flip, saveslack, counter):
    if flip:
        for x in range(0, len(c)):
            c[x] = -c[x]
    bases = []
    symbols = []
    for x in range(0, len(a)):
        index = len(a[x]) - 1
        if type(a[x][index]) is str:
            symbols.append(a[x][index])
            a[x].pop(index)
        else:
            symbols.append(a[x][index])
    for x in range(0, len(a)):
        if symbols[x] == '<':
            c.append(0)
            counter += 1
            for y in range(0, len(a)):
                if y != x:
                    a[y].append(0)
                else:
                    a[y].append(1)
        elif symbols[x] == '>':
            c.append(0)
            counter += 1
            for y in range(0, len(a)):
                if y != x:
                    a[y].append(0)
                else:
                    a[y].append(-1)
    for x in range(0, len(a[0])):
        y = 0
        baseIndex = -1
        isBase = True
        while isBase and y < len(b):
            isBase = a[y][x] == 0 or a[y][x] == 1
            if a[y][x] == 1:
                if baseIndex > -1:
                    isBase = False
                    baseIndex = -1
                else:
                    baseIndex = y
            y += 1
        if isBase:
            bases.append(baseIndex)
        else:
            bases.append(-1)
    baseExists = []
    for x in range(0, len(b)):
        baseExists.append(False)
    for x in range(0, len(a[0])):
        if bases[x] > -1:
            baseExists[bases[x]] = True
    for x in range(0, len(b)):
        if not baseExists[x]:
            c.append(1)
            counter += 1
            for y in range(0, len(b)):
                a[y].append(0)
            a[x][len(a[0]) - 1] = 1
            bases.append(x)
    bases_prime = []
    for x in range(0, len(bases)):
        if bases[x] > -1:
            bases_prime.append(x)
    deltas = []
    for y in range(0, len(a[0])):
        d = 0
        for x in range(0, len(bases)):
            if bases[x] > -1:
                d += a[bases[x]][y] * c[x]
        d -= c[y]
        deltas.append(d)
    success = True
    for x in range(0, len(b)):
        success = b[x] >= 0 and success
    while not success:
        index = b.index(min(b))
        potential = []
        for y in range(0, len(deltas)):
            if a[index][y] != 0 and bases[y] == -1 and deltas[y] < 0:
                potential.append(deltas[y] / a[index][y])
            else:
                potential.append('-1')
        potential_prime = []
        for x in range(0, len(potential)):
            potential_prime.append(potential[x])
        minp = min_check(potential)
        index2 = potential_prime.index(minp)
        index3 = bases.index(index)
        bases[index2] = index
        bases[index3] = -1
        divider = a[index][index2]
        for x in range(0, len(a[0])):
            a[index][x] /= divider
        b[index] /= divider
        for y in range(0, len(a)):
            if y != index:
                multiplier = -a[y][index2]
                for x in range(0, len(a[0])):
                    a[y][x] += a[index][x] * multiplier
                b[y] += b[index] * multiplier
        deltas = []
        for y in range(0, len(a[0])):
            d = 0
            for x in range(0, len(bases)):
                if bases[x] > -1:
                    d += a[bases[x]][y] * c[x]
            d -= c[y]
            deltas.append(d)
        success = True
        for x in range(0, len(b)):
            success = b[x] >= 0 and success
    result = []
    bases = bases[:len(bases) - counter]
    if not saveslack:
        for x in range(0, len(a)):
            a[x] = a[x][:len(a[x]) - counter]
        c = c[: len(c) - counter]
    for x in range(0, len(bases)):
        if bases[x] > -1:
            result.append(b[bases[x]])
        else:
            result.append(0)
    f = 0
    for x in range(0, len(bases)):
        if bases[x] > -1:
            f += b[bases[x]] * c[x]
    if flip:
        f = -f
    return [a, b, bases_prime, bases, f, result, c, counter]
