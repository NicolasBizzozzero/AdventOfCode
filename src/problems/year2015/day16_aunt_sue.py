import copy

from src.common.iterators import batched


def parse_input(data: str):
    aunts = dict()
    for row in data.split("\n"):
        aunt = int(row.split("Sue ")[1].split(":")[0])
        aunts[aunt] = dict()

        data = ": ".join(row.split(": ")[1:]).split(", ")
        for _data in data:
            key, value = _data.split(": ")
            aunts[aunt][key] = int(value)
    return aunts


def main(aunts: dict[int, dict[str, int]]) -> tuple[int, int]:
    clues = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    return (
        level1(aunts=copy.deepcopy(aunts), clues=clues),
        level2(aunts=copy.deepcopy(aunts), clues=clues),
    )


def level1(aunts: dict[int, dict[str, int]], clues: dict[str, int]) -> int:
    for aunt in aunts.keys():
        if is_your_aunt(aunt=aunts[aunt], clues=clues):
            return aunt


def level2(aunts: dict[int, dict[str, int]], clues: dict[str, int]) -> int:
    for aunt in aunts.keys():
        if is_your_aunt_retroencubalated(aunt=aunts[aunt], clues=clues):
            return aunt


def is_your_aunt(aunt: dict[str, int], clues: dict[str, int]) -> bool:
    for key, value in aunt.items():
        if key in clues.keys():
            if value != clues[key]:
                return False
    return True


def is_your_aunt_retroencubalated(aunt: dict[str, int], clues: dict[str, int]) -> bool:
    for key, value in aunt.items():
        if key in clues.keys():
            match key:
                case "cats" | "trees":
                    if value <= clues[key]:
                        return False
                case "pomeranians" | "goldfish":
                    if value >= clues[key]:
                        return False
                case _:
                    if value != clues[key]:
                        return False
    return True
