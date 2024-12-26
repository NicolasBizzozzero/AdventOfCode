""" Day 3: Rucksack Reorganization

One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

    The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
    The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
    The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
    The fourth rucksack's compartments only share item type v.
    The fifth rucksack's compartments only share item type t.
    The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
"""

import copy
import os
from more_itertools import chunked


PATH_DIR_INPUT = "res"
PATH_FILE_INPUT = os.path.join(
    PATH_DIR_INPUT, f"{__file__.split('/')[-1].split('_')[0]}_input.txt"
)


def main():
    problem = parse_input(path_file_input=PATH_FILE_INPUT)

    part1(problem=copy.deepcopy(problem))
    part2(problem=chunked(copy.deepcopy(problem), 3))


def part1(problem):
    total_priorities = sum(
        list(
            map(
                lambda rucksack: sum(
                    map(
                        lambda item: item_to_priority(item),
                        inter_compartiments(*rucksack),
                    )
                ),
                problem,
            )
        )
    )

    print("Problem 1")
    print("  Total priorities:", total_priorities)


def part2(problem):
    all_badges = []
    for elves in problem:
        # Concatenate the two compartiments
        elves = list(map(lambda rutsack: rutsack[0] + rutsack[1], elves))

        all_badges.append(inter_rutsacks(*elves).pop())

    # Compute sum of priorities of all badges
    total_priorities = sum(map(lambda badge: item_to_priority(badge), all_badges))

    print("Problem 2")
    print("  Total priorities:", total_priorities)


def parse_input(path_file_input: str):
    problem = []

    with open(path_file_input) as fp:
        for line in fp:
            line = line.strip()
            if len(line) != 0:
                compartiment1, compartiment2 = (
                    line[: len(line) // 2],
                    line[len(line) // 2 :],
                )
                problem.append([compartiment1, compartiment2])
    return problem


def inter_compartiments(compartiment1, compartiment2) -> set[str]:
    compartiment1, compartiment2 = set(compartiment1), set(compartiment2)
    return compartiment1.intersection(compartiment2)


def inter_rutsacks(*rutsacks) -> set[str]:
    intersection = set(rutsacks[0])
    for rutsack in rutsacks[1:]:
        intersection = intersection.intersection(set(rutsack))
    return intersection


def item_to_priority(item: str) -> int:
    if item.islower():
        return ord(item) - 96  # ord('a') - 1
    else:
        return ord(item) - 38  # ord('A') - 1 - 26


if __name__ == "__main__":
    main()
