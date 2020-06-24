from collections import defaultdict

# with open("test-input.txt") as file:
with open("input.txt") as file:
    content = file.read().split("\n")

# Stuff that needs to change depending on test or real input
time_diff = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26,
}
buffer = 60
workers = ["worker_1", "worker_2", "worker_3", "worker_4", "worker_5"]
max_time = 351 + (60 * 26)

all_steps = list()
conditions = defaultdict(set)

# build conditional dependency graph as a dictionary
for line in content:
    words = line.split()
    prereq = words[1]
    step = words[7]
    if step not in all_steps:
        all_steps.append(step)
    if prereq not in all_steps:
        all_steps.append(prereq)
    conditions[step].add(prereq)

steps_left = set(all_steps)
completed = set()
in_progress = set()
available = set()
time_left = dict()
# initialize workers as having no task
current_task = {worker: "not_busy" for worker in workers}

for i in range(0, max_time):
    no_of_seconds = i
    if i == 0:
        for letter in all_steps:
            if letter in steps_left and conditions[letter] <= completed:
                available.add(letter)
    for worker in workers:
        if current_task[worker] == "not_busy":
            if available != set():
                alphabetical = sorted(available)
                new_step = alphabetical[0]
                in_progress.add(new_step)
                current_task[worker] = new_step
                time_left[new_step] = time_diff[new_step] + buffer
                steps_left.remove(new_step)
                available.remove(new_step)
        else:
            current_step = current_task[worker]
            time_left[current_step] -= 1
    for worker, step in current_task.items():
        if step != "not_busy":
            if time_left[step] == 0:
                completed.add(step)
                in_progress.remove(step)
                current_task[worker] = "not_busy"
    for letter in all_steps:
        if letter in steps_left and conditions[letter] <= completed:
            available.add(letter)
    for worker in workers:
        if current_task[worker] == "not_busy" and available != set():
            alphabetical = sorted(available)
            new_step = alphabetical[0]
            in_progress.add(new_step)
            current_task[worker] = new_step
            time_left[new_step] = time_diff[new_step] + buffer
            steps_left.remove(new_step)
            available.remove(new_step)
    # print(f"At second {no_of_seconds}, state is:")
    # print(current_task)
    # print(completed)
    if steps_left == set() and in_progress == set():
        assert completed == set(all_steps), "You've lost some steps, hon."
        break

if no_of_seconds == max_time:
    print("I think something's broken.")
else:
    print(f"It will take {no_of_seconds} to complete all steps.")
