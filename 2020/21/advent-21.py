from collections import Counter
from typing import List


class Food:
    def __init__(self, ingredients: List[str], allergens: List[str]):
        self.ingredients = set(ingredients)
        self.allergens = set(allergens)

    def __repr__(self):
        return f"{self.ingredients} (contains {self.allergens})"

    @classmethod
    def from_string(cls, string: str):
        """
        string of the form:
        ingredient ingredient ingredient (contains allergen, allergen)
        """
        ing_str, all_str = string.split(" (contains ")
        allergens = all_str.strip(")").split(", ")
        ingredients = ing_str.split(" ")
        return cls(ingredients, allergens)


class Menu:
    def __init__(self, food_list: List[Food]):
        self.items = food_list

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            content = [x.strip() for x in f.readlines()]
        return cls([Food.from_string(line) for line in content])

    @property
    def all_ingredients(self):
        return set([x for item in self.items for x in list(item.ingredients)])

    def possibility_table(self):
        table = {}
        for item in self.items:
            for allergen in list(item.allergens):
                if allergen in table:
                    table[allergen] = table[allergen] & item.ingredients
                else:
                    table[allergen] = item.ingredients
        return table

    def potential_allergens(self):
        return set([x for k, v in self.possibility_table().items() for x in list(v)])

    @property
    def safe_ingredients(self):
        return self.all_ingredients - self.potential_allergens()

    def ingredient_count(self):
        return Counter([x for item in self.items for x in list(item.ingredients)])


foodlist = Menu.from_file("input.txt")

# part one
count = foodlist.ingredient_count()
print(sum([count[x] for x in foodlist.safe_ingredients]))

# part two
possibilities = foodlist.possibility_table()
official = {}
while possibilities:
    for key in list(possibilities.keys()):
        if len(possibilities[key]) == 1:
            the_ingredient = possibilities.pop(key).pop()
            for k, v in possibilities.items():
                v.discard(the_ingredient)
            official[the_ingredient] = key

print(",".join(sorted(list(official.keys()), key=lambda x: official[x])))
