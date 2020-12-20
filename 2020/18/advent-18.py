import math


class Equation:
    def __init__(self):
        self._exp_list = []

    @classmethod
    def from_string(cls, expression: str):
        open_par = 0
        l_obj = ""
        equation = Equation()
        current_list = equation._exp_list
        for char in expression:
            if char == "(":
                if open_par == 0:
                    current_list = []
                else:
                    l_obj += "("
                open_par += 1
            elif char == ")":
                open_par -= 1
                if open_par == 0:
                    current_list += l_obj
                    l_obj = Equation.from_string(" ".join(current_list))
                    current_list = equation._exp_list
                else:
                    l_obj += ")"
                    current_list.append(l_obj)
                    l_obj = ""
            elif char == " ":
                current_list.append(l_obj)
                l_obj = ""
            else:
                l_obj += char
        current_list.append(l_obj)
        return equation

    @property
    def exp_list(self):
        return [x.evaluate() if isinstance(x, Equation) else x for x in self._exp_list]

    @property
    def adv_exp(self):
        return [
            x.advanced_eval() if isinstance(x, Equation) else x for x in self._exp_list
        ]

    def evaluate(self):
        value = None
        operation = None
        for item in self.exp_list:
            try:
                n = int(item)
            except ValueError:
                if item in {"+", "*"}:
                    operation = item
                    n = None
            finally:
                if n is not None:
                    if value is None:
                        value = n
                    elif operation is not None:
                        if operation == "+":
                            value += n
                        elif operation == "*":
                            value *= n
                        operation = None
        return value

    def advanced_eval(self):
        mult_list = []
        val = None
        for item in self.adv_exp:
            try:
                n = int(item)
            except ValueError:
                if item == "+":
                    val = mult_list.pop()
            else:
                if val:
                    n += val
                    val = None
                mult_list.append(n)
        return math.prod(mult_list)


with open("input.txt") as f:
    equations = [line.strip() for line in f.readlines()]

# part one

answers = []
for e in equations:
    answers.append(Equation.from_string(e).evaluate())
print(sum(answers))

# part two

answers = []
for e in equations:
    answers.append(Equation.from_string(e).advanced_eval())
print(sum(answers))
