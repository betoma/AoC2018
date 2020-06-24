from collections import Counter

# with open("test.txt") as f:
with open("input.txt") as f:
    content = f.readlines()

orbits = [line.strip().split(")") for line in content]

orbit_chain = {}
for orbit in orbits:
    orbit_chain[orbit[1]] = orbit[0]


def orbit_list(chain: dict, start: str):
    orbits = []
    body = start
    while body in chain:
        orbits.append(body)
        body = chain[body]
    return orbits


def lowest_common_orbit(body_1: str, body_2: str, chain: dict):
    lco = None
    list_1 = orbit_list(chain, body_1)
    list_2 = set(orbit_list(chain, body_2))
    for body in list_1:
        if body in list_2:
            lco = body
            break
    return lco


def count_orbits(chain: dict, until: str = "COM"):
    orbit_count = Counter()
    for body in chain:
        orbit_count[body] += 1
        parent = chain[body]
        while parent != until:
            orbit_count[body] += 1
            try:
                parent = chain[parent]
            except KeyError:
                break
    return orbit_count


# part one
print(sum(count_orbits(orbit_chain).values()))

# part two
branch = lowest_common_orbit("YOU", "SAN", orbit_chain)
to_branch = count_orbits(orbit_chain, until=branch)
print(to_branch[orbit_chain["SAN"]] + to_branch[orbit_chain["YOU"]])

