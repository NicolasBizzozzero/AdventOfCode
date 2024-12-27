import copy
from collections import Counter, defaultdict


def parse_input(data: str):
    return data.split("\n")


def main(text_file: list[str]) -> tuple[int, int]:

    return (
        level1(text_file=copy.deepcopy(text_file)),
        level2(text_file=copy.deepcopy(text_file)),
    )


def level1(text_file: list[str]) -> int:
    nice_strings = 0
    for string in text_file:
        nice_strings += is_nice(string=string)
    return nice_strings


def level2(text_file: list[str]) -> int:
    nice_strings = 0
    for string in text_file:
        nice_strings += is_nice_better(string=string)
    return nice_strings


def is_nice(string: str) -> bool:
    for naughty_substring in ("ab", "cd", "pq", "xy"):
        if naughty_substring in string:
            return False

    # Check for letter appearing twice in a row
    for i in range(len(string) - 1):
        if string[i] == string[i + 1]:
            break
    else:
        return False

    counter = Counter(string)
    vowels = counter["a"] + counter["e"] + counter["i"] + counter["o"] + counter["u"]
    return vowels >= 3


def is_nice_better(string: str) -> bool:
    # Check for letter which repeats with exactly one letter inbetween
    for i in range(len(string) - 2):
        if string[i] == string[i + 2] and string[i] != string[i + 1]:
            break
    else:
        return False

    # Check for a pair of any two letters that appears at least twice in the string without overlapping
    seen_pairs = defaultdict(list)
    for i in range(len(string) - 1):
        pair = string[i : i + 2]

        # Check for at least one letter between pairs
        if pair in seen_pairs:
            if pair[0] != pair[1]:
                return True

            for old_pair in seen_pairs[pair]:
                if old_pair < i - 1:
                    return True
        seen_pairs[pair].append(i)
    return False
