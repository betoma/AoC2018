with open("input.txt") as f:
    content = f.readlines()


# part one


def anyone(passengers):
    groups = []
    letters = set()
    for line in passengers:
        if line == "\n":
            groups.append(letters)
            letters = set()
        else:
            letters.update(set(line.strip()))
    groups.append(letters)
    return groups


print(sum([len(x) for x in anyone(content)]))


# part two


def everyone(passengers):
    groups = []
    letter_start = True
    letters = set()
    for line in passengers:
        if line == "\n":
            groups.append(letters)
            letter_start = True
        elif letter_start:
            letters = set(line.strip())
            letter_start = False
        else:
            letters = letters.intersection(set(line.strip()))
    groups.append(letters)
    return groups


print(sum([len(x) for x in everyone(content)]))
