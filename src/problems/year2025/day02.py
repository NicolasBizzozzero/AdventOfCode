import _io
from functools import lru_cache


def parse_input(fp: _io.FileIO):
    ranges = list(
        map(
            lambda row: (int(row[0]), int(row[1])),
            [row.split("-") for row in fp.readline().split(",")],
        )
    )
    return ranges


def main(ranges: list[tuple[int, int]]) -> tuple[int, int]:
    invalid_ids_part1 = []
    invalid_ids_part2 = []
    for first_id, last_id in ranges:
        for id in range(first_id, last_id + 1):
            if is_invalid_id_part1(id):
                invalid_ids_part1.append(id)
            elif is_invalid_id_part2(id):
                invalid_ids_part2.append(id)

    return (sum(invalid_ids_part1), sum(invalid_ids_part2))


@lru_cache()  # In case of overlapping IDs
def is_invalid_id_part1(id: int) -> bool:
    str_id = str(id)
    if len(str_id) % 2 != 0:
        return False
    return str_id[: len(str_id) // 2] == str_id[len(str_id) // 2 :]


@lru_cache()
def is_invalid_id_part2(id: int) -> bool:
    if is_invalid_id_part1(id):  # part2 is a generalization of part1 for case size == 2
        return True

    str_id = str(id)
    if len(str_id) <= 2:
        return False

    for size in range(3, len(str_id) + 1):
        if len(str_id) % size != 0:
            continue

        # Splitting string in chunk of equal size
        split = [
            str_id[i * (len(str_id) // size) : (i + 1) * (len(str_id) // size)]
            for i in range(size)
        ]  # J'ai mal à la tête

        if all(chunk == split[0] for chunk in split):
            return True
    return False
