import copy
import itertools
from collections import defaultdict
from math import inf


def parse_input(data: str):
    minimum_distances = defaultdict(defaultdict)

    for row in data.split("\n"):
        location1 = row.split(" to")[0]
        location2 = row.split("to ")[1].split(" ")[0]
        distance = int(row.split(" ")[-1])

        minimum_distances[location1][location2] = distance
        minimum_distances[location2][location1] = distance

    return minimum_distances


def main(minimum_distances: dict[str, dict[str, int]]) -> tuple[int, int]:
    return (
        level1(minimum_distances=copy.deepcopy(minimum_distances)),
        level2(minimum_distances=copy.deepcopy(minimum_distances)),
    )


def level1(minimum_distances: dict[str, dict[str, int]]) -> int:
    min_distance = inf
    all_locations = list(minimum_distances.keys())
    for route in itertools.permutations(all_locations):
        distance_route = compute_distance_route(
            route=route, minimum_distances=minimum_distances
        )
        if distance_route < min_distance:
            min_distance = distance_route
    return min_distance


def level2(minimum_distances: dict[str, dict[str, int]]) -> int:
    max_distance = -inf
    all_locations = list(minimum_distances.keys())
    for route in itertools.permutations(all_locations):
        distance_route = compute_distance_route(
            route=route, minimum_distances=minimum_distances
        )
        if distance_route > max_distance:
            max_distance = distance_route
    return max_distance


def compute_distance_route(
    route: list[str], minimum_distances: dict[str, dict[str, int]]
) -> int:
    distance_route = 0
    for i in range(len(route) - 1):
        distance_route += minimum_distances[route[i]][route[i + 1]]
    return distance_route
