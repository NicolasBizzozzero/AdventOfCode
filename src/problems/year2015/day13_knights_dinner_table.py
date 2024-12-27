import copy
import itertools
from collections import defaultdict
from dataclasses import dataclass
from math import inf

from src.common.structures import defaultdict_to_dict


@dataclass
class Constraint:
    person1: str
    person2: str
    happy: bool
    points: int


def parse_input(data: str):
    constraints = []
    for row in data.split("\n"):
        person1 = row.split(" ")[0]
        person2 = row.split(" ")[-1].split(".")[0]
        happy = " gain " in row
        points = int(row.split(" ")[3])
        constraints.append(Constraint(*(person1, person2, happy, points)))
    return constraints


def main(constraints: list[Constraint]) -> tuple[int, int]:
    return (
        level1(constraints=copy.deepcopy(constraints)),
        level2(constraints=copy.deepcopy(constraints)),
    )


def level1(constraints: list[Constraint]) -> int:
    arrangement, happiness = get_optimal_guest_arrangement(constraints=constraints)
    return happiness


def level2(constraints: list[Constraint]) -> int:
    # Find all guests
    all_guests = set()
    for constraint in constraints:
        all_guests.add(constraint.person1)
        all_guests.add(constraint.person2)

    # Add myself to constraints
    for guest in all_guests:
        constraints.append(
            Constraint(person1=guest, person2="Me", happy=True, points=0)
        )
        constraints.append(
            Constraint(person1="Me", person2=guest, happy=True, points=0)
        )

    arrangement, happiness = get_optimal_guest_arrangement(constraints=constraints)
    return happiness


def get_optimal_guest_arrangement(
    constraints: list[Constraint],
) -> tuple[list[str], int]:
    cost_matrix = build_cost_matrix(constraints=constraints)

    all_guests = list(cost_matrix.keys())
    max_happiness = -inf
    max_arrangement = None
    for arrangement in itertools.permutations(all_guests):
        arrangement = list(arrangement)

        happiness = arrangement_happiness(
            arrangement=arrangement, cost_matrix=cost_matrix
        )
        if happiness > max_happiness:
            max_happiness, max_arrangement = happiness, arrangement
    return max_arrangement, max_happiness


def build_cost_matrix(constraints: list[Constraint]) -> dict[str, dict[str, int]]:
    cost_matrix = defaultdict(defaultdict)
    for constraint in constraints:
        cost_matrix[constraint.person1][constraint.person2] = (
            constraint.points if constraint.happy else -constraint.points
        )

    # Convert defaultdict to dict
    cost_matrix = defaultdict_to_dict(cost_matrix)
    return cost_matrix


def arrangement_happiness(
    arrangement: list[str], cost_matrix: dict[str, dict[str, int]]
) -> int:
    happiness = 0

    # Add cost for first and last neighbours
    happiness += cost_matrix[arrangement[0]][arrangement[1]]
    happiness += cost_matrix[arrangement[0]][arrangement[-1]]
    happiness += cost_matrix[arrangement[-1]][arrangement[-2]]
    happiness += cost_matrix[arrangement[-1]][arrangement[0]]

    for idx_guest in range(1, len(arrangement) - 1):
        guest = arrangement[idx_guest]
        left_neighbour = arrangement[idx_guest - 1]
        right_neighbour = arrangement[idx_guest + 1]
        happiness += cost_matrix[guest][left_neighbour]
        happiness += cost_matrix[guest][right_neighbour]

    return happiness
