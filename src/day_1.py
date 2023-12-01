import re
import os

main_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(main_dir, "data/day_1.txt")) as f:
    data = f.readlines()

# part 1
digits = [re.findall(r"\d", s) for s in data]
values = [int(digit[0] + digit[-1]) for digit in digits]
print(sum(values))

# part two
digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

# Searching for 'one|two' (as in part i) on 'twone' will only return ['two']
# but we want ['two', 'one']. To do this you have to
# search for '(?=(one|two))'
find_string = r"(?=(\d|" + "|".join(digit_map.keys()) + "))"
digits = [re.findall(find_string, s) for s in data]
digits_as_symbols = [
    [digit_map[digit] if digit in digit_map.keys() else digit for digit in digit_list]
    for digit_list in digits
]
values = [int(digit[0] + digit[-1]) for digit in digits_as_symbols]
print(sum(values))
