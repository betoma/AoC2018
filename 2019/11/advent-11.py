import intcode
from collections import defaultdict
import matplotlib.pyplot as plt


class PaintingRobot:
    def __init__(self, inputfile: str, starting_color=0):
        self.color_matrix = defaultdict(int)
        self.painted = set()
        self.robot = intcode.Intcode.read_program(inputfile)
        self.place = (0, 0)
        self.facing = (
            0,
            1,
        )  # (0,1) is up, (0,-1) is down, (1,0) is right, (-1,0) is left
        self.color_matrix[(0, 0)] = starting_color

    def turn(self, n: int):
        if n == 0:
            if self.facing[0] == 0:
                if self.facing[1] > 0:
                    self.facing = (-1, 0)
                else:
                    self.facing = (1, 0)
            else:
                if self.facing[0] > 0:
                    self.facing = (0, 1)
                else:
                    self.facing = (0, -1)
        elif n == 1:
            if self.facing[0] == 0:
                if self.facing[1] > 0:
                    self.facing = (1, 0)
                else:
                    self.facing = (-1, 0)
            else:
                if self.facing[0] > 0:
                    self.facing = (0, -1)
                else:
                    self.facing = (0, 1)
        else:
            raise ValueError(
                "Something's borked! Your program shouldn't be outputting something that isn't 1 or 0."
            )

    def take_step(self):
        self.place = tuple(
            item1 + item2 for item1, item2 in zip(self.place, self.facing)
        )

    def paint(self, color: int):
        self.color_matrix[self.place] = color
        self.painted.add(self.place)

    def run(self):
        while True:
            current_color = [self.color_matrix[self.place]]
            program = self.robot.run_program(current_color)
            try:
                color_output = next(program)
            except StopIteration:
                break
            self.paint(color_output)
            try:
                direction = next(program)
            except StopIteration:
                break
            self.turn(direction)
            self.take_step()
        return self.painted, self.color_matrix


# ---part one---#
hull = PaintingRobot("input.txt")
paint, colors = hull.run()
print(len(paint))

# ---part two--#
hull = PaintingRobot("input.txt", starting_color=1)
_, colors = hull.run()
white_list = [coord for coord in colors if colors[coord] == 1]
x_list, y_list = [i for i, j in white_list], [j for i, j in white_list]
plt.scatter(x_list, y_list, s=100)
plt.show()
