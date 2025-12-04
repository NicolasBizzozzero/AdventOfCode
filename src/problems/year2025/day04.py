import _io
from functools import lru_cache
from math import inf
from pprint import pprint

from src.common.grid import print_grid, iter_grid_idx, grid_iter_adjacent, is_in_bound
from src.common.iterators import ordered_combinations


def parse_input(fp: _io.FileIO):
    grid = []
    for row in fp.readlines():
        row = row.strip()
        row = list(row)
        grid.append(row)
    return grid


def main(grid: list[list[str]]) -> tuple[int, int]:
    return (part1(grid), part2(grid))


def part1(grid: list[list[str]]) -> int:
    total = 0
    for x, y in iter_grid_idx(grid):
        if grid[x][y] == "@":
            if is_toilet_paper_accessible(grid, x, y):
                total += 1
    return total


def part2(grid: list[list[str]]) -> int:
    total = 0
    while True:
        removed_this_round = 0
        for x, y in iter_grid_idx(grid):
            if grid[x][y] == "@":
                if is_toilet_paper_accessible(grid, x, y):
                    removed_this_round += 1
                    grid[x][y] = "."
        total += removed_this_round
        if removed_this_round == 0:
            break

    return total


def is_toilet_paper_accessible(grid: list[list[str]], x: int, y: int) -> bool:
    adjacent_papers = 0
    for i, j in grid_iter_adjacent(grid, (x, y), diagonals=True):
        if not is_in_bound(grid, (x, y)):
            continue
        if grid[i][j] == "@":
            adjacent_papers += 1
            if adjacent_papers >= 4:
                return False
    return True
