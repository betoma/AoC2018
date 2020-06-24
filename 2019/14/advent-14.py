from collections import defaultdict


def ceil(a, b):
    return -(-a // b)


class Reaction:
    def __init__(self, desc: str):
        def typsep(s: str):
            sep = s.split()
            n = int(sep[0])
            s = sep[1]
            return (n, s)

        splitline = desc.split("=>")
        inp = splitline[0]
        self.input = [typsep(x) for x in inp.split(",")]
        out = splitline[1]
        output = typsep(out)
        self.increment = output[0]
        self.output = output[1]

    def __repr__(self):
        return f"Reaction: {self.output} from {self.input}"


class ReactionChain:
    def __init__(self, filename: str):
        all_reactions = []
        with open(filename) as f:
            content = f.readlines()
        for line in content:
            r = Reaction(line)
            all_reactions.append(r)
        self.reactions = {x.output: (x.increment, x.input) for x in all_reactions}
        self.pantry = defaultdict(int)

    def how_much(self, ingredient, n: int = 1):
        recipe = self.reactions[ingredient]
        already_got = self.pantry.pop(ingredient, 0)
        need = n - already_got
        if need > 0:
            remaining = 0
            batch = (ceil(need, recipe[0]), recipe)
            times = batch[0]
            increment = batch[1][0]
            amounts = batch[1][1]
            requirements = {y: x * times for (x, y) in amounts}
            leftovers = (((times * increment) - need), ingredient)
        else:
            leftovers = (0, ingredient)
            remaining = -need
            requirements = {"ORE": 0}
        ingredients = [*requirements]
        self.pantry[leftovers[1]] = remaining + leftovers[0]
        return requirements, ingredients

    def empty_pantry(self):
        self.pantry = defaultdict(int)

    def how_much_ore(self, ingredient, n: int = 1):
        amounts, components = self.how_much(ingredient, n)
        # print(f"{n} {ingredient} requires {amounts}.")
        # print(f"{self.pantry} leftover.")
        if components.count("ORE") == len(components) and components:
            return amounts["ORE"]
        else:
            sum_list = [self.how_much_ore(x, amounts[x]) for x in components]
            return sum(sum_list)

    def how_much_fuel(self, n: int = 100):
        test_amount = n // self.how_much_ore("FUEL")
        tried = set()
        while True:
            self.empty_pantry()
            actual_amount = self.how_much_ore("FUEL", int(test_amount))
            if actual_amount not in tried:
                tried.add(actual_amount)
            elif actual_amount <= n:
                return int(test_amount)
            multiple = n / actual_amount
            test_amount *= multiple


fu = ReactionChain("input.txt")
# print(fu.how_much_ore('FUEL'))
print(fu.how_much_fuel(1000000000000))

