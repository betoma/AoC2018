from itertools import permutations
from intcode import Intcode


class Amplifiers:
    def __init__(self, inputfile):
        self.amplifiers = [
            Intcode.read_program(inputfile),
            Intcode.read_program(inputfile),
            Intcode.read_program(inputfile),
            Intcode.read_program(inputfile),
            Intcode.read_program(inputfile),
        ]

    def run(self, phase_settings=None, input_signal=0):
        next_in = input_signal
        for i, amp in enumerate(self.amplifiers):
            if phase_settings is not None:
                stack = [next_in, phase_settings[i]]
            else:
                stack = [next_in]
            program = amp.run_program(stack)
            next_in = next(program)
        return next_in

    def recursive_run(self, phase_settings, input_signal=0):
        lastE = self.run(phase_settings, input_signal)
        while True:
            # print(f"IN SIGNAL: {lastE}")
            try:
                lastE = self.run(input_signal=lastE)
            except StopIteration:
                break
            # else:
            #    print(f"OUT SIGNAL: lastE")
        return lastE


# ---part one---#


def part_one():
    finals = []
    for setting in permutations(range(5)):
        a = Amplifiers("input.txt")
        thrust = a.run(setting)
        finals.append(thrust)

    print(max(finals))


# part_one()

# ---part two---#


def part_two():
    finals = []
    for setting in permutations(range(5, 10)):
        b = Amplifiers("input.txt")
        thrust = b.recursive_run(setting)
        finals.append(thrust)

    print(max(finals))


part_two()
