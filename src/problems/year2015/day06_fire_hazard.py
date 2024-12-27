import copy
from dataclasses import dataclass

import numpy as np


@dataclass
class Instruction:
    command: str
    start: tuple[int, int]
    end: tuple[int, int]


def parse_input(data: str):
    instructions = []
    for row in data.split("\n"):
        if row.startswith("turn"):
            command = " ".join(row.split(" ")[:2]).strip()
            start = tuple(map(int, row.split(" ")[2].split(",")))
            end = tuple(map(int, row.split(" ")[4].split(",")))
        else:
            command = "toggle"
            start = tuple(map(int, row.split(" ")[1].split(",")))
            end = tuple(map(int, row.split(" ")[3].split(",")))
        instructions.append(Instruction(*(command, start, end)))
    return instructions


def main(instructions: list[Instruction]) -> tuple[int, int]:
    return (
        level1(instructions=copy.deepcopy(instructions)),
        level2(instructions=copy.deepcopy(instructions)),
    )


def level1(instructions: list[Instruction]) -> int:
    house = create_house(size=1_000)
    for instruction in instructions:
        apply_instructions(house=house, instruction=instruction)
    return house.sum()


def level2(instructions: list[Instruction]) -> int:
    house = create_house(size=1_000)
    for instruction in instructions:
        apply_real_instructions(house=house, instruction=instruction)
    return house.sum()


def create_house(size: int) -> np.ndarray:
    return np.zeros(shape=(size, size), dtype=np.int64)


def apply_instructions(house: np.ndarray, instruction: Instruction) -> None:
    match instruction.command:
        case "turn on":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] = 1
        case "turn off":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] = 0
        case "toggle":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] ^= 1  # XOR with 1 flips the bits


def apply_real_instructions(house: np.ndarray, instruction: Instruction) -> None:
    match instruction.command:
        case "turn on":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] += 1
        case "turn off":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] -= 1
            house[house < 0] = 0
        case "toggle":
            house[
                instruction.start[0] : instruction.end[0] + 1,
                instruction.start[1] : instruction.end[1] + 1,
            ] += 2
