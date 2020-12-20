from collections import defaultdict
import itertools
from operator import itemgetter
from typing import List, Tuple


class PocketDimension:
    def __init__(self, dimensions: int, initial_cubes: List[Tuple[int]]):
        for cube in initial_cubes:
            if len(cube) != dimensions:
                raise ValueError
        self.activity = defaultdict(bool)
        self.dimensions = dimensions
        for location in initial_cubes:
            self.activity[location] = True

    def __repr__(self):
        quards = list(self.activity.keys())
        max_x = max(quards, key=itemgetter(0))[0]
        max_y = max(quards, key=itemgetter(1))[1]
        max_z = max(quards, key=itemgetter(2))[2]
        min_x = min(quards, key=itemgetter(0))[0]
        min_y = min(quards, key=itemgetter(1))[1]
        min_z = min(quards, key=itemgetter(2))[2]

        def three_d(w: int = None):
            string = ""
            for i in range(min_z, max_z + 1):
                string += f"\nz={i}"
                for j in range(min_y, max_y + 1):
                    string += "\n"
                    for k in range(min_x, max_x + 1):
                        if w:
                            q = (k, j, i, w)
                        else:
                            q = (k, j, i)
                        if self.activity[q]:
                            string += "#"
                        else:
                            string += "."
            return string

        if self.dimensions == 4:
            max_w = max(quards, key=itemgetter(3))[3]
            min_w = min(quards, key=itemgetter(3))[3]
            string = ""
            for w in range(min_w, max_w + 1):
                string += f"\nw={w}\n"
                string += three_d(w)
            return string
        else:
            return three_d()

    @classmethod
    def from_file(cls, filename: str, dimensions: int):
        with open(filename) as f:
            cubes = [[char for char in string.strip()] for string in f.readlines()]
        active_cubes = []
        for y, row in enumerate(cubes):
            for x, cell in enumerate(row):
                if cell == "#":
                    if dimensions == 3:
                        active_cubes.append((x, y, 0))
                    elif dimensions == 4:
                        active_cubes.append((x, y, 0, 0))
        return PocketDimension(dimensions, active_cubes)

    @property
    def total_active(self):
        return len([x for x in self.activity if self.activity[x]])

    def get_adjacent_cubes(self, coord: Tuple[int]):
        x = coord[0]
        y = coord[1]
        z = coord[2]
        x_list = [x, x + 1, x - 1]
        y_list = [y, y + 1, y - 1]
        z_list = [z, z + 1, z - 1]
        if self.dimensions == 4:
            w = coord[3]
            w_list = [w, w + 1, w - 1]
            pro = itertools.product(x_list, y_list, z_list, w_list)
        elif self.dimensions == 3:
            pro = itertools.product(x_list, y_list, z_list)
        return [tup for tup in pro if tup != coord]

    def n_active(self, coord: Tuple[int]):
        cubes = self.get_adjacent_cubes(coord)
        inactive_cubes = [x for x in cubes if not self.activity[x]]
        return len(cubes) - len(inactive_cubes), inactive_cubes

    def cycle(self, n: int):
        for _ in range(n):
            yield self
            adjacence = {}
            relevant_inactive = set()
            for cube, active in list(self.activity.items()):
                if active:
                    adj_active, adj_inactive = self.n_active(cube)
                    adjacence[cube] = adj_active
                    relevant_inactive.update(adj_inactive)
                else:
                    relevant_inactive.add(cube)
            for cube in list(relevant_inactive):
                adjacence[cube] = self.n_active(cube)[0]
            for cube, value in adjacence.items():
                if self.activity[cube]:
                    if value > 3 or value < 2:
                        self.activity[cube] = False
                elif value == 3:
                    self.activity[cube] = True
        yield self


# part one

boot = PocketDimension.from_file("input.txt", 3)
for period in boot.cycle(6):
    pass
print(boot.total_active)

# part two

boot = PocketDimension.from_file("input.txt", 4)
for period in boot.cycle(6):
    pass
print(boot.total_active)
