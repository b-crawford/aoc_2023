import re
import os
import numpy as np

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_3.txt")) as f:
    data = f.readlines()

data = [i.replace("\n", "") for i in data]

# Part 1
symbol_locations = [
    (i, string_.span()[0])
    for i, d in enumerate(data)
    for string_ in re.finditer(r"[^\d.]", d)
]


def symbol_loc_to_valid_locations(symbol_loc):
    y_loc = symbol_loc[0]
    x_loc = symbol_loc[1]

    return [(y_loc + i, x_loc + j) for i in range(-1, 2) for j in range(-1, 2)]


valid_locations = []
for symbol in symbol_locations:
    valid_locations += symbol_loc_to_valid_locations(symbol)


numbers = [
    {
        "coords": [(i, j) for j in range(search.span()[0], search.span()[1])],
        "number": int(search.group()),
    }
    for i, d in enumerate(data)
    for search in re.finditer(r"\b\d+\b", d)
]

relevant_numbers = [
    number
    for number in numbers
    if any([i in valid_locations for i in number["coords"]])
]

print(sum([i["number"] for i in relevant_numbers]))


# Part 2

asterisk_locations = [
    (i, string_.span()[0])
    for i, d in enumerate(data)
    for string_ in re.finditer(r"\*", d)
]


def adjacent(loc_1, loc_2):
    return all(np.abs(np.array(loc_1) - np.array(loc_2)) <= 1)


def check_asterisk_is_gear(asterisk_location, numbers):
    adjacency = [
        any(
            [
                adjacent(asterisk_location, number_location)
                for number_location in number["coords"]
            ]
        )
        for number in numbers
    ]
    return sum(np.array(adjacency).astype(int)) == 2


gears = [
    asterisk
    for asterisk in asterisk_locations
    if check_asterisk_is_gear(asterisk, numbers)
]

running_total = 0
for gear in gears:
    relevant_numbers = [
        number
        for number in numbers
        if any(
            [adjacent(gear, number_location) for number_location in number["coords"]]
        )
    ]
    running_total += np.prod([i["number"] for i in relevant_numbers])
print(running_total)
