from collections import Counter
import itertools


def checksum(thing):
    exactly_two = 0
    exactly_three = 0
    for part in thing:
        id_letters = Counter(part)
        numbas = id_letters.values()
        if 2 in numbas:
            exactly_two += 1
        if 3 in numbas:
            exactly_three += 1
    sum = exactly_two * exactly_three
    return sum


def oneApart(str1, str2):
    differ = 0
    for i, _ in enumerate(str1):
        if str1[i] != str2[i]:
            if differ == 1:
                return False
            differ += 1
    return differ == 1


list_of_strings = []

with open("input.txt") as f:
    print(checksum(f))  # result is part one answer

with open("input.txt") as f:
    for lyne in f:
        list_of_strings.append(lyne)


for string1, string2 in itertools.combinations(list_of_strings, 2):
    if oneApart(string1, string2):
        output = []
        for i, j in enumerate(string1):
            if string1[i] == string2[i]:
                output.append(j)
        print("".join(output))  # result is part two answer
