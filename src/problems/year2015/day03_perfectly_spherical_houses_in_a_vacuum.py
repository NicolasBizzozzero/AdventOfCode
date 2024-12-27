import copy
from collections import defaultdict


def parse_input(data: str):
    return data


def main(directions: str) -> tuple[int, int]:
    return (
        level1(directions=copy.deepcopy(directions)),
        level2(directions=copy.deepcopy(directions)),
    )


def level1(directions: str) -> int:
    houses = defaultdict(int)
    deliver_presents(
        directions=directions,
        houses=houses,
        starting_location=(0, 0),
    )
    return len(houses)


def level2(directions: str) -> int:
    houses = defaultdict(int)
    deliver_presents(
        directions=directions[0::2],
        houses=houses,
        starting_location=(0, 0),
    )
    deliver_presents(
        directions=directions[1::2],
        houses=houses,
        starting_location=(0, 0),
    )
    return len(houses)


def deliver_presents(
    directions: str,
    houses: defaultdict[tuple[int, int], int],
    starting_location: tuple[int, int],
) -> None:
    houses[starting_location] += 1

    location = starting_location
    for direction in directions:
        match direction:
            case ">":
                step = (1, 0)
            case "v":
                step = (0, 1)
            case "<":
                step = (-1, 0)
            case "^":
                step = (0, -1)

        location = (location[0] + step[0], location[1] + step[1])
        houses[location] += 1
