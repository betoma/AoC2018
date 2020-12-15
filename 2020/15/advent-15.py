from typing import List
from tqdm import trange


def play_game(starting_nos: List[int], rounds: int):
    history = {}
    now = 0
    for n in starting_nos:
        yield now + 1, n
        if now != 0:
            history[last_n] = now - 1
        now += 1
        last_n = n
    for r in trange(now, rounds):
        if last_n in history:
            new_n = r - history[last_n] - 1
        else:
            new_n = 0
        history[last_n] = r - 1
        yield r + 1, new_n
        last_n = new_n


in_list = [6, 19, 0, 5, 7, 13, 1]

# part one
for round in play_game(in_list, 2020):
    pass
print(round)

# part two
for round in play_game(in_list, 30000000):
    pass
print(round)
