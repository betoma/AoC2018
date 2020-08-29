from operator import itemgetter, attrgetter
from collections import deque, defaultdict
from functional import compose
from tqdm import tqdm


class Unit:
    TARGETS = {"E": "G", "G": "E"}

    def __init__(self, the_type: str, loc: tuple, ap: int = 3):
        self.type = the_type
        self.target = self.TARGETS[the_type]
        self.ap = ap
        self.hp = 200
        self.location = loc
        self.alive = True

    def __repr__(self):
        return f"Unit({self.type}:{self.hp})"

    def vibe_check(self, grid):
        if self.hp <= 0:
            self.alive = False
            grid.kill(self)


class Cave:
    def __init__(self, filename: str, elf_ap: int = 3):
        with open(filename) as f:
            content = f.read().splitlines()
        self.grid = []
        for line in content:
            row = [x for x in line]
            self.grid.append(row)
        self.max_row = len(self.grid)
        self.max_column = len(self.grid[0])
        self.units = []
        for i, row in enumerate(self.grid):
            for j, column in enumerate(row):
                if column == "G":
                    self.units.append(Unit("G", (i, j), 3))
                elif column == "E":
                    self.units.append(Unit("E", (i, j), elf_ap))
        self.combat = True
        self.no_losses = True

    def __repr__(self):
        return f"Cave(Dim:{self.max_row}x{self.max_column},Units:{len(self.units)})"

    def __str__(self):
        lines = ["".join(row) for row in self.grid]
        lines.append(f"Units: {self.units}")
        return "\n".join(lines)

    def adjacent_squares(self, square: tuple):
        adj = []
        i = square[0]
        j = square[1]
        if j + 1 <= self.max_column:
            adj.append((i, j + 1))
        if j - 1 >= 0:
            adj.append((i, j - 1))
        if i + 1 <= self.max_row:
            adj.append((i + 1, j))
        if i - 1 >= 0:
            adj.append((i - 1, j))
        return adj

    def is_open(self, square: tuple, fauxpen: list = []):
        try:
            if self.grid[square[0]][square[1]] == ".":
                return True
            elif square in fauxpen:
                return True
            else:
                return False
        except IndexError:
            return False

    def in_range(self, square: tuple, **kwargs):
        open_squares = []
        for s in self.adjacent_squares(square):
            if self.is_open(s, **kwargs):
                open_squares.append(s)
        return open_squares

    def attacks(self, attacker, enemy):
        enemy.hp -= attacker.ap
        enemy.vibe_check(self)

    def kill(self, unit):
        self.grid[unit.location[0]][unit.location[1]] = "."
        unit.location = None
        if unit.type == "E":
            self.no_losses = False

    def viable_targets(self, unit):
        return [u for u in self.units if u.type == unit.target and u.alive == True]

    def viable_t_squares(self, unit, viable_targets: list = None):
        if viable_targets == None:
            viable_targets = self.viable_targets(unit)
        t_squares = []
        for u in viable_targets:
            t_squares.extend(self.in_range(u.location))
        return t_squares

    def attack_targets(self, unit, viable_targets: list = None):
        if viable_targets == None:
            viable_targets = self.viable_targets(unit)
        return [
            u
            for u in viable_targets
            if u.location in self.adjacent_squares(unit.location)
        ]

    def attack_squares(self, unit, attack_targets: list = None, **kwargs):
        if attack_targets == None:
            attack_targets = self.attack_targets(unit, **kwargs)
        return [u.location for u in attack_targets]

    def in_attack_range(self, unit, attack_squares: list = None, **kwargs):
        if attack_squares == None:
            attack_squares = self.attack_squares(unit, **kwargs)
        return any(
            [(x in attack_squares) for x in self.adjacent_squares(unit.location)]
        )

    def take_step(self, unit, square: tuple):
        if square not in self.adjacent_squares(unit.location):
            raise ValueError("Cannot move to non-adjacent square!")
        self.grid[unit.location[0]][unit.location[1]] = "."
        self.grid[square[0]][square[1]] = unit.type
        unit.location = square

    def next_steps(self, start, end):
        q = deque()
        visited = {}
        parent = defaultdict(list)
        q.appendleft(end)
        visited[end] = 1
        while q:
            current_node = q.pop()
            if current_node == start:
                return end, visited[start], parent[start]
            for node in self.in_range(current_node, fauxpen=[start]):
                if node not in visited:
                    visited[node] = visited[current_node] + 1
                    q.appendleft(node)
                    parent[node].append(current_node)
                elif any([(visited[current_node] == visited[x]) for x in parent[node]]):
                    parent[node].append(current_node)
        if start in visited:
            return end, visited[start], parent[start]
        else:
            return None

    def rounds(self, allow_losses: bool = True):
        n_rounds = -1
        while self.combat:
            n_rounds += 1
            yield n_rounds, self
            self.units = [unit for unit in self.units if unit.alive == True]
            self.units.sort(key=attrgetter("location"))
            for u in self.units:
                if not u.alive:
                    continue
                targets_left = self.viable_targets(u)
                if not targets_left:
                    self.combat = False
                    break
                else:
                    if not self.in_attack_range(u, viable_targets=targets_left):
                        open_range_squares = self.viable_t_squares(u, targets_left)
                        if not open_range_squares:
                            continue
                        else:
                            path_options = [
                                self.next_steps(u.location, x)
                                for x in open_range_squares
                            ]
                            path_options = [p for p in path_options if p is not None]
                            if path_options:
                                min_path_length = min(path_options, key=itemgetter(1))[
                                    1
                                ]
                                best_paths = [
                                    x for x in path_options if x[1] == min_path_length
                                ]
                                if len(best_paths) > 1:
                                    chosen_end = min(
                                        best_paths,
                                        key=itemgetter(0),
                                    )
                                else:
                                    chosen_end = best_paths[0]
                                if len(chosen_end[2]) > 1:
                                    step_choice = min(chosen_end[2])
                                else:
                                    step_choice = chosen_end[2][0]
                                self.take_step(u, step_choice)
                    if self.in_attack_range(u, viable_targets=targets_left):
                        adjacent_targets = self.attack_targets(u, targets_left)
                        lowest_hp = min(adjacent_targets, key=attrgetter("hp")).hp
                        weakest_links = [
                            x for x in adjacent_targets if x.hp == lowest_hp
                        ]
                        if len(weakest_links) > 1:
                            victim = min(
                                weakest_links,
                                key=attrgetter("location"),
                            )
                        else:
                            victim = weakest_links[0]
                        self.attacks(u, victim)
            if not allow_losses:
                if not self.no_losses:
                    break
        self.units = [unit for unit in self.units if unit.alive == True]
        yield n_rounds, self


# --- part one ---#
cave = Cave("input.txt")
print(cave)
for r, s in cave.rounds():
    round_no = r
print(round_no)
print(cave)
print(round_no * sum([x.hp for x in cave.units]))

# --- part two --- #
for n in tqdm(range(4, 50)):
    cave = Cave("input.txt", elf_ap=n)
    for r, s in tqdm(cave.rounds(allow_losses=False)):
        round_no = r
    if cave.no_losses:
        break
print(cave)
print(round_no * sum([x.hp for x in cave.units]))