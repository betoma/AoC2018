import re

with open("input.txt", "r") as f:
    content = [re.split(r"-|:\s| ", line) for line in f.readlines()]

passwords = [(int(z[0]), int(z[1]), z[2], z[3].strip()) for z in content]

# part one


def password_check(low_n: int, high_n: int, letter: str, string: str):
    if (c := string.count(letter)) <= high_n:
        return c >= low_n


password_good = [password_check(*p) for p in passwords]

print(password_good.count(True))


# part two


def new_password_check(i_1: int, i_2: int, letter: str, string: str):
    if string[i_1 - 1] == letter:
        return string[i_2 - 1] != letter
    return string[i_2 - 1] == letter


password_better = [new_password_check(*p) for p in passwords]

print(password_better.count(True))