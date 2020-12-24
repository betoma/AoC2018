from __future__ import annotations

import copy
import itertools
from collections import deque
from operator import itemgetter
from typing import List


class Player:
    def __init__(self, deck: List[int]):
        self.deck = deque(deck)

    def __repr__(self):
        string = f"w/ {self.cards_left} cards"
        if self.cards_left > 0:
            string += f", {self.deck[0]} on top"
        return string

    @property
    def cards_left(self):
        return len(self.deck)

    def points(self):
        self.deck.reverse()
        points = 0
        for i, card in enumerate(self.deck):
            points += (i + 1) * card
        self.deck.reverse()
        return points


class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.round_no = 0

    def __repr__(self):
        string = f"Round {self.round_no}:\n"
        for i, p in enumerate(self.players):
            string += f"Player #{i+1} {p}\n"
        return string

    @classmethod
    def from_file(cls, filename: str):
        players = []
        with open(filename) as f:
            content = [x.strip() for x in f.readlines()]
        for line in content:
            if line.startswith("Player"):
                newplayer = []
            elif line == "":
                players.append(Player(newplayer))
            else:
                newplayer.append(int(line))
        players.append(Player(newplayer))
        return cls(players)

    @property
    def remaining_players(self):
        return len([player for player in self.players if player.cards_left > 0])


class Combat(Game):
    def play(self):
        yield self
        while True:
            if self.remaining_players < 2:
                break
            self.round_no += 1
            cards_in_play = [
                (i, player.deck.popleft()) for i, player in enumerate(self.players)
            ]
            cards_in_play.sort(reverse=True, key=itemgetter(1))
            self.players[cards_in_play[0][0]].deck.extend([x[1] for x in cards_in_play])
            yield self


class RecursiveCombat(Game):
    def __init__(self, players: List[Player]):
        super().__init__(players)
        self.history = []

    def play(self):
        current_state = [p.deck for p in self.players]
        while True:
            print(f"Round: {self.round_no}")
            print(self)
            if self.remaining_players < 2:
                print("someone won!")
                return [(i, p) for i, p in enumerate(self.players) if p.cards_left > 0][
                    0
                ]
            elif current_state in self.history:
                print("game ended to avoid recursion")
                return 0, self.players[0]
            self.history.append(copy.deepcopy(current_state))
            self.round_no += 1
            cards_in_play = [
                (i, player.deck.popleft()) for i, player in enumerate(self.players)
            ]
            if all([self.players[i].cards_left >= card for i, card in cards_in_play]):
                print("beginning subgame")
                subgame = RecursiveCombat(
                    [
                        Player(
                            list(
                                itertools.islice(
                                    self.players[0].deck, 0, cards_in_play[0][1]
                                )
                            )
                        ),
                        Player(
                            list(
                                itertools.islice(
                                    self.players[1].deck, 0, cards_in_play[1][1]
                                )
                            )
                        ),
                    ]
                )
                win_i, _ = yield from subgame.play()
                winner = self.players[win_i]
                cards_in_play.insert(0, cards_in_play.pop(win_i))
                print("ending subgame")
            else:
                cards_in_play.sort(reverse=True, key=itemgetter(1))
                win_i = cards_in_play[0][0]
                winner = self.players[win_i]
            winner.deck.extend([x[1] for x in cards_in_play])
            current_state = [p.deck for p in self.players]
            yield win_i, winner


# part one

game = Combat.from_file("input.txt")
for r in game.play():
    # print(r)
    pass
print(max([p.points() for p in game.players]))

# part two

game = RecursiveCombat.from_file("input.txt")
for r in game.play():
    # print(game)
    pass
print(r[1].points())
