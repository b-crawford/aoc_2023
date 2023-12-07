import re
import os
import numpy as np

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_4.txt")) as f:
    data = f.readlines()

parsed = [
    {
        "winning": np.array(re.findall(r"\d+", d.split(":")[1].split("|")[0])).astype(
            int
        ),
        "numbers": np.array(re.findall(r"\d+", d.split(":")[1].split("|")[1])).astype(
            int
        ),
    }
    for d in data
]

n_winning_numbers = [sum([i in d["winning"] for i in d["numbers"]]) for d in parsed]

points = [2 ** (i - 1) if i else 0 for i in n_winning_numbers]
print(sum(points))

# part 2
n_copies = []

for i in range(len(n_winning_numbers)):
    n_copies += [
        sum(
            [(n_winning_numbers[i - j] >= j) * n_copies[i - j] for j in range(1, i + 1)]
        )
        + 1
    ]

print(sum(n_copies))
