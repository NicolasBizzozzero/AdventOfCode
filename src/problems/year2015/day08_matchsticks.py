import copy


def parse_input(data: str):
    return data.strip().split("\n")


def main(strings: list[str]) -> tuple[int, int]:
    return (
        level1(strings=copy.deepcopy(strings)),
        level2(strings=copy.deepcopy(strings)),
    )


def level1(strings: list[str]) -> int:
    total_code, total_data = 0, 0
    for string in strings:
        total_code += len_code(string=string)
        total_data += len_representation(string=string)
    return total_code - total_data


def level2(strings: list[str]) -> int:
    total_code, total_encoded = 0, 0
    for string in strings:
        total_code += len_code(string=string)
        total_encoded += len_encoded(string=string)
    return total_encoded - total_code


def len_code(string: str) -> int:
    return len(string)


def len_representation(string: str) -> int:
    return len(eval(string))


def len_encoded(string: str) -> int:
    return len(string) + string.count("\\") + string.count('"') + 2
