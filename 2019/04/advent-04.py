from collections import Counter
from itertools import islice


def criteria(number: int):
    string_n = str(number)
    if len(string_n) == 6:
        repeats = Counter()
        for i, j in zip(string_n, islice(string_n, 1, None)):
            if int(i) > int(j):
                return False
            elif i == j:
                repeats[i + j] += 1
        if 1 in repeats.values():
            return True
    return False


print(len([n for n in range(109165, 576723) if criteria(n)]))

