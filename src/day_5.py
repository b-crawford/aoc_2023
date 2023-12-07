import re
import os

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_5.txt")) as f:
    data = f.read()

chunks = data.split("\n\n")

seeds = [int(i) for i in re.findall(r"\d+", chunks[0])]
map_strings = chunks[1:]


class Mapping:
    def __init__(self, map_string):
        self.ranges = []
        for mapping in map_string.split("\n")[1:]:
            values = [int(i) for i in mapping.split(" ")]
            self.ranges += [
                {
                    "source_start": values[1],
                    "map_add": values[0] - values[1],
                    "length": values[2],
                }
            ]

    @staticmethod
    def check_source_in_range(range, source):
        return (
            source >= range["source_start"]
            and source < range["source_start"] + range["length"]
        )

    def find_relevant_range(self, source):
        return [
            range for range in self.ranges if self.check_source_in_range(range, source)
        ]

    @staticmethod
    def map_if_range_relevant(source, range):
        return source + range["map_add"]

    def map(self, source):
        relevant_range = self.find_relevant_range(source)
        if len(relevant_range) == 0:
            return source
        else:
            return self.map_if_range_relevant(source, relevant_range[0])


mappings = [Mapping(map_string) for map_string in map_strings]


def map_seed(source, mappings):
    for mapping in mappings:
        source = mapping.map(source)
    return source


print(min([map_seed(seed, mappings) for seed in seeds]))

# part 2


class QuickRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __repr__(self):
        return f"QuickRange({self.start, self.stop})"

    def min(self):
        return self.start

    def max(self):
        return self.stop - 1

    def __len__(self):
        return self.stop - self.start

    def contains(self, number):
        return number >= self.start and number <= self.stop


expanded_seeds = [
    QuickRange(seeds[2 * i], seeds[2 * i] + seeds[2 * i + 1])
    for i in range(int(len(seeds) / 2))
]


def quick_range_add(quick_range, add):
    return QuickRange(quick_range.min() + add, quick_range.max() + add + 1)


def quick_range_a_contained_in_range_b(range_a, range_b):
    return range_a.min() >= range_b.min() and range_a.max() <= range_b.max()


def break_range(range_, break_points):
    relevant_break_points = [i for i in break_points if range_.contains(i)]
    relevant_break_points.sort()
    range_points = [range_.min()] + relevant_break_points + [range_.max() + 1]

    out_ranges = []
    for i in range(len(range_points) - 1):
        out_ranges += [QuickRange(range_points[i], range_points[i + 1])]

    return out_ranges


class Mapping:
    def __init__(self, source_range, map_add):
        self.source_range = source_range
        self.map_add = map_add

    def __repr__(self):
        return f"Mapping from {self.source_range} by adding {self.map_add};"

    def break_apart(self, break_points):
        out_ranges = break_range(self.source_range, break_points)

        return [Mapping(range_, self.map_add) for range_ in out_ranges]

    def __len__(self):
        return len(self.source_range)

    def map_range(self, range_):
        if quick_range_a_contained_in_range_b(range_, self.source_range):
            return quick_range_add(range_, self.map_add)
        elif not (
            (range_.min() > self.source_range.max())
            or (range_.max() < self.source_range.min())
        ):
            error_string = "Method not designed to handle overlap, use break first. \n"
            error_string += f"{self}" + "\n"
            error_string += f"Range {range_}"
            raise ValueError(error_string)
        else:
            return None


def parse_mapping_collection(map_string):
    out_mappings = []
    for mapping in map_string.split("\n")[1:]:
        values = [int(i) for i in mapping.split(" ")]
        out_mappings += [
            Mapping(QuickRange(values[1], values[1] + values[2]), values[0] - values[1])
        ]

    return out_mappings


def mapping_collection_source_range(mapping_collection, range_):
    for mapping in mapping_collection:
        mapped = mapping.map_range(range_)
        if mapped is not None:
            return mapped
    return range_


def mapping_collection_source_ranges(mapping_collection, source_ranges):
    # first take the ranges and break them into chunks based on the mappings
    break_points = [mapping.source_range.min() for mapping in mapping_collection] + [
        mapping.source_range.max() + 1 for mapping in mapping_collection
    ]
    broken_ranges = [
        i
        for sublist in [
            break_range(source_range, break_points) for source_range in source_ranges
        ]
        for i in sublist
        if len(i)
    ]
    out_ranges = [
        mapping_collection_source_range(mapping_collection, source_range)
        for source_range in broken_ranges
    ]
    return out_ranges


mapping_collections = [
    parse_mapping_collection(map_string) for map_string in map_strings
]

ranges = expanded_seeds
for mapping_collection in mapping_collections:
    ranges = mapping_collection_source_ranges(mapping_collection, ranges)

print(min([i.min() for i in ranges]))
