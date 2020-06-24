from collections import deque

no_of_players = 468
last_marble = 7101000
scores = [0 for x in range(0, no_of_players)]
circle = deque([0])
current_player = 0

for marble in range(1, last_marble + 1):
    current_player += 1
    if current_player == no_of_players:
        current_player = 0
    if marble % 23 == 0:
        circle.rotate(7)
        scores[current_player] += marble + circle.pop()
        circle.rotate(-1)
    else:
        circle.rotate(-1)
        circle.append(marble)

print(f"The winner has a score of {max(scores)}")
