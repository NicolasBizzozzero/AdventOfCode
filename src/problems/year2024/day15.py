import _io
import copy

import numpy as np

from src.common.grid import print_grid


def parse_input(fp: _io.FileIO):
    grid = []
    grid_horizontal_limits = 0
    moves = []

    for row in fp.readlines():
        row = row.strip()

        if grid_horizontal_limits < 2:
            grid.append(list(row))
        else:
            if row != "":
                moves += list(row)

        if row == "#" * len(row):
            grid_horizontal_limits += 1

    return (grid, moves)


def main(data) -> tuple[int, int]:
    grid, moves = data
    return (
        level1(grid=copy.deepcopy(grid), moves=copy.deepcopy(moves)),
        level2(grid=copy.deepcopy(grid), moves=copy.deepcopy(moves)),
    )


def level1(grid: list[list[str]], moves: list[str]) -> int:
    print_grid(grid=grid)
    robot = get_robot_position(grid)
    for idx_move, move in enumerate(moves):
        grid, robot = epoch(grid=grid, robot=robot, move=move)

    score = compute_gps_coordinates(grid=grid)
    return score


def level2(grid: list[list[str]], moves: list[str]) -> int:
    grid = expand_warehouse(grid=grid)
    print_grid(grid=grid)
    robot = get_robot_position(grid)
    for idx_move, move in enumerate(moves):
        grid, robot = epoch_big_warehouse(grid=grid, robot=robot, move=move)
        print_grid(grid=grid)
    score = compute_gps_coordinates(grid=grid)
    print(score)
    exit(0)
    return score


def get_robot_position(grid: list[list[str]]) -> tuple[int, int]:
    for idx_row, row in enumerate(grid):
        for idx_col, col in enumerate(row):
            if grid[idx_row][idx_col] == "@":
                return idx_col, idx_row


def epoch(
    grid: list[list[str]], robot: tuple[int, int], move: str
) -> tuple[list[list[str]], tuple[int, int]]:
    match move:
        case "<":
            direction = (-1, 0)
        case "^":
            direction = (0, -1)
        case ">":
            direction = (1, 0)
        case "v":
            direction = (0, 1)

    match grid[robot[1] + direction[1]][robot[0] + direction[0]]:
        case ".":
            grid[robot[1]][robot[0]] = "."
            grid[robot[1] + direction[1]][robot[0] + direction[0]] = "@"
            robot = (robot[0] + direction[0], robot[1] + direction[1])
        case "O":
            # Check if we can push box
            for idx_box in range(2, max(len(grid[0]), len(grid))):
                match grid[robot[1] + (idx_box * direction[1])][
                    robot[0] + (idx_box * direction[0])
                ]:
                    case "#":
                        # We cannot, do nothing
                        break
                    case "O":
                        # Check next case if there is space available
                        continue
                    case ".":
                        # Yes we can
                        grid[robot[1]][robot[0]] = "."
                        grid[robot[1] + direction[1]][robot[0] + direction[0]] = "@"
                        grid[robot[1] + (idx_box * direction[1])][
                            robot[0] + (idx_box * direction[0])
                        ] = "O"
                        robot = (robot[0] + direction[0], robot[1] + direction[1])
                        break
    return grid, robot


def epoch_big_warehouse(
    grid: list[list[str]], robot: tuple[int, int], move: str
) -> tuple[list[list[str]], tuple[int, int]]:
    match move:
        case "<":
            direction = (-1, 0)
        case "^":
            direction = (0, -1)
        case ">":
            direction = (1, 0)
        case "v":
            direction = (0, 1)

    match grid[robot[1] + direction[1]][robot[0] + direction[0]]:
        case ".":
            grid[robot[1]][robot[0]] = "."
            grid[robot[1] + direction[1]][robot[0] + direction[0]] = "@"
            robot = (robot[0] + direction[0], robot[1] + direction[1])
        case "[" | "]":
            grid, robot, _ = push_boxes_big_warehouse(
                grid=grid,
                robot=robot,
                direction=direction,
                box_coordinates=(robot[0] + direction[0], robot[1] + direction[1]),
            )
    return grid, robot


def compute_gps_coordinates(grid: list[list[str]]) -> int:
    total = 0
    for y, row in enumerate(grid):
        for x, element in enumerate(row):
            if element in ("O", "["):
                total += gps_coordinates(box=(x, y))
    return total


def gps_coordinates(box: tuple[int, int]) -> int:
    return (100 * box[1]) + box[0]


def expand_warehouse(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, element in enumerate(row):
            match element:
                case "#":
                    new_row += ["#", "#"]
                case "O":
                    new_row += ["[", "]"]
                case ".":
                    new_row += [".", "."]
                case "@":
                    new_row += ["@", "."]
        new_grid.append(new_row)
    return new_grid


def push_boxes_big_warehouse(
    grid: list[list[str]],
    robot: tuple[int, int],
    direction: tuple[int, int],
    box_coordinates: tuple[int, int],
) -> tuple[list[list[str]], tuple[int, int], bool]:
    if direction in ((0, -1), (0, 1)):
        match grid[box_coordinates[1] + direction[1]][
            box_coordinates[0] + direction[0]
        ]:
            case "#":
                # We cannot, do nothing
                return grid, robot, False
            case "[" | "]":
                # Check next case if there is space available
                grid, robot, is_box_pushed = push_boxes_big_warehouse(
                    grid=grid,
                    robot=robot,
                    direction=direction,
                    box_coordinates=(
                        box_coordinates[0] + direction[0],
                        box_coordinates[1] + direction[1],
                    ),
                )
                if is_box_pushed:
                    # Next box has been pushed, push our box
                    grid[box_coordinates[1]][box_coordinates[0]]
                return grid, robot, is_box_pushed
            case ".":
                # Yes we can
                grid[robot[1]][robot[0]] = "."
                grid[robot[1] + direction[1]][robot[0] + direction[0]] = "@"
                grid[robot[1] + (idx_box * direction[1])][
                    robot[0] + (idx_box * direction[0])
                ] = "O"
                robot = (robot[0] + direction[0], robot[1] + direction[1])
                break
    else:
        ...
