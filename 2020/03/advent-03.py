from typing import List

with open("input.txt", "r") as f:
    content = [x.strip() for x in f.readlines()]


def tree_index(forest: List[list], x_change: int, y_change: int):
    x, y = 0, 0
    while y < len(forest):
        yield forest[y][x % len(forest[y])]
        x += x_change
        y += y_change


def tree_count(*args):
    trees = 0
    for t in tree_index(*args):
        if t == "#":
            trees += 1
    return trees


# part one
slope = tree_count(content, 3, 1)
print(slope)

# part two
slopes = [(1, 1), (5, 1), (7, 1), (1, 2)]

for s in slopes:
    slope *= tree_count(content, *s)

print(slope)
