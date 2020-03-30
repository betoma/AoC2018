from itertools import cycle
from tqdm import tqdm

class FFT:
    def __init__(self,filename:str):
        with open(filename) as f:
            content = f.read().strip()
        self.list = [int(x) for x in content]
        self.length = len(self.list)
        self.pattern = [0,1,0,-1]

    def go_pattern(self,n:int):
        out_list = []
        for item in self.pattern:
            out_list += [item] * (n+1)
        pattern = cycle(out_list)
        next(pattern)
        for _ in range(self.length):
            yield next(pattern)

    def phases(self, n):
        for _ in tqdm(range(n)):
            new_list = []
            for i in range(self.length):
                pattern = self.go_pattern(i)
                sum_up = [x*y for x, y in zip(self.list,pattern)]
                new_list.append(int(str(sum(sum_up))[-1]))
            yield new_list
            self.list = new_list
        return

#---part one---#
algo = FFT("input.txt")
for _ in algo.phases(100):
    pass
print(algo.list[:8])