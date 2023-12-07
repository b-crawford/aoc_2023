import re
import os
import numpy as np

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_2.txt")) as f:
    data = f.readlines()


# part 1
def parse(string):
    game_id = int(re.findall(r"Game (\d+)", string)[0])
    results = {
        col: np.max(np.array(re.findall(r"(\d+) " + col, string)).astype(int))
        for col in ["blue", "green", "red"]
    }
    return game_id, results


parsed = [parse(d) for d in data]
print(
    sum(
        [id for id, d in parsed if d["red"] < 13 and d["blue"] < 15 and d["green"] < 14]
    )
)

# we can use the same parsed data for part 2
print(sum([np.prod(list(d.values()), axis=0) for _, d in parsed]))
