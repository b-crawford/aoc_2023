import re
import os
import numpy as np

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_6.txt")) as f:
    data = f.readlines()

time, distance = [np.array(re.findall(r"\d+", i)).astype(int) for i in data]


def time_and_distance_to_number_of_ways(time, distance):
    # use the quadratic forumla
    start, end = (time - np.sqrt(np.square(time) - 4 * distance)) / 2, (
        time + np.sqrt(np.square(time) - 4 * distance)
    ) / 2

    # round up or down
    start_round, end_round = np.ceil(start), np.floor(end)

    # if it was already and integer go to the next one
    start_round, end_round = start_round + (start_round == start), end_round - (
        end_round == end
    )

    return np.prod(end_round - start_round + 1)


print(time_and_distance_to_number_of_ways(time, distance))

# part 2
time, distance = [re.findall(r"\d+", i) for i in data]
time = int("".join(time))
distance = int("".join(distance))

print(time_and_distance_to_number_of_ways(time, distance))
