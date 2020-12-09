import itertools


class XMAS:
    def __init__(self, filename: str, preamble_size: int):
        with open(filename) as f:
            self.numbers = [int(n.strip()) for n in f.readlines()]
        self.preamble_size = preamble_size

    def valid_numbers(self, index: int):
        return set(
            [
                x + y
                for x, y in itertools.permutations(
                    self.numbers[index - self.preamble_size : index], 2
                )
            ]
        )

    def validate(self):
        for i, n in enumerate(self.numbers[self.preamble_size :]):
            index = i + self.preamble_size
            if n not in self.valid_numbers(index):
                return n

    def encryption(self):
        desired_number = self.validate()
        table = {1: self.numbers}
        for n in range(2, len(self.numbers) + 1):
            table[n] = []
            for i in range(len(table[n - 1])):
                if (
                    last_val := table[n - 1][i]
                ) is not None and last_val < desired_number:
                    new_n = last_val + self.numbers[i + n - 1]
                    if new_n == desired_number:
                        return i, n, new_n
                    table[n].append(new_n)
                else:
                    table[n].append(None)

    def encryption_weakness(self):
        index, size, _ = self.encryption()
        continuous_range = self.numbers[index : index + size]
        return min(continuous_range) + max(continuous_range)


system = XMAS("input.txt", 25)

# part one

print(system.validate())

# part two

print(system.encryption_weakness())
