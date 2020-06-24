from collections import defaultdict
from collections import Counter


def takeFirst(elem):
    return elem[0]


list_of_actions = []

with open("input.txt") as f:
    for line in f:
        the_line = line.split("]", 1)
        date = the_line[0][1:]
        action = the_line[1].strip()
        list_item = [date, action]
        list_of_actions.append(list_item)

chrono_list = sorted(list_of_actions, key=takeFirst)
guard_total = Counter()
guard_minutes = {}

for item in chrono_list:
    splaction = item[1].split()
    if splaction[0] == "Guard":
        current_guard = splaction[1]
        if current_guard not in guard_minutes:
            guard_minutes[current_guard] = Counter()
    if splaction[0] == "falls":
        sleep_start = item[0]
    if splaction[0] == "wakes":
        sleep_end = item[0]
        start_minute = int(sleep_start.split(":", 1)[1])
        end_minute = int(sleep_end.split(":", 1)[1])
        sleep_length = end_minute - start_minute
        guard_total[current_guard] += sleep_length
        for value in range(0, sleep_length):
            minute = start_minute + value
            guard_minutes[current_guard][minute] += 1

sleepiest = guard_total.most_common(1)[0]
sleepy_guard = sleepiest[0]
sleepy_time = sleepiest[1]
sleepy_minute = guard_minutes[sleepy_guard].most_common(1)[0]
actual_minute = sleepy_minute[0]
minute_frequency = sleepy_minute[1]

answer_to_part_one = int(sleepy_guard[1:]) * int(actual_minute)

print(
    "{} slept for {} minutes, and was mostly frequently asleep at 00:{} ({} times).".format(
        sleepy_guard, sleepy_time, actual_minute, minute_frequency
    )
)
print("Answer to part one is {}".format(answer_to_part_one))

# --- part two ---#
most_frequent_minutes = Counter()

for guard in guard_minutes:
    if guard_minutes[guard]:
        freq_min = guard_minutes[guard].most_common(1)[0]
        most_frequent_minutes[(guard, freq_min[0])] = int(freq_min[1])

regularity = most_frequent_minutes.most_common(1)[0]
regular_sleeper = regularity[0][0]
regular_minute = regularity[0][1]
how_often = regularity[1]

answer_to_part_two = int(regular_sleeper[1:]) * int(regular_minute)

print(
    "{} slept at 00:{} most often, {} times.".format(
        regular_sleeper, regular_minute, how_often
    )
)
print("Answer to part two is {}".format(answer_to_part_two))
