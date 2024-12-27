import copy

from src.common.grid import (
    iter_grid,
    grid_init_empty,
    iter_grid_idx,
    grid_iter_adjacent,
)


def parse_input(data: str):
    grid = []
    for row in data.split("\n"):
        row = row.strip()
        row = list(row)
        grid.append(row)
    return grid


def main(lights: list[list[str]]) -> tuple[int, int]:
    return level1(lights=copy.deepcopy(lights)), level2(lights=copy.deepcopy(lights))


def level1(lights: list[list[str]]) -> int:
    lights = let_lights_run_for(lights=lights, steps=100, corners_on=False)
    return count_lights_on(lights=lights)


def level2(lights: list[list[str]]) -> int:
    lights = let_lights_run_for(lights=lights, steps=100, corners_on=True)
    return count_lights_on(lights=lights)


def let_lights_run_for(
    lights: list[list[str]], steps: int, corners_on: bool
) -> list[list[str]]:
    for _ in range(steps):
        lights = get_next_state(lights=lights, corners_on=corners_on)
    return lights


def get_next_state(lights: list[list[str]], corners_on: bool) -> list[list[str]]:
    if corners_on:
        lights[0][0] = "#"
        lights[0][-1] = "#"
        lights[-1][0] = "#"
        lights[-1][-1] = "#"

    next_state = grid_init_empty(width=len(lights[0]), height=len(lights), value=".")
    for x, y in iter_grid_idx(grid=lights):
        neighbours_on = count_neighbours_on(lights=lights, idx=(x, y))
        if lights[y][x] == "#":
            next_state[y][x] = "#" if neighbours_on in (2, 3) else "."
        else:
            next_state[y][x] = "#" if neighbours_on == 3 else "."

    if corners_on:
        next_state[0][0] = "#"
        next_state[0][-1] = "#"
        next_state[-1][0] = "#"
        next_state[-1][-1] = "#"

    return next_state


def count_neighbours_on(lights: list[list[str]], idx: tuple[int, int]) -> int:
    neighbours_on = 0
    for xn, yn in grid_iter_adjacent(grid=lights, idx=idx, diagonals=True):
        neighbours_on += 1 if lights[yn][xn] == "#" else 0
    return neighbours_on


def count_lights_on(lights: list[list[str]]) -> int:
    total = 0
    for light in iter_grid(grid=lights):
        total += 1 if light == "#" else 0
    return total
