from collections import defaultdict
import re

with open("input.txt") as f:
    contents = f.readlines()

bag_contents = {}
contained_by = defaultdict(list)

for line in contents:
    bag_rel = line.split(" bags contain ")
    bags = bag_rel[1].split(",")
    inner_bags = []
    for b in bags:
        bag = b.strip().split(" ", 1)
        if bag[0] != "no":
            n = int(bag[0])
            c = re.sub(r"\sbags?.?$", "", bag[1])
            inner_bags.append((c, n))
    bag_contents[bag_rel[0]] = inner_bags
    for bag in inner_bags:
        contained_by[bag[0]].append(bag_rel[0])


# part one


def types_contain(bag):
    bag_set = set(contained_by[bag])
    for b in contained_by[bag]:
        bag_set.update(types_contain(b))
    return bag_set


print(len(types_contain("shiny gold")))


# part two


def must_contain(bag):
    bags_needed = 0
    for b, n in bag_contents[bag]:
        bags_needed += n * (must_contain(b) + 1)
    return bags_needed


print(must_contain("shiny gold"))
