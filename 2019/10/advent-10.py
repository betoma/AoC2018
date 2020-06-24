from collections import defaultdict, deque
import math

# with open("test.txt") as f:
with open("input.txt") as f:
    content = f.readlines()

asteroids = []

rows = [[x for x in line.strip()] for line in content]
for j, row in enumerate(rows):
    for i, cell in enumerate(row):
        if cell == "#":
            asteroids.append((i, j))

# ---part one---#

sights = {}
number_seen = {}

for aster in asteroids:
    sightlines = defaultdict(list)
    for roid in asteroids:
        if aster != roid:
            theta = math.atan2((roid[1] - aster[1]), (roid[0] - aster[0])) - math.pi / 2
            sightlines[theta].append(roid)
    # print(f"{aster}: {sightlines}")
    sights[aster] = sightlines
    number_seen[aster] = len(sightlines.keys())

best_spot = max(number_seen, key=number_seen.get)
print(f"{best_spot}: {number_seen[best_spot]}")

# ---part two---#
n_roids = len([x for x in asteroids if x != best_spot])
real_sights = sights[best_spot]

angles = [x for x in real_sights]
real_sights = {
    k: sorted(v, key=lambda x: (abs(x[1] - best_spot[1]) + abs(x[0] - best_spot[0])))
    for k, v in real_sights.items()
}
dangle = deque(sorted(angles))
while dangle[0] != -3.141592653589793:
    dangle.rotate(-1)

vaporder = []
while dangle != deque():
    current_angle = dangle[0]
    if real_sights[current_angle] == []:
        dangle.popleft()
    else:
        bang = real_sights[current_angle].pop(0)
        vaporder.append(bang)
    dangle.rotate(-1)

two00th = vaporder[199]
print(two00th, ((two00th[0] * 100) + two00th[1]))

