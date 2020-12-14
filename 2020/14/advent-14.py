import itertools


def read_file(filename: str):
    with open(filename) as f:
        for line in f:
            x = line.strip().split(" = ")
            if x[0] == "mask":
                yield x[0], x[1]
            else:
                yield x[0][:3], int(x[0][4:-1]), int(x[1])


class Docking:
    def __init__(self):
        self.mask = {}
        self.memory = {}

    @property
    def memory_sum(self):
        return sum(self.memory.values())

    def set_mask(self, mask: str):
        self.mask = mask

    def through_mask(self, n: int):
        binary = zip(self.mask, format(n, "036b"))
        return int("".join(y if x == "X" else x for x, y in binary), 2)

    def through_floatmask(self, n: int):
        binary = zip(self.mask, format(n, "036b"))
        float_list = [y if x == "0" else (x if x == "1" else "01") for x, y in binary]
        return itertools.product(*float_list)

    @classmethod
    def initialize(cls, filename: str):
        dock = cls()
        for x in read_file(filename):
            if x[0] == "mask":
                dock.set_mask(x[1])
            elif x[0] == "mem":
                address = x[1]
                dock.memory[address] = dock.through_mask(x[2])
        return dock

    @classmethod
    def v2(cls, filename: str):
        dock = cls()
        for x in read_file(filename):
            if x[0] == "mask":
                dock.set_mask(x[1])
            elif x[0] == "mem":
                for address in dock.through_floatmask(x[1]):
                    dock.memory[address] = x[2]
        return dock


# part one

port1 = Docking.initialize("input.txt")
print(port1.memory_sum)

# part two

port2 = Docking.v2("input.txt")
print(port2.memory_sum)
