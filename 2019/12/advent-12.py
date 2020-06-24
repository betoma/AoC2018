from itertools import count, combinations
from math import gcd


class Moon:
    def __init__(self, x, y, z):
        self.vel = [0, 0, 0]
        self.pos = [x, y, z]

    def __repr__(self):
        return f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>"

    def gravity(self, other_moon):
        for i, a, b in zip(count(), self.pos, other_moon.pos):
            if a != b:
                if a > b:
                    self.vel[i] -= 1
                    other_moon.vel[i] += 1
                else:
                    self.vel[i] += 1
                    other_moon.vel[i] -= 1

    def move(self):
        for i in range(3):
            self.pos[i] += self.vel[i]

    def pot(self):
        return sum([abs(x) for x in self.pos])

    def kin(self):
        return sum([abs(x) for x in self.vel])

    def energy(self):
        return self.pot() * self.kin()


class Planet:
    def __init__(self, filename: str):
        self.moons = []
        with open(filename) as f:
            content = f.readlines()
        for line in content:
            sep = line.replace("=", ",").replace(">", ",").split(",")
            x = int(sep[1])
            y = int(sep[3])
            z = int(sep[5])
            self.moons.append(Moon(x, y, z))

    def __repr__(self):
        return f"{self.moons}"

    def __str__(self):
        return "\n".join([str(x) for x in self.moons])

    def sim(self, t):
        yield self
        for _ in range(t):
            for a, b in combinations(self.moons, 2):
                a.gravity(b)
            for m in self.moons:
                m.move()
            yield self

    def total_energy(self):
        return sum([x.energy() for x in self.moons])


jupiter = Planet("input.txt")

# ---part one---#
for i, t in zip(count(), jupiter.sim(1000)):
    if i == 1000:
        print(t)
        print(f"Total Energy: {jupiter.total_energy()}")

# ---part two---#
def repeat(max_iter: int, axis: str):
    if axis == "x":
        v = 0
    elif axis == "y":
        v = 1
    elif axis == "z":
        v = 2
    steps = {}
    for i, t in zip(count(), jupiter.sim(max_iter)):
        this_step = tuple([(x.pos[v], x.vel[v]) for x in t.moons])
        if this_step in steps:
            loop_end = i
            break
        else:
            steps[this_step] = i
    try:
        return loop_end
    except NameError:
        return None


x_cycle = repeat(1000000, "x")
y_cycle = repeat(1000000, "y")
z_cycle = repeat(1000000, "z")
xy = abs(x_cycle * y_cycle) // gcd(x_cycle, y_cycle)
print(abs(xy * z_cycle) // gcd(xy, z_cycle))

