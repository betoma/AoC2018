import itertools


class FuelCell:
    def __init__(self, x, y, serial):
        self.coordinates = (x, y)
        self.rack_id = x + 10
        self.power_level = self.rack_id * y
        self.power_level += serial
        self.power_level *= self.rack_id
        self.power_level = (self.power_level // 100) % 10
        self.power_level -= 5


class Grid:
    def __init__(self, serial):
        self.serial = serial
        self.cells = dict()
        for (i, j) in list(itertools.product(range(1, 301), range(1, 301))):
            self.cells[(i, j)] = FuelCell(i, j, serial)

    def grid(self, x, y, n):
        grid = dict()
        grid["coordinates"] = (x, y)
        grid["cells"] = dict()
        power_per_cell = list()
        for (i, j) in list(itertools.product(range(x, x + n), range(y, y + n))):
            cell = FuelCell(i, j, self.serial)
            grid["cells"][(i, j)] = cell
            power_per_cell.append(cell.power_level)
        grid["total power"] = sum(power_per_cell)
        return grid

    def max_of_size(self, n):
        total_power = dict()
        for (i, j) in list(itertools.product(range(1, 301 - n), range(1, 301 - n))):
            square = self.grid(i, j, n)
            total_power[(i, j)] = square["total power"]
        max_coords = max(total_power, key=lambda key: total_power[key])
        return max_coords, total_power[max_coords]

    def ultra_max(self):
        max_dict = dict()
        for n in range(1, 301):
            max_set = self.max_of_size(n)
            max_dict[n] = max_set
            print(f"Found max for size {n}: {max_set[1]} at {max_set[0]}")
        maximum = max(max_dict, key=lambda key: max_dict[key][1])
        return max_dict[maximum][0], maximum, max_dict[maximum][1]


test = Grid(7400)
print(test.ultra_max)
