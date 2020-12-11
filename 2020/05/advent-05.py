import itertools


class BoardingPass:
    def __init__(self, binary_space: str):
        rows = (0, 128)
        columns = (0, 8)
        for c in binary_space[:7]:
            halfway = (rows[1] - rows[0]) // 2 + rows[0]
            if c == "F":
                rows = (rows[0], halfway)
            elif c == "B":
                rows = (halfway, rows[1])
        for c in binary_space[7:]:
            halfway = (columns[1] - columns[0]) // 2 + columns[0]
            if c == "L":
                columns = (columns[0], halfway)
            elif c == "R":
                columns = (halfway, columns[1])
        self.row = rows[0]
        self.column = columns[0]

    @property
    def id(self):
        return self.calc_seat_id(self.row, self.column)

    @staticmethod
    def calc_seat_id(row: int, col: int):
        return row * 8 + col


with open("input.txt") as f:
    contents = f.readlines()

tickets = [BoardingPass(x.strip()) for x in contents]

# part one

ids = [t.id for t in tickets]
print(max(ids))

# part two
id_set = set(ids)
all_ids = set(
    [
        BoardingPass.calc_seat_id(x, y)
        for x, y in itertools.product(range(128), range(8))
    ]
)
unused_ids = list(all_ids - id_set)

for i in unused_ids:
    if i - 1 in id_set and i + 1 in id_set:
        print(i)
        break
