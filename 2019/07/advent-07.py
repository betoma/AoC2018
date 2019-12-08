from itertools import permutations
from operator import itemgetter

class Intcode:
    def __init__(self,initial:list):
        self.memory = initial
        self.pointer = 0

    def run(self,inputs):
        outputs = []
        while True:
            try:
                opcode = self.memory[self.pointer]
            except IndexError:
                print("Something's borked!")
                break
            else:
                if opcode == 99:
                    break
                else:
                    string_rep = str(opcode)
                    chars = len(string_rep)
                    if chars > 1:
                        code = int(string_rep[-2:])
                        modes = [int(x) for x in string_rep[:-2][::-1]]
                    else:
                        code = opcode
                        modes = []
                    if code == 1:
                        next_ip = self.addition(modes)
                    elif code == 2:
                        next_ip = self.multiplication(modes)
                    elif code == 3:
                        inp = inputs.pop()
                        next_ip = self.from_input(inp)
                    elif code == 4:
                        output, next_ip = self.output(modes)
                        outputs.append(output)
                    elif code == 5:
                        next_ip = self.jump_if_true(modes)
                    elif code == 6:
                        next_ip = self.jump_if_false(modes)
                    elif code == 7:
                        next_ip = self.less_than(modes)
                    elif code == 8:
                        next_ip = self.equals(modes)
                    self.pointer = next_ip
        return outputs

    @staticmethod
    def _key_modes(modes_lst:list, instr_length):
        while len(modes_lst) < instr_length:
            modes_lst.append(0)

    def addition(self,modes):
        self._key_modes(modes, 3)
        i = self.memory[self.pointer+1]
        j = self.memory[self.pointer+2]
        o = self.memory[self.pointer+3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        self.memory[o] = i+j
        return self.pointer+4

    def multiplication(self,modes):
        self._key_modes(modes,3)
        i = self.memory[self.pointer+1]
        j = self.memory[self.pointer+2]
        o = self.memory[self.pointer+3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        self.memory[o] = i*j
        return self.pointer+4
    
    def from_input(self,inp):
        if inp is None:
            inp = input("Please input an integer: ")
        o = self.memory[self.pointer+1]
        self.memory[o] = int(inp)
        return self.pointer+2
    
    def output(self,modes):
        self._key_modes(modes,1)
        o = self.memory[self.pointer+1]
        if modes[0] == 0:
            o = self.memory[o]
        return o, self.pointer+2
    
    def jump_if_true(self,modes):
        self._key_modes(modes,2)
        i = self.memory[self.pointer+1]
        o = self.memory[self.pointer+2]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            o = self.memory[o]
        if i == 0:
            return self.pointer+3
        else:
            return o

    def jump_if_false(self,modes):
        self._key_modes(modes,2)
        i = self.memory[self.pointer+1]
        o = self.memory[self.pointer+2]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            o = self.memory[o]
        if i == 0:
            return o
        else:
            return self.pointer+3

    def less_than(self,modes):
        self._key_modes(modes,2)
        i = self.memory[self.pointer+1]
        j = self.memory[self.pointer+2]
        op = self.memory[self.pointer+3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        if i < j:
            o = 1
        else:
            o = 0
        self.memory[op] = o
        return self.pointer+4

    def equals(self,modes):
        self._key_modes(modes,2)
        i = self.memory[self.pointer+1]
        j = self.memory[self.pointer+2]
        op = self.memory[self.pointer+3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        if i == j:
            o = 1
        else:
            o = 0
        self.memory[op] = o
        return self.pointer+4

class AmpChain:
    def __init__(self,initial:list):
        self.amps = [
            Intcode(initial),
            Intcode(initial),
            Intcode(initial),
            Intcode(initial),
            Intcode(initial)
        ]
    
    def runthrough(self,settings:tuple,initial:int):
        o = initial
        for i, a in enumerate(self.amps):
            print(i,a,o)
            o = a.run([o,settings[i]])[0]
        return o

#with open("test.txt") as f:
with open("input.txt") as f:
    content = f.readlines()

initial = [int(x) for line in content for x in line.split(',')]


#---part one---#
finals = []
for setting in permutations(range(5)):
    amps = AmpChain(initial)
    thrust = amps.runthrough(setting,0)
    finals.append((setting,thrust))

print(max(finals,key=itemgetter(1)))