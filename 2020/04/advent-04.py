import re


def process_file(filename: str):
    with open(filename, "r") as f:
        contents = f.readlines()
    list_of_documents = []
    document = {}
    for line in contents:
        if line == "\n":
            list_of_documents.append(document)
            document = {}
        else:
            sections = line.strip().split()
            for s in sections:
                field, value = s.split(":")
                document[field] = value
    list_of_documents.append(document)
    return list_of_documents


pass_list = process_file("input.txt")

# part one


def has_all_required_fields(document: dict):
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return required_fields <= set(document)


print([has_all_required_fields(p) for p in pass_list].count(True))

# part two


def has_good_data(document: dict):
    if not has_all_required_fields(document):
        return False
    try:
        byr = int(document["byr"])
        iyr = int(document["iyr"])
        eyr = int(document["eyr"])
    except ValueError:
        return False
    if byr < 1920 or byr > 2002:
        return False
    if iyr < 2010 or iyr > 2020:
        return False
    if eyr < 2020 or eyr > 2030:
        return False
    try:
        height = int(document["hgt"][:-2])
        unit = document["hgt"][-2:]
    except ValueError:
        return False
    if unit == "cm":
        if height < 150 or height > 193:
            return False
    elif unit == "in":
        if height < 59 or height > 76:
            return False
    else:
        return False
    if len(document["hcl"]) == 7:
        if document["hcl"].startswith("#"):
            if bool(re.match(r"[^a-f0-9]", document["hcl"][1:])):
                return False
        else:
            return False
    else:
        return False
    if document["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False
    if len(document["pid"]) == 9:
        try:
            _ = int(document["pid"])
        except ValueError:
            return False
    else:
        return False
    return True


print([has_good_data(p) for p in pass_list].count(True))
