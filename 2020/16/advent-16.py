import math
from collections import defaultdict
from typing import List


class Trainge:
    def __init__(self, string: str):
        self.numbers = [
            int(n) for group in string.split(" or ") for n in group.split("-")
        ]

    def __repr__(self):
        return (
            f"{self.numbers[0]}-{self.numbers[1]}, {self.numbers[2]}-{self.numbers[3]}"
        )

    def __contains__(self, other):
        if isinstance(other, int):
            return (
                self.numbers[0] <= other <= self.numbers[1]
                or self.numbers[2] <= other <= self.numbers[3]
            )
        else:
            return NotImplemented


class Transticket:
    def __init__(self):
        self.my_ticket = []
        self.nearby_tickets = []
        self.fields = {}

    @classmethod
    def from_file(cls, filename: str):
        obj = cls()
        with open(filename) as f:
            for line in f.readlines():
                if line != "\n":
                    li = line.strip()
                    if ":" in line:
                        if li == "your ticket:":
                            mine = True
                        elif li == "nearby tickets:":
                            pass
                        else:
                            fields = li.split(": ")
                            obj.fields[fields[0]] = Trainge(fields[1])
                    else:
                        n_list = [int(n) for n in li.split(",")]
                        if mine:
                            obj.my_ticket = n_list
                            mine = False
                        else:
                            obj.nearby_tickets.append(n_list)
        return obj

    def is_invalid(self, n: int):
        return all([n not in self.fields[k] for k in self.fields])

    def is_valid(self, ticket: List[int]):
        return not any([self.is_invalid(n) for n in ticket])

    @property
    def valid_tickets(self):
        return [t for t in self.nearby_tickets if self.is_valid(t)] + [self.my_ticket]

    def error_rate(self):
        ticket_nos = [n for t in self.nearby_tickets for n in t]
        nos = [n for n in ticket_nos if self.is_invalid(n)]
        return sum(nos)

    @property
    def valid_numbers(self):
        by_index = defaultdict(set)
        for ticket in self.valid_tickets:
            for i, v in enumerate(ticket):
                by_index[i].add(v)
        return by_index

    def field_indices(self):
        indices = {}
        possibilities = defaultdict(set)
        for i in self.valid_numbers:
            for k in self.fields:
                if all([n in self.fields[k] for n in self.valid_numbers[i]]):
                    possibilities[k].add(i)
        while len(indices) < len(self.fields):
            solved = []
            for field in self.fields:
                if len(possibilities[field]) == 1:
                    index = possibilities[field].pop()
                    solved.append(index)
                    indices[field] = index
            for n in solved:
                for k in possibilities:
                    possibilities[k].discard(n)
        return indices

    def my_values(self):
        index_guide = self.field_indices()
        return {k: self.my_ticket[index_guide[k]] for k in self.fields}

    def my_departures(self):
        my_numbers = self.my_values()
        return [my_numbers[k] for k in my_numbers if k.startswith("departure")]


train = Transticket.from_file("input.txt")

# part one

print(train.error_rate())

# part two

print(math.prod(train.my_departures()))
