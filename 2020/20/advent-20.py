from __future__ import annotations

import itertools
import math
from collections import defaultdict
from typing import List


class Tile:
    def __init__(self, id: """int or str""", tile_list: List[str]):
        self.tile = tile_list
        self.edges = [
            [char for char in tile_list[0]],
            [s[-1] for s in tile_list],
            [char for char in tile_list[-1]],
            [s[0] for s in tile_list],
        ]
        self.id = int(id)

    def __repr__(self):
        return f"Tile {self.id}:\n" + "\n".join(self.tile)

    def __eq__(self, other: Tile):
        return self.id == other.id

    def match_edges(self, other: Tile):
        for i, edge in enumerate(self.edges):
            for j, oth in enumerate(other.edges):
                if edge == oth:
                    return (i, j, False)
                elif edge[::-1] == oth:
                    return (i, j, True)
        return None


class Puzzle:
    def __init__(self):
        self.tiles = []

    @classmethod
    def from_file(cls, filename):
        me = cls()
        with open(filename) as f:
            content = [x.strip() for x in f.readlines()]
        for line in content:
            if line.startswith("Tile"):
                tile = []
                t_id = line.split(" ")[1].strip(":")
            elif line == "":
                me.tiles.append(Tile(t_id, tile))
            else:
                tile.append(line)
        me.tiles.append(Tile(t_id, tile))
        return me

    def find_matches(self):
        pairs = itertools.combinations(self.tiles, 2)
        connections = {}
        for x, y in pairs:
            if x.id not in connections:
                connections[x.id] = [set(), set(), set(), set()]
            if y.id not in connections:
                connections[y.id] = [set(), set(), set(), set()]
            if match := x.match_edges(y):
                connections[x.id][match[0]].add((y.id, match[1], match[2]))
                connections[y.id][match[1]].add((x.id, match[0], match[2]))
        return connections

    def corners(self, matches: dict = None):
        if matches:
            return [k for k, v in matches.items() if len([x for x in v if x]) == 2]
        return [
            k for k, v in self.find_matches().items() if len([x for x in v if x]) == 2
        ]

    def put_together(self):
        matches = self.find_matches()
        ids_left = set(matches)
        locations = defaultdict(dict)
        first_corner = self.corners(matches)[0]
        connections = {first_corner: matches[first_corner]}
        empty_sides = [i for i, side in enumerate(matches[first_corner]) if not side]
        if 0 in empty_sides and 3 in empty_sides:
            top_side = 0
        else:
            top_side = max(empty_sides)
        locations[first_corner] = ((0, 0), top_side, False, False)
        ids_left.remove(first_corner)
        while ids_left:
            new_connections = {}
            for last_id, match_list in connections.items():
                for i, match in enumerate(match_list):
                    if not match:
                        continue
                    diff = abs(locations[last_id][1] - i)


picture = Puzzle.from_file("test.txt")

# part one
print(math.prod(picture.corners()))

# part two
print(picture.find_matches())
