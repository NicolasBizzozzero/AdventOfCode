import _io
from functools import lru_cache
from math import inf
from pprint import pprint

from tqdm import tqdm

from src.common.grid import print_grid, iter_grid_idx, grid_iter_adjacent, is_in_bound
from src.common.iterators import ordered_combinations


def parse_input(fp: _io.FileIO):
    fresh_id_ranges = []
    available_ingredients = []
    switch_parsing = False
    for row in fp.readlines():
        if row.strip() == "":
            switch_parsing = True
            continue

        if not switch_parsing:
            min_id, max_id = row.strip().split("-")
            fresh_id_ranges.append((int(min_id), int(max_id)))
        else:
            available_ingredients.append(int(row.strip()))

    return fresh_id_ranges, available_ingredients


def main(params) -> tuple[int, int]:
    fresh_id_ranges, available_ingredients = params
    return (
        part1(fresh_id_ranges, available_ingredients),
        part2(fresh_id_ranges, available_ingredients),
    )


def part1(
    fresh_id_ranges: list[tuple[int, int]], available_ingredients: list[int]
) -> int:
    fresh_ingredients = 0
    for ingredient in available_ingredients:
        if is_fresh(ingredient, fresh_id_ranges):
            fresh_ingredients += 1
    return fresh_ingredients


def part2(
    fresh_id_ranges: list[tuple[int, int]], available_ingredients: list[int]
) -> int:
    # Sort ranges by min_id for easier comparisons
    fresh_id_ranges.sort(key=lambda args: args[0])

    total_fresh_ids = 0
    processed_ranges = []
    for min_id, max_id in tqdm(fresh_id_ranges):
        new_fresh_ids = nb_ids_in_range(min_id, max_id, processed_ranges)
        total_fresh_ids += new_fresh_ids
        processed_ranges.append((min_id, max_id))
    return total_fresh_ids


def is_fresh(ingredient: int, fresh_id_ranges: list[tuple[int, int]]) -> bool:
    for min_id, max_id in fresh_id_ranges:
        if min_id <= ingredient <= max_id:
            return True
    return False


def nb_ids_in_range(
    min_id: int, max_id: int, processed_ranges: list[tuple[int, int]]
) -> int:
    for processed_range in sorted(processed_ranges):
        # Completely outside a range
        if min_id > processed_range[1] or max_id < processed_range[0]:
            continue

        # Partially overlap a range, update ids
        if min_id >= processed_range[0]:
            min_id = processed_range[1] + 1
        if max_id <= processed_range[1]:
            max_id = processed_range[0] - 1

        # If our new range is fucked up, stop early
        if max_id < min_id:
            return 0

    return max_id - min_id + 1
