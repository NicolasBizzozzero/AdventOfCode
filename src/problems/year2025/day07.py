import _io
from functools import lru_cache
from math import inf
from pprint import pprint

from tqdm import tqdm

from src.common.grid import print_grid, iter_grid_idx, grid_iter_adjacent, is_in_bound
from src.common.iterators import ordered_combinations
from src.common.strings import str_replace_by_index


def parse_input(fp: _io.FileIO):
    grid = []
    for row in fp.readlines():
        row = row.strip()
        row = list(row)
        grid.append(row)
    return grid


def main(grid: list[str]) -> tuple[int, int]:
    return (
        part1(grid),
        # part2(grid),
    )


def part1(grid: list[str]) -> int:
    times_split = 0
    new_grid = [grid[0]]
    indexes_tachyons = [grid[0].index("S")]
    for row in grid[1:]:
        new_row = row
        for idx in indexes_tachyons:
            if new_row[idx] == "^":
                indexes_tachyons.append(idx - 1)
                indexes_tachyons.append(idx + 1)
                times_split += 1
            elif new_row[idx] == "|":
                indexes_tachyons.append(idx)
            elif new_row[idx] == ".":
                indexes_tachyons.append(idx)
                new_row = str_replace_by_index(new_row, idx, "|")
        new_grid.append(row)
        indexes_tachyons = [
            idx
            for idx, (char, new_char) in enumerate(zip(row, new_row))
            if char == "^" and new_char == "|"
        ]


def part2(grid: list[str]) -> int:
    pass
