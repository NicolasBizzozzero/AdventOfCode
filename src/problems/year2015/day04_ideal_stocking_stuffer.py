import copy
from hashlib import md5


def parse_input(data: str):
    return data.strip()


def main(secret_key: str) -> tuple[int, int]:
    return (
        level1(secret_key=copy.deepcopy(secret_key)),
        level2(secret_key=copy.deepcopy(secret_key)),
    )


def level1(secret_key: str) -> int:
    return find_advent_coin(secret_key=secret_key, prefix="00000")


def level2(secret_key: str) -> int:
    return find_advent_coin(secret_key=secret_key, prefix="000000")


def compute_md5(string: str) -> str:
    return md5(string.encode("utf-8")).hexdigest()


def find_advent_coin(secret_key: str, prefix: str) -> int:
    number = 0
    while True:
        md5_hash = compute_md5(string=secret_key + str(number))
        if md5_hash.startswith(prefix):
            return number
        number += 1
