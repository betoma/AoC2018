class Intcode:
    def __init__(self, initial: list):
        self.memory = initial

    def run(self):
        ip = 0
        while True:
            try:
                opcode = self.memory[ip]
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
                        next_ip = self.addition(ip, modes)
                    elif code == 2:
                        next_ip = self.multiplication(ip, modes)
                    elif code == 3:
                        next_ip = self.from_input(ip)
                    elif code == 4:
                        next_ip = self.output(ip, modes)
                    elif code == 5:
                        next_ip = self.jump_if_true(ip, modes)
                    elif code == 6:
                        next_ip = self.jump_if_false(ip, modes)
                    elif code == 7:
                        next_ip = self.less_than(ip, modes)
                    elif code == 8:
                        next_ip = self.equals(ip, modes)
                    ip = next_ip

    @staticmethod
    def _key_modes(modes_lst: list, instr_length):
        while len(modes_lst) < instr_length:
            modes_lst.append(0)

    def addition(self, ip, modes):
        self._key_modes(modes, 3)
        i = self.memory[ip + 1]
        j = self.memory[ip + 2]
        o = self.memory[ip + 3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        self.memory[o] = i + j
        return ip + 4

    def multiplication(self, ip, modes):
        self._key_modes(modes, 3)
        i = self.memory[ip + 1]
        j = self.memory[ip + 2]
        o = self.memory[ip + 3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        self.memory[o] = i * j
        return ip + 4

    def from_input(self, ip):
        i = input("Please input an integer: ")
        o = self.memory[ip + 1]
        self.memory[o] = int(i)
        return ip + 2

    def output(self, ip, modes):
        self._key_modes(modes, 1)
        o = self.memory[ip + 1]
        if modes[0] == 0:
            o = self.memory[o]
        print(f"Output: {o}")
        return ip + 2

    def jump_if_true(self, ip, modes):
        self._key_modes(modes, 2)
        i = self.memory[ip + 1]
        o = self.memory[ip + 2]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            o = self.memory[o]
        if i == 0:
            return ip + 3
        else:
            return o

    def jump_if_false(self, ip, modes):
        self._key_modes(modes, 2)
        i = self.memory[ip + 1]
        o = self.memory[ip + 2]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            o = self.memory[o]
        if i == 0:
            return o
        else:
            return ip + 3

    def less_than(self, ip, modes):
        self._key_modes(modes, 2)
        i = self.memory[ip + 1]
        j = self.memory[ip + 2]
        op = self.memory[ip + 3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        if i < j:
            o = 1
        else:
            o = 0
        self.memory[op] = o
        return ip + 4

    def equals(self, ip, modes):
        self._key_modes(modes, 2)
        i = self.memory[ip + 1]
        j = self.memory[ip + 2]
        op = self.memory[ip + 3]
        if modes[0] == 0:
            i = self.memory[i]
        if modes[1] == 0:
            j = self.memory[j]
        if i == j:
            o = 1
        else:
            o = 0
        self.memory[op] = o
        return ip + 4


with open("input.txt") as f:
    content = f.readlines()

initial = [int(x) for line in content for x in line.split(",")]
program = Intcode(initial)
program.run()
