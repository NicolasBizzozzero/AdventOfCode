import _io
import math
from functools import lru_cache
from math import inf
from pprint import pprint

from tqdm import tqdm

from src.common.grid import print_grid, iter_grid_idx, grid_iter_adjacent, is_in_bound
from src.common.iterators import ordered_combinations


def parse_input(fp: _io.FileIO):
    args_part1 = parse_part1(fp=fp)
    fp.seek(0)
    args_part2 = parse_part2(fp=fp)
    return (args_part1, args_part2)


def parse_part1(fp: _io.FileIO):
    worksheet = []
    operations = []
    for row in fp.readlines():
        if row[0] in "*+":
            operations = [col.strip() for col in row.split()]
        else:
            row = [int(col.strip()) for col in row.split()]
            worksheet.append(row)
    return worksheet, operations


def parse_part2(fp: _io.FileIO):
    content = [row.replace("\n", "") for row in fp.readlines()]
    operations = "".join(reversed(content[-1]))
    worksheet = ["".join(reversed(row)) for row in content[:-1]]

    new_operations = []
    new_worksheet = []
    current_formula = [[] for _ in range(len(worksheet))]
    skip_next_column = False
    for idx_col, column in enumerate(operations):
        # Empty column just after reading an operator
        if skip_next_column:
            skip_next_column = False
            continue

        for idx_row, row in enumerate(worksheet):
            current_formula[idx_row].append(row[idx_col])

        if column in "*+":
            current_formula = ["".join(col) for col in reversed(current_formula)]
            final_operation = ["" for _ in range(len(current_formula[0]))]
            for number in reversed(current_formula):
                for idx_col, col in enumerate(number):
                    final_operation[idx_col] += col
            final_operation = [int(number) for number in final_operation]
            new_worksheet.append(final_operation)
            new_operations.append(column)
            current_formula = [[] for _ in range(len(worksheet))]
            skip_next_column = True

    return new_worksheet, new_operations


def main(args) -> tuple[int, int]:
    (worksheet_part1, operations_part1), (worksheet_part2, operations_part2) = args
    return (
        do_maths(worksheet_part1, operations_part1),
        do_maths_human(worksheet_part2, operations_part2),
    )


def do_maths(worksheet: list[list[int]], operations: list[str]) -> int:
    intermediate_row = worksheet[0]
    for row in tqdm(worksheet[1:]):
        for idx_col, col in enumerate(row):
            if operations[idx_col] == "+":
                intermediate_row[idx_col] += col
            elif operations[idx_col] == "*":
                intermediate_row[idx_col] *= col
    grand_total = sum(intermediate_row)
    return grand_total


def do_maths_human(worksheet: list[list[int]], operations: list[str]) -> int:
    grand_total = 0
    for row, operator in zip(worksheet, operations):
        if operator == "*":
            grand_total += math.prod(row)
        elif operator == "+":
            grand_total += sum(row)
    return grand_total
