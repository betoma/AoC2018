from collections import deque
from typing import List

from tqdm import tqdm, trange


class CupCircle:
    def __init__(self, cups: List[int]):
        self.cups = deque(cups)

    def __repr__(self):
        return " ".join(str(x) for x in self.cups)

    @classmethod
    def from_string(cls, string: str):
        return cls([int(char) for char in string])

    @classmethod
    def million_list(cls, string: str):
        me = cls.from_string(string)
        starter = max(me.cups)
        for _ in range(len(me.cups), 1000000):
            starter += 1
            me.cups.append(starter)
        return me

    def move(self):
        current_cup = self.cups[-1]
        removed_cups = [self.cups.popleft() for _ in range(3)]
        destination = current_cup - 1
        while True:
            try:
                dest = self.cups.index(destination)
            except ValueError:
                destination -= 1
                if destination < min(self.cups):
                    destination = max(self.cups)
            else:
                break
        for cup in removed_cups[::-1]:
            self.cups.insert(dest + 1, cup)
        self.cups.rotate(-1)

    def play(self, n_moves: int):
        self.cups.rotate(-1)
        yield self
        for _ in trange(n_moves):
            self.move()
            yield self

    def display_labels(self):
        while self.cups[0] != 1:
            self.cups.rotate()
        return "".join(str(x) for x in self.cups)[1:]

    def result_cups(self):
        one = self.cups.index(1)
        return self.cups[one + 1] * self.cups[one + 2]


# part one

game = CupCircle.from_string("389547612")
for move in tqdm(game.play(100)):
    pass
print(game.display_labels())

# part two

million_game = CupCircle.million_list("389547612")
for move in million_game.play(10000000):
    pass
print(million_game.result_cups())
