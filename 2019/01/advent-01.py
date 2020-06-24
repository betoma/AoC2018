def mass_calc(n: int):
    mass = (n // 3) - 2
    if mass > 0:
        return mass
    else:
        return 0


def fuel_calc(n: int):
    mass = 0
    further_fuel_needed = mass_calc(n)
    while further_fuel_needed != 0:
        mass += further_fuel_needed
        further_fuel_needed = mass_calc(further_fuel_needed)
    return mass


with open("input.txt") as f:
    content = f.readlines()

mass = sum([fuel_calc(int(x)) for x in content])
print(mass)
