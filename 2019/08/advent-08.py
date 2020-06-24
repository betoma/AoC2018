from collections import Counter
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np


class Image:
    def __init__(self, values: list, width: int, height: int):
        ppl = width * height
        self.width = width
        self.height = height
        self.layers = self._divide_by(values, ppl)
        self.layer_counts = [Counter(x) for x in self.layers]
        self.layer_matrix = [self._divide_by(x, width) for x in self.layers]

    def _divide_by(self, input_list: list, value: int):
        list_of_lists = [[]]
        list_count = 0
        value_count = 0
        for n in input_list:
            if value_count == value:
                value_count = 0
                list_count += 1
                list_of_lists.append(list())
            list_of_lists[list_count].append(n)
            value_count += 1
        return list_of_lists

    def least_layer(self, k: str):
        return min(self.layer_counts, key=itemgetter(k))

    def get_image_matrix(self):
        final_matrix = [list() for _ in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                values_in_pixel = [x[j][i] for x in self.layer_matrix]
                for value in values_in_pixel:
                    if value == "2":
                        continue
                    else:
                        final_matrix[j].append(value)
                        break
        return final_matrix

    def show_image(self):
        matrix = np.array(self.get_image_matrix())
        G = np.zeros((6, 25, 3))
        G[matrix == "1"] = [1, 1, 1]
        G[matrix == "2"] = [0, 0, 0]
        plt.imshow(G, interpolation="nearest")
        plt.show()


with open("input.txt") as f:
    content = f.readlines()

all_values = [char for line in content for char in line]

password = Image(all_values, 25, 6)

# ---part one---#
least_zeroes = password.least_layer("0")
print(least_zeroes["1"] * least_zeroes["2"])

# ---part two---#
print(password.show_image())
