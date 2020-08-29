from itertools import cycle
from tqdm import tqdm


class FFT:
    def __init__(self, content: str):
        self.list = [int(x) for x in content]
        self.length = len(self.list)
        self.pattern = [0, 1, 0, -1]

    def go_pattern(self, n: int):
        out_list = []
        for item in self.pattern:
            out_list += [item] * (n + 1)
        pattern = cycle(out_list)
        next(pattern)
        for _ in range(self.length):
            yield next(pattern)

    def phases(self, n):
        for _ in tqdm(range(n)):
            new_list = []
            for i in range(self.length):
                pattern = self.go_pattern(i)
                sum_up = [x * y for x, y in zip(self.list, pattern)]
                new_list.append(int(str(sum(sum_up))[-1]))
            yield new_list
            self.list = new_list
        return


# ---part one---#
with open("input.txt", "r") as f:
    c = f.read().strip()

algo = FFT(c)
for _ in algo.phases(100):
    pass
print(algo.list[:8])

# -- part two -- #
# algo2 = FFT(c * 10000)
# start = int(c[:7])
# for _ in algo2.phases(100):
#     pass
# print(algo2.list[start : start + 8])
# way too slow, gotta re-do this whole shebang
