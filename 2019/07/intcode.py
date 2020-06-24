class Opcode:
    def __init__(self, code, current_index, memory, input_stack):
        self.code = str(code)
        self.index = current_index
        self.memory = memory
        self.input_stack = input_stack

        parameter_nos = {
            "1": 3,
            "2": 3,
            "3": 1,
            "4": 1,
            "5": 2,
            "6": 2,
            "7": 3,
            "8": 3,
            "99": 0,
        }

        # get parameter modes
        if len(self.code) > 2:
            code_chars = list(self.code)
            self.code = str(int("".join(code_chars[-2:])))
            self.parameter_count = parameter_nos[self.code]
            parmods = code_chars[:-2][::-1]
            spec_length = len(parmods)
            self.parameter_modes = {}
            for i, char in enumerate(parmods):
                if char == "0":
                    self.parameter_modes[i] = "pos"
                elif char == "1":
                    self.parameter_modes[i] = "imm"
            if spec_length < self.parameter_count:
                for x in range(self.parameter_count - spec_length):
                    self.parameter_modes[spec_length + x] = "pos"
        else:
            self.parameter_count = parameter_nos[self.code]
            self.parameter_modes = {x: "pos" for x in range(self.parameter_count)}

        if self.parameter_count > 0:
            self.parameters = self.memory[
                self.index + 1 : self.index + self.parameter_count + 1
            ]
        else:
            self.parameters = None

        if self.code == "3":
            if self.input_stack:
                inp = self.input_stack.pop()
                self.parameters.append(inp)

    def fetch_param(self, n, i):
        if self.parameter_modes[i] == "pos":
            p_val = self.memory[n]
        elif self.parameter_modes[i] == "imm":
            p_val = n
        return p_val

    def run(self):
        def add(n1: int, n2: int, o: int):
            n1 = self.fetch_param(n1, 0)
            n2 = self.fetch_param(n2, 1)
            return self.index + 4, (n1 + n2, o), None

        def multiply(n1: int, n2: int, o: int):
            n1 = self.fetch_param(n1, 0)
            n2 = self.fetch_param(n2, 1)
            return self.index + 4, (n1 * n2, o), None

        def put_in(o: int, i: int):
            return self.index + 2, (i, o), None

        def output(o: int):
            o = self.fetch_param(o, 0)
            return self.index + 2, None, o

        def jump_if_true(n: int, p: int):
            n = self.fetch_param(n, 0)
            p = self.fetch_param(p, 1)
            if n == 0:
                next_point = self.index + 3
            else:
                next_point = p
            return next_point, None, None

        def jump_if_false(n: int, p: int):
            n = self.fetch_param(n, 0)
            p = self.fetch_param(p, 1)
            if n == 0:
                next_point = p
            else:
                next_point = self.index + 3
            return next_point, None, None

        def less_than(n1: int, n2: int, o: int):
            n1 = self.fetch_param(n1, 0)
            n2 = self.fetch_param(n2, 1)
            if n1 < n2:
                put = 1
            else:
                put = 0
            return self.index + 4, (put, o), None

        def equals(n1: int, n2: int, o: int):
            n1 = self.fetch_param(n1, 0)
            n2 = self.fetch_param(n2, 1)
            if n1 == n2:
                put = 1
            else:
                put = 0
            return self.index + 4, (put, o), None

        def halt():
            return "HALT"

        operation = {
            "1": add,
            "2": multiply,
            "3": put_in,
            "4": output,
            "5": jump_if_true,
            "6": jump_if_false,
            "7": less_than,
            "8": equals,
            "99": halt,
        }

        if self.parameters is not None:
            return operation[self.code](*self.parameters)
        else:
            return operation[self.code]()


class Intcode:
    def __init__(self):
        self.memory = []
        self.pointer = 0

    @classmethod
    def read_program(cls, inputfile: str):
        computer = cls()
        with open(inputfile) as f:
            content = f.read()
        computer.memory = [int(x) for x in content.split(",")]
        return computer

    def run_program(self, input_stack=None):
        while True:
            code = Opcode(
                self.memory[self.pointer], self.pointer, self.memory, input_stack
            )
            # print(f"Opcode #{code.code}, parameters: {code.parameters}, modes: {code.parameter_modes}")
            if code.run() == "HALT":
                # print("HALTING PROGRAM")
                break
            else:
                new_pointer, changes, output = code.run()
                if changes is not None:
                    self.memory[changes[1]] = changes[0]
                    # print(f"value at index {changes[1]} changed to {changes[0]}")
                self.pointer = new_pointer
                # print(f"pointer now at {self.pointer}")
                if output is not None:
                    yield output
        return
