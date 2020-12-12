class Nav:
    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def follow_path(self, filename: str):
        def string_to_dir(line: str):
            li = line.strip()
            return (li[0], int(li[1:]))

        with open(filename) as f:
            contents = f.readlines()
        path = [string_to_dir(line) for line in contents]
        instructions = {
            "R": self.turn_right,
            "L": self.turn_left,
            "N": self.north,
            "S": self.south,
            "E": self.east,
            "W": self.west,
            "F": self.forward,
        }

        for p in path:
            yield self
            instructions[p[0]](p[1])
        yield self


class Ship(Nav):
    def __init__(self):
        super().__init__()
        self.facing = "East"

    def __str__(self):
        return f"Ship: ({self.x},{self.y}), {self.facing}"

    @property
    def direction(self):
        dir_move = {
            "East": self.east,
            "West": self.west,
            "North": self.north,
            "South": self.south,
        }
        return dir_move[self.facing]

    def north(self, n: int):
        self.y += n

    def south(self, n: int):
        self.y -= n

    def east(self, n: int):
        self.x += n

    def west(self, n: int):
        self.x -= n

    def forward(self, n: int):
        self.direction(n)

    def turn(self, dir_turn: dict, degrees: int):
        for _ in range(degrees // 90):
            self.facing = dir_turn[self.facing]

    def turn_right(self, degrees: int):
        self.turn(
            {"East": "South", "South": "West", "West": "North", "North": "East"},
            degrees,
        )

    def turn_left(self, degrees: int):
        self.turn(
            {"East": "North", "North": "West", "West": "South", "South": "East"},
            degrees,
        )


class WayShip(Nav):
    def __init__(self):
        super().__init__()
        self.x_rel = 10
        self.y_rel = 1

    def __str__(self):
        return f"WayShip: ({self.x},{self.y}), waypoint at ({self.way_x},{self.way_y})"

    @property
    def way_x(self):
        return self.x + self.x_rel

    @property
    def way_y(self):
        return self.y + self.y_rel

    def north(self, n: int):
        self.y_rel += n

    def south(self, n: int):
        self.y_rel -= n

    def east(self, n: int):
        self.x_rel += n

    def west(self, n: int):
        self.x_rel -= n

    def forward(self, n: int):
        for _ in range(n):
            self.x = self.way_x
            self.y = self.way_y

    def turn_right(self, degrees: int):
        for _ in range(degrees // 90):
            new_y = 0 - self.x_rel
            new_x = self.y_rel
            self.x_rel, self.y_rel = new_x, new_y

    def turn_left(self, degrees: int):
        for _ in range(degrees // 90):
            new_y = self.x_rel
            new_x = 0 - self.y_rel
            self.x_rel, self.y_rel = new_x, new_y


# part one
# boat = Ship()

# part two
boat = WayShip()

for _ in boat.follow_path("input.txt"):
    pass
print(boat.manhattan_distance)
