class Adapter:
    def __init__(self, n: int):
        self.joltage = n
        self.valid_connections = set(range(self.joltage - 3, self.joltage))

    def __repr__(self):
        return f"Adapter({self.joltage})"


class Chain:
    def __init__(self, filename: str):
        with open(filename) as f:
            numbers = [int(line.strip()) for line in f]
        numbers.sort()
        self.device = max(numbers) + 3
        self.adapters = [Adapter(0)]
        self.adapters.extend([Adapter(n) for n in numbers])
        self.adapters.append(Adapter(self.device))
        self.chain_count = {0: 1}

    @property
    def connections(self):
        return {
            n.joltage: [
                a.joltage for a in self.adapters if a.joltage in n.valid_connections
            ]
            for n in self.adapters
        }

    def chain_all_differences(self):
        one = 0
        three = 0
        for i, a in enumerate(self.adapters[:-1]):
            joltage_diff = self.adapters[i + 1].joltage - a.joltage
            if joltage_diff == 1:
                one += 1
            elif joltage_diff == 3:
                three += 1
        return one, three, one * three

    def chains_down(self, n: int):
        if n not in self.chain_count:
            self.chain_count[n] = sum(
                [self.chains_down(a) for a in self.connections[n]]
            )
        return self.chain_count[n]

    def all_chains(self):
        return self.chains_down(self.device)


system = Chain("input.txt")

# part one
print(system.chain_all_differences())

# part two
print(system.all_chains())
