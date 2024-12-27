import copy
import json
import re


def parse_input(data: str):
    return json.loads(data)


def main(document: dict | list | int | str) -> tuple[int, int]:
    return (
        level1(document=copy.deepcopy(document)),
        level2(document=copy.deepcopy(document)),
    )


def level1(document: dict | list | int | str) -> int:
    # All numbers can also quickly be grepped with re.findall(r"-?\d+") on raw data
    total = 0
    if isinstance(document, list):
        for element in document:
            total += level1(document=element)
    elif isinstance(document, dict):
        for element in document.values():
            total += level1(document=element)
    elif isinstance(document, int):
        total += document
    else:
        return 0
    return total


def level2(document: dict | list | int | str) -> int:
    total = 0
    if isinstance(document, list):
        for element in document:
            total += level2(document=element)
    elif isinstance(document, dict):
        if "red" in document.values():
            return 0
        for element in document.values():
            total += level2(document=element)
    elif isinstance(document, int):
        total += document
    else:
        return 0
    return total
