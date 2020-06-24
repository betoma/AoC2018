import re
import matplotlib.pyplot as plt

# with open("test-input.txt") as file:
with open("input.txt") as file:
    lines = [l.rstrip("\n") for l in file]
    lines = [[int(i) for i in re.findall(r"-?\d+", l)] for l in lines]

for i in range(0, 10000000000):
    rows = [x[0] for x in lines]
    columns = [x[1] for x in lines]
    min_frame = (max(rows) - min(rows)) * (max(columns) - min(columns))
    if i != 0:
        if min_frame > last_frame:
            print(f"The message appears when {i-1} seconds have passed.")
            break
    last_frame = min_frame
    for coords in lines:
        coords[0] += coords[2]
        coords[1] += coords[3]

for coords in lines:
    coords[0] -= coords[2]
    coords[1] -= coords[3]
rows = [x[0] for x in lines]
columns = [x[1] for x in lines]

plt.scatter(rows, columns)
plt.xlim(min(rows), max(rows))
plt.ylim(min(columns), max(columns))
plt.gca().invert_yaxis()
plt.show()
