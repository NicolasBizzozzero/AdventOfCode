import copy
from itertools import combinations


def parse_input(data: str):
    return [int(value) for value in data.split("\n")]


def main(containers: list[int]) -> tuple[int, int]:
    return (
        level1(containers=copy.deepcopy(containers)),
        level2(containers=copy.deepcopy(containers)),
    )


def level1(containers: list[int]) -> int:
    all_combinations = generate_combinations(containers=containers, target=150)
    return len(all_combinations)


def level2(containers: list[int]) -> int:
    all_combinations = generate_combinations(containers=containers, target=150)
    min_containers = len(min(all_combinations, key=len))

    total_combinations = 0
    for combination in all_combinations:
        if len(combination) == min_containers:
            total_combinations += 1

    return total_combinations


def generate_combinations(containers: list[int], target: int) -> list[list[int]]:
    result = []
    for comb_length in range(1, len(containers) + 1):
        for combination in combinations(containers, comb_length):
            if sum(combination) == target:
                result.append(list(combination))
    return result
