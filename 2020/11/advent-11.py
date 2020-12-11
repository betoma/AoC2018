from __future__ import annotations
import itertools


class Place:
    def __init__(self, row: int, column: int):
        self.location = (row, column)

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return f"Seat({self.symbol}: {self.location})"

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.occupied == other.occupied
            and self.location == other.location
        )


class Seat(Place):
    def __init__(
        self,
        row: int,
        column: int,
        room: WaitingRoom,
        occupied: bool = False,
        threshold: int = 4,
    ):
        super().__init__(row, column)
        self.waiting = room
        self.occupied = occupied
        self.threshold = threshold
        self.seat = True

    @property
    def symbol(self):
        if self.occupied:
            return "#"
        else:
            return "L"

    def adjacent_seats(self):
        x, y = self.location
        possible_x = [x]
        possible_y = [y]
        if x > 0:
            possible_x.append(x - 1)
        if y > 0:
            possible_y.append(y - 1)
        if x < self.waiting.rows - 1:
            possible_x.append(x + 1)
        if y < self.waiting.columns - 1:
            possible_y.append(y + 1)
        allowed_spots = [
            s for s in itertools.product(possible_x, possible_y) if s != self.location
        ]
        return [self.waiting.room[i][j] for i, j in allowed_spots]

    def too_full(self):
        return len([s for s in self.adjacent_seats() if s.occupied]) >= self.threshold

    def all_empty(self):
        return all([not s.occupied for s in self.adjacent_seats()])

    def change_status(self):
        if self.occupied and self.too_full():
            return self.__class__(
                self.location[0], self.location[1], self.waiting, occupied=False
            )
        elif (not self.occupied) and self.all_empty():
            return self.__class__(
                self.location[0], self.location[1], self.waiting, occupied=True
            )
        else:
            return self


class Floor(Place):
    def __init__(self, row: int, column: int):
        super().__init__(row, column)
        self.occupied = False
        self.seat = False

    @property
    def symbol(self):
        return "."

    def change_status(self):
        return self


class SmarterSeat(Seat):
    def __init__(
        self,
        row: int,
        column: int,
        room: WaitingRoom,
        occupied: bool = False,
        threshold: int = 5,
    ):
        super().__init__(row, column, room, occupied, threshold)

    def adjacent_seats(self):
        adj_places = super().adjacent_seats()
        seats_that_matter = [s for s in adj_places if s.seat]
        empty_places = [
            (s, (s.location[0] - self.location[0], s.location[1] - self.location[1]))
            for s in adj_places
            if not s.seat
        ]
        while empty_places:
            look_further = []
            for spot, loc in empty_places:
                x = spot.location[0]
                y = spot.location[1]
                new_x, new_y = (x + loc[0], y + loc[1])
                if (
                    new_x >= 0
                    and new_x <= self.waiting.rows - 1
                    and new_y >= 0
                    and new_y <= self.waiting.columns - 1
                ):
                    look_further.append((self.waiting.room[new_x][new_y], loc))
            seats_that_matter.extend([s[0] for s in look_further if s[0].seat])
            empty_places = [s for s in look_further if not s[0].seat]
        return seats_that_matter


class WaitingRoom:
    def __init__(self, filename: str):
        with open(filename) as f:
            contents = [line.strip() for line in f]
        self.room = []
        for i, line in enumerate(contents):
            row = []
            for j, cell in enumerate(line):
                if cell == "L":
                    # part one
                    # row.append(Seat(i, j, self))
                    # part two
                    row.append(SmarterSeat(i, j, self))
                elif cell == ".":
                    row.append(Floor(i, j))
            self.room.append(row)

    def __str__(self):
        return "\n".join(["".join([repr(s) for s in row]) for row in self.room])

    @property
    def rows(self):
        return len(self.room)

    @property
    def columns(self):
        return len(self.room[0])

    def n_occupied(self):
        return len([seat for row in self.room for seat in row if seat.occupied])

    def churn(self):
        unstable = True
        while unstable:
            yield self
            new_room = [[s.change_status() for s in row] for row in self.room]
            if all([row == self.room[i] for i, row in enumerate(new_room)]):
                unstable = False
            self.room = new_room


r = WaitingRoom("input.txt")
for _ in r.churn():
    pass
print(r.n_occupied())
