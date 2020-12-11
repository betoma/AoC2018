import copy


class Handheld:
    def __init__(self, filename: str):
        with open(filename) as f:
            contents = [line.split(" ", 1) for line in f.readlines()]
        self.instructions = [(line[0], int(line[1].strip())) for line in contents]
        self.pointer = 0
        self.accumulator = 0

    def acc(self, n):
        self.accumulator += n
        self.pointer += 1

    def jmp(self, n):
        self.pointer += n

    def nop(self, *args):
        self.pointer += 1

    def execute(self, instr: tuple):
        if (i := instr[0]) == "acc":
            operation = self.acc
        elif i == "jmp":
            operation = self.jmp
        elif i == "nop":
            operation = self.nop
        operation(instr[1])

    def run_debug(self):
        run_log = [False for x in self.instructions]
        while True:
            if self.pointer == len(self.instructions):
                terminates = True
                break
            elif run_log[self.pointer]:
                terminates = False
                break
            else:
                run_log[self.pointer] = True
                self.execute(self.instructions[self.pointer])
        return terminates, self.accumulator

    def code_repair(self):
        possible_fixes = [
            i
            for i, instr in enumerate(self.instructions)
            if instr[0] == "jmp" or instr[0] == "nop"
        ]
        original_instr = copy.deepcopy(self.instructions)
        for i in possible_fixes:
            self.pointer = 0
            self.accumulator = 0
            self.instructions = [n for n in original_instr]
            if original_instr[i][0] == "nop":
                self.instructions[i] = ("jmp", original_instr[i][1])
            elif original_instr[i][0] == "jmp":
                self.instructions[i] = ("nop", original_instr[i][1])
            debugging = self.run_debug()
            if debugging[0]:
                return debugging[1]
        print("Something's borked!")
        return


system = Handheld("input.txt")

# part one

print(system.run_debug()[1])


# part two

print(system.code_repair())
