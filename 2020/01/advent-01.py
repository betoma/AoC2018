with open("./input.txt", "r") as f:
    content = f.readlines()


numbers = [int(x.strip()) for x in content]
num_set = set(numbers)
numbers.sort()

# part one
for n in numbers:
    v = 2020 - n
    if v in num_set:
        print(n, v)
        break

print(n * v)

# part two
for i, n in enumerate(numbers):
    found = False
    for j in range(1, len(numbers) - i):
        g = numbers[j]
        z = n + g
        v = 2020 - z
        if v in num_set:
            found = True
            print(n, g, v)
            break
    if found:
        break

print(n * g * v)
