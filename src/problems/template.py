import copy


def parse_input(data: str):
    return data.strip()


def main(data) -> tuple[int, int]:
    return (
        level1(data=copy.deepcopy(data)),
        # level2(data=copy.deepcopy(data))
    )


def level1(data) -> int:
    print(data)
    exit(0)


def level2(data) -> int: ...
