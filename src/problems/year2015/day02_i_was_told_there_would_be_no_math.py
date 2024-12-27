import copy
from dataclasses import dataclass

import numpy as np


@dataclass
class Gift:
    length: int
    width: int
    height: int


def parse_input(data: str):
    gifts = []
    for row in data.split("\n"):
        gift = row.strip().split("x")
        gift = tuple(map(int, gift))
        gifts.append(Gift(*gift))
    return gifts


def main(gifts: list[Gift]) -> tuple[int, int]:
    return (level1(gifts=copy.deepcopy(gifts)), level2(gifts=copy.deepcopy(gifts)))


def level1(gifts: list[Gift]) -> int:
    total_cost = 0
    for gift in gifts:
        total_cost += cost_wrapping_paper(gift=gift)
    return total_cost


def level2(gifts: list[Gift]) -> int:
    total_cost = 0
    for gift in gifts:
        total_cost += cost_ribbon(gift=gift)
    return total_cost


def cost_wrapping_paper(gift: Gift) -> int:
    sides = (
        gift.length * gift.width,
        gift.width * gift.height,
        gift.height * gift.length,
    )
    smallest_side = min(sides)
    surface_area = (np.array(sides) * 2).sum()
    return surface_area + smallest_side


def cost_ribbon(gift: Gift) -> int:
    perimeters = (
        2 * gift.length + 2 * gift.width,
        2 * gift.width + 2 * gift.height,
        2 * gift.height + 2 * gift.length,
    )
    ribbon = min(perimeters)
    bow = gift.length * gift.width * gift.height
    return ribbon + bow
