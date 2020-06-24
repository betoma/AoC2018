import re


def formatLine(string):
    line = "".join(string.split())
    the_list = re.split(r"[@\:x,]", line)
    return the_list


def everySquareinch(left, top, width, height):
    set_of_squares = set()
    for i in range(1, width + 1):
        current_column = left + i
        for j in range(1, height + 1):
            current_row = top + j
            current_square = (current_column, current_row)
            set_of_squares.add(current_square)
    return set_of_squares


all_the_patterns = {}
pattern_squares = {}
used_squares = set()
overlap_squares = set()

with open("input.txt") as f:
    for line in f:
        list_of_measurements = formatLine(line)
        all_the_patterns[list_of_measurements[0]] = list_of_measurements[1:]

# part one
for the_id, pattern in all_the_patterns.items():
    the_squares = everySquareinch(
        int(pattern[0]), int(pattern[1]), int(pattern[2]), int(pattern[3])
    )
    for square in the_squares:
        if square in used_squares:
            overlap_squares.add(square)
        else:
            used_squares.add(square)
    pattern_squares[the_id] = the_squares

# part two
for the_id, squinch in pattern_squares.items():
    if not squinch.intersection(overlap_squares):
        the_one_true_id = the_id
        break

print(len(overlap_squares))
print(the_one_true_id)
