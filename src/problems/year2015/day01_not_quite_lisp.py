import copy
from collections import Counter


def parse_input(data: str):
    return data.strip()


def main(directions: str) -> tuple[int, int]:
    return (
        level1(directions=copy.deepcopy(directions)),
        level2(directions=copy.deepcopy(directions)),
    )


def level1(directions: str) -> int:
    counter = Counter(directions)
    return counter["("] - counter[")"]


def level2(directions: str) -> int:
    level = 0
    for position in range(len(directions)):
        direction = directions[position]
        match direction:
            case "(":
                level += 1
            case ")":
                level -= 1
        if level == -1:
            return position + 1
