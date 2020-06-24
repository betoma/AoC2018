from collections import defaultdict

# with open("test-input.txt") as file:
with open("input.txt") as file:
    content = file.read().split("\n")

all_steps = list()
conditions = defaultdict(set)

for line in content:
    words = line.split()
    prereq = words[1]
    step = words[7]
    if step not in all_steps:
        all_steps.append(step)
    if prereq not in all_steps:
        all_steps.append(prereq)
    conditions[step].add(prereq)

total = len(all_steps)
available = set()
steps_taken = list()
completed = set()
i = 0
while i < total:
    for letter in all_steps:
        if conditions[letter] <= completed:
            available.add(letter)
    alphabetical = sorted(available)
    new_step = alphabetical[0]
    available.discard(new_step)
    steps_taken.append(new_step)
    completed.add(new_step)
    all_steps.remove(new_step)
    i += 1

answer = "".join(steps_taken)
print(f"The final result is: {answer}")
