def differentCase(str1, str2):
    if str1.islower():
        if str2.isupper():
            return True
        else:
            return False
    elif str1.isupper():
        if str2.islower():
            return True
        else:
            return False


with open("input.txt") as file:
    content = file.read()
# content = "dabAcCaCBAcCcaDA" #test case
each_unit_type = set()
unit_removal = {}

content_list = list(content.strip())

for unit in content_list:
    each_unit_type.add(unit.lower())

for item in each_unit_type:
    polymer = content_list
    #    print("Test removing {} from list.".format(item))
    fresh_polymer = []
    for unit in polymer:
        if unit.lower() != item:
            fresh_polymer.append(unit)
    polymer = fresh_polymer
    while True:
        length = len(polymer)
        changes_count = 0
        pair_deleted = False
        next_polymer = []
        for index, unit in enumerate(polymer):
            # print("Analyzing index {} -- {}".format(index, unit))
            this_unit = polymer[index]
            if pair_deleted:
                # print("Unit was deleted by previous step. Deleting {}.".format(unit))
                pair_deleted = False
            elif index == length - 1:
                # print("Unit is the undeleted final unit. Not deleting.")
                next_polymer.append(this_unit)
            else:
                next_unit = polymer[index + 1]
                # print("Comparing current unit {} with next unit {}".format(this_unit, next_unit))
                if (this_unit.lower() == next_unit.lower()) and (
                    differentCase(this_unit, next_unit)
                ):
                    # print("Units are of the same type and opposite polarity. Deleting {}.".format(this_unit))
                    pair_deleted = True
                    changes_count += 1
                else:
                    # print("Units are not deleted.")
                    next_polymer.append(this_unit)
        # print("".join(next_polymer))
        polymer = next_polymer
        # print("".join(polymer))
        if changes_count == 0:
            # print("No remaining units to delete. Terminating.")
            break
        else:
            # print("Finished with entirety of polymer. Beginning again.")
            continue
    polymer_length = len(polymer)
    # print("Final polymer is {} -- {}".format(("".join(polymer)),polymer_length))
    unit_removal[item] = polymer_length

ordered_list_of_results = [
    (thing, unit_removal[thing]) for thing in sorted(unit_removal, key=unit_removal.get)
]
print(ordered_list_of_results[0])

