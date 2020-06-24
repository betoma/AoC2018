class Wire:
    def __init__(self, directions: list):
        self.path = directions
        self.occupies = set()
        self.delay = dict()
        self.length = 0
        for cell, length in self._occupied_cells():
            self.occupies.add(cell)
            if cell not in self.delay:
                self.delay[cell] = length
            self.length += 1

    def __repr__(self):
        return f"Wire({self.path[0]}...,Length:{self.length})"

    def __str__(self):
        return f"Wire({sorted(list(self.occupies))})"

    def _occupied_cells(self):
        cell = (0, 0)
        length = 0
        for code in self.path:
            direction = code[0]
            distance = int(code[1:])
            if direction == "U":
                for _ in range(distance):
                    cell = (cell[0], cell[1] + 1)
                    length += 1
                    yield cell, length
            elif direction == "D":
                for _ in range(distance):
                    cell = (cell[0], cell[1] - 1)
                    length += 1
                    yield cell, length
            elif direction == "R":
                for _ in range(distance):
                    cell = (cell[0] + 1, cell[1])
                    length += 1
                    yield cell, length
            elif direction == "L":
                for _ in range(distance):
                    cell = (cell[0] - 1, cell[1])
                    length += 1
                    yield cell, length


class Grid:
    def __init__(self, filename: str):
        with open(filename) as f:
            content = f.readlines()
        wire_directions = [[x for x in line.strip().split(",")] for line in content]
        self.wires = [Wire(x) for x in wire_directions]
        self.intersections = self.wires[0].occupies.intersection(self.wires[1].occupies)

    def nearest_intersection(self):
        return min([(abs(x[0]) + abs(x[1]), x) for x in list(self.intersections)])

    def least_delay(self):
        return min(
            [
                (sum([wire.delay[x] for wire in self.wires]), x)
                for x in list(self.intersections)
            ]
        )


panel = Grid("input.txt")
print(panel.wires)
print(panel.nearest_intersection())
print(panel.least_delay())
