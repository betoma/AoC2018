import itertools

# import matplotlib.pyplot as plt


class Pot:
    def __init__(self, value=".", placement=None):
        if value in {"#", "."}:
            self.value = value
        else:
            raise ValueError("Pot value must be either a Boolean or one of {'#', '.'}")
        self.place = placement

    def has_plant(self):
        if self.value == "#":
            return True
        else:
            return False


class GrowRule:
    def __init__(self, placement_input, output):
        assert len(placement_input) == 5
        assert len(output) == 1
        self.full_rule = f"{placement_input} => {output}"
        self.current = placement_input[2]
        self.left = placement_input[1]
        self.far_left = placement_input[0]
        self.right = placement_input[3]
        self.far_right = placement_input[4]
        self.output = output
        self.leftside = f"{self.far_left}{self.left}"
        self.rightside = f"{self.right}{self.far_right}"

    def applies_at_leftmost(self):
        if self.current == "." and self.leftside == "..":
            return True
        else:
            return False

    def applies_at_rightmost(self):
        if self.current == "." and self.rightside == "..":
            return True
        else:
            return False

    def fits_current(self, value):
        if self.current == value:
            return True
        else:
            return False

    def fits_left(self, leftwards):
        if type(leftwards) == list:
            leftwards = "".join(leftwards)
        if leftwards == self.leftside:
            return True
        else:
            return False

    def fits_right(self, rightwards):
        if type(rightwards) == list:
            rightwards = "".join(rightwards)
        if rightwards == self.rightside:
            return True
        else:
            return False

    def fits(self, value, leftwards, rightwards):
        if (
            self.fits_current(value)
            and self.fits_left(leftwards)
            and self.fits_right(rightwards)
        ):
            return True
        else:
            return False


class RowofPots:
    def __init__(self, initial, list_of_rules):
        all_contexts = set(
            ["".join(x) for x in itertools.product(["#", "."], repeat=5)]
        )
        self.pots = list()
        self.rules = list()
        for index, pot in enumerate(initial):
            this_pot = Pot(value=pot, placement=index)
            self.pots.append(this_pot)
        for rule in list_of_rules:
            rule_set = rule.split()
            this_rule = GrowRule(rule_set[0], rule_set[2])
            self.rules.append(this_rule)
            all_contexts.remove(rule_set[0])
        if all_contexts is not set():
            for context in all_contexts:
                this_rule = GrowRule(context, ".")
                self.rules.append(this_rule)

    def pot_at_place(self, place):
        for pot in self.pots:
            if pot.place == place:
                return pot

    def over_time(self, no_of_generations):
        self.gen = 0
        for _ in range(0, no_of_generations):
            if self.gen == 0:
                last_gen = self.pots
            else:
                plant_list = self.show_pots(next_gen)
                first_plant = plant_list.index("#")
                last_plant = len(plant_list) - 1 - plant_list[::-1].index("#")
                last_gen = next_gen[first_plant : last_plant + 1]
            next_gen = list()
            self.gen += 1
            gen_length = len(last_gen)
            last_pot = gen_length - 1
            penult_pot = gen_length - 2
            for rule in self.rules:
                if rule.applies_at_leftmost():
                    if rule.fits_right(f"{last_gen[0].value}{last_gen[1].value}"):
                        first_pot = last_gen[0].place
                        new_pot = Pot(rule.output, placement=first_pot - 1)
                        next_gen.append(new_pot)
                        break
            for index, pot in enumerate(last_gen):
                new_state = pot
                if index < 2:
                    left_two = "."
                    if index == 0:
                        left_one = "."
                    elif index == 1:
                        left_one = last_gen[0].value
                else:
                    left_two = last_gen[index - 2].value
                    left_one = last_gen[index - 1].value
                if index > gen_length - 3:
                    right_two = "."
                    if index == last_pot:
                        right_one = "."
                    elif index == penult_pot:
                        right_one = last_gen[last_pot].value
                else:
                    right_one = last_gen[index + 1].value
                    right_two = last_gen[index + 2].value
                left_side = f"{left_two}{left_one}"
                right_side = f"{right_one}{right_two}"
                #  print(f"index #{index}, current pot: {pot.value}, left: {left_side}, right: {right_side}")
                for rule in self.rules:
                    #  print(f"rule: {rule.full_rule}")
                    if rule.fits(pot.value, left_side, right_side):
                        # print("Fits! output: {rule.output}")
                        new_state = Pot(value=rule.output, placement=pot.place)
                        break
                    # else:
                    # print(f"Doesn't fit.")
                next_gen.append(new_state)
            for rule in self.rules:
                if rule.applies_at_rightmost():
                    if rule.fits_left(
                        f"{last_gen[penult_pot].value}{last_gen[last_pot].value}"
                    ):
                        final_place = last_gen[last_pot].place
                        new_pot = Pot(rule.output, placement=final_place + 1)
                        next_gen.append(new_pot)
            yield next_gen

    @staticmethod
    def show_pots(list_of_pots):
        return [x.value for x in list_of_pots]

    @staticmethod
    def sum_of_plants(list_of_pots):
        sum = 0
        for x in list_of_pots:
            if x.has_plant():
                sum += 1
        return sum

    @staticmethod
    def sum_of_plant_nos(list_of_pots):
        sum = 0
        for x in list_of_pots:
            if x.has_plant():
                sum += x.place
        return sum


# with open("test.txt") as f:
with open("input.txt") as f:
    content = f.read()

lines = content.splitlines()
initial = [char for char in lines[0].split()[2]]
rules = [line for line in lines[1:] if line is not ""]

underground = RowofPots(initial, rules)
count_per_round = []
for g in underground.over_time(200):
    count_per_round.append(underground.sum_of_plant_nos(g))
differences = [
    (x - count_per_round[i - 1]) for i, x in enumerate(count_per_round) if i > 0
]
# plot = plt.figure()
# plt.plot(range(1,200),differences,'ro',range(1,200),differences,'k')
# plt.xlabel('generation')
# plt.ylabel('difference in plant sum')
# plt.show()
print((50000000000 - 142) * 32 + 4945)

