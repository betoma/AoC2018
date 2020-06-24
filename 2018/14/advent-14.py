class Elf:
    def __init__(self, recipe, index):
        self.current_recipe = recipe
        self.recipe_index = index

    def __repr__(self):
        return f"Elf({self.current_recipe}, {self.recipe_index})"

    def choose_recipe(self, list_of_recipes):
        current_index = self.recipe_index
        number_of_steps = 1 + self.current_recipe
        list_size = len(list_of_recipes)
        if (number_of_steps + current_index) >= list_size:
            new_index = number_of_steps - (list_size - current_index)
            while new_index > list_size:
                new_index -= list_size
        else:
            new_index = number_of_steps + current_index
        self.current_recipe = list_of_recipes[new_index]
        self.recipe_index = new_index


class RecipeList:
    def __init__(self, no_of_elves, starting_list):
        self.elf_list = list()
        for e in range(no_of_elves):
            elf = Elf(starting_list[e], e)
            self.elf_list.append(elf)
        self.recipes = starting_list

    def __repr__(self):
        return f"RecipeList({self.recipes}, {self.elf_list})"

    def add_recipes(self):
        recipe_ratings = [elf.current_recipe for elf in self.elf_list]
        the_sum = sum(recipe_ratings)
        new_ratings = [int(i) for i in str(the_sum)]
        self.recipes.extend(new_ratings)

    def experiment(self, n):
        while len(self.recipes) < n:
            yield self
            self.add_recipes()
            for elf in self.elf_list:
                elf.choose_recipe(self.recipes)

    def next_ten(self, n):
        final_state = list(self.experiment(n + 10))[-1]
        return final_state.recipes[n : n + 10]

    def first_encounter(self, the_input: list):
        length = len(the_input)
        for round in self.experiment(1000000000):
            recipes = round.recipes
            how_many = len(recipes)
            i = how_many - length
            j = i - 1
            if recipes[i:] == the_input:
                return i
            elif recipes[j:-1] == the_input:
                return j


the_start = RecipeList(2, [3, 7])
# print(the_start.next_ten(260321))
print(the_start.first_encounter([2, 6, 0, 3, 2, 1]))

