from itertools import permutations
import intcode

#---part one---#

def part_one():
    finals = []
    for setting in permutations(range(5)):
        a = intcode.Amplifiers("input.txt")
        thrust = a.run(setting)
        finals.append(thrust)

    print(max(finals))

#part_one()

#---part two---#

def part_two():
    finals = []
    for setting in permutations(range(5,10)):
        b = intcode.Amplifiers("input.txt")
        thrust = b.recursive_run(setting)
        finals.append(thrust)
    
    print(max(finals))

part_two()