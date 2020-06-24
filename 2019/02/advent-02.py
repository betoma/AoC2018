import itertools


def intcode(program: list):
    i = 0
    while True:
        try:
            code = program[i]
        except IndexError:
            print("Something's borked")
            break
        else:
            # print(code)
            if code == 99:
                break
            else:
                first_index = program[i + 1]
                second_index = program[i + 2]
                new_index = program[i + 3]
                if code == 1:
                    new_n = program[first_index] + program[second_index]
                elif code == 2:
                    new_n = program[first_index] * program[second_index]
                program[new_index] = new_n
                i += 4
    return program[0]


def which_words(filename: str, n: int):
    with open(filename) as f:
        content = f.read()
    test_values = list(itertools.product(range(100), range(100)))
    for t in test_values:
        noun = t[0]
        verb = t[1]
        code = [int(x.strip()) for x in content.split(",")]
        code[1] = noun
        code[2] = verb
        if intcode(code) == n:
            return noun, verb
    return None


noun, verb = which_words("input.txt", 19690720)
print(f"100*{noun}+{verb}={(100*noun)+verb}")
