from itertools import product
from collections import Counter
from collections import defaultdict


def manhattan_distance(tpl1, tpl2):
    x1 = int(tpl1[0])
    x2 = int(tpl2[0])
    y1 = int(tpl1[1])
    y2 = int(tpl2[1])
    return abs(x1 - x2) + abs(y1 - y2)


def closest_taxi(tpl, list_of_coords):
    distances = list()
    for coord in list_of_coords:
        distance = manhattan_distance(tpl, coord)
        distances.append(distance)
    closest = min(distances)
    if distances.count(closest) == 1:
        ind = distances.index(closest)
        nearpoint = list_of_coords[ind]
    else:
        nearpoint = None
    return nearpoint


def is_edge(tpl, x1, x2, y1, y2):
    if tpl[0] == x1 or tpl[0] == x2 or tpl[1] == y1 or tpl[1] == y2:
        val = True
    else:
        val = False
    return val


def total_distance(tpl, list_of_coords):
    distances = []
    for coord in list_of_coords:
        distances.append(manhattan_distance(tpl, coord))
    return sum(distances)


coords = list()

with open("test-content.txt") as file:
    # with open("input.txt") as file:
    content = file.read().split("\n")

for item in content:
    coord = tuple([int(x.strip()) for x in item.split(",")])
    coords.append(coord)

x_coords = [a for a, b in coords]
y_coords = [b for a, b in coords]
x_max = max(x_coords)
y_max = max(y_coords)
x_min = min(x_coords)
y_min = min(y_coords)

all_coords = list(
    product([x for x in range(x_min, x_max + 1)], [x for x in range(y_min, y_max + 1)])
)

closest_coord = dict()
edge = dict()
for place in all_coords:
    closest_coord[place] = closest_taxi(place, coords)
    edge[place] = is_edge(place, x_min, x_max, y_min, y_max)

num_spaces = Counter()
infinites = list()
for k in all_coords:
    close = closest_coord[k]
    if edge[k]:
        infinites.append(close)
for k in all_coords:
    if not edge[k]:
        close = closest_coord[k]
        if close not in infinites:
            num_spaces[close] += 1

print(num_spaces.most_common(3)[0][1])

close_list = list()
for k in all_coords:
    if total_distance(k, coords) < 10000:
        close_list.append(k)

print(len(close_list))
