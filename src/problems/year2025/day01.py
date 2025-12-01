import _io
import math
from collections import Counter

import numpy as np


def parse_input(fp: _io.FileIO):
    sequence = []
    for row in fp.readlines():
        rotation, distance = row[0], int(row[1:].strip())
        sequence.append((rotation, distance))
    return sequence


def main(sequence: list[tuple[str, int]]) -> tuple[int, int]:
    return (find_password_1(sequence), find_password_2(sequence))


def find_password_1(sequence: list[tuple[str, int]]) -> int:
    dial = 50
    password = 0
    for rotation, distance in sequence:
        dial = rotate_dial(dial, rotation, distance)
        if dial == 0:
            password += 1
    return password


def find_password_2(sequence: list[tuple[str, int]]) -> int:
    dial = 50
    password = 0
    for rotation, distance in sequence:
        dial_before = dial
        dial = rotate_dial(dial_before, rotation, distance)

        # We count all full loops here, then will add one later for the latest rotation
        password += distance // 100

        if dial_before != 0:
            if rotation == "L" and (distance % 100) >= dial_before:
                password += 1
            elif rotation == "R" and (distance % 100) >= (100 - dial_before):
                password += 1

    return password


def rotate_dial(dial: int, rotation: str, distance: int) -> int:
    if rotation == "L":
        return (dial - distance) % 100
    if rotation == "R":
        return (dial + distance) % 100
