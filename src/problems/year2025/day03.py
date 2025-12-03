import _io
from functools import lru_cache
from math import inf
from pprint import pprint

from src.common.iterators import ordered_combinations


def parse_input(fp: _io.FileIO):
    banks = []
    for row in fp.readlines():
        banks.append(row.strip())
    return banks


def main(banks: list[str]) -> tuple[int, int]:
    joltages_part1 = []
    joltages_part2 = []
    for bank in banks:
        joltages_part1.append(largest_joltage_part1(bank))
        joltages_part2.append(largest_joltage_part2(bank))
    return (sum(joltages_part1), sum(joltages_part2))


def largest_joltage_part1(bank: str) -> int:
    max_joltage = -inf
    for idx_i in range(len(bank) - 1):
        for idx_j in range(idx_i + 1, len(bank)):
            joltage = int(bank[idx_i] + bank[idx_j])
            if joltage > max_joltage:
                max_joltage = joltage
    return max_joltage


def largest_joltage_part2(bank: str) -> int:
    """We are going to traverse almost (- window size) the whole bank twelves times. We are trying to find the LARGEST
    digit, then the one nearer to the left as possible. Next iteration, we redo the same thing starting from the idx
    of the last digit.
    """
    joltage = []
    idx_min = 0
    for picks_left in range(12, 0, -1):
        # Retrieve the max value possible in this small window
        window = bank[idx_min : len(bank) - picks_left + 1]
        max_value = max(window)
        joltage.append(max_value)

        # Find the index furthest to the left of this max value (.index() returns first found value)
        idx_min += window.index(max_value) + 1

    return int("".join(joltage))
