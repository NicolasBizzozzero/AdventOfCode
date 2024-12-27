import copy


def parse_input(data: str):
    return data.strip()


def main(sequence: str) -> tuple[int, int]:
    return (
        level1(sequence=copy.deepcopy(sequence)),
        level2(sequence=copy.deepcopy(sequence)),
    )


def level1(sequence: str) -> int:
    for _ in range(40):
        sequence = look_and_say(sequence=sequence)
    return len(sequence)


def level2(sequence: str) -> int:
    for _ in range(50):
        sequence = look_and_say(sequence=sequence)
    return len(sequence)


def look_and_say(sequence: str) -> str:
    new_sequence = ""
    for count, char in group_consecutive_chars(string=sequence):
        new_sequence += str(count) + char
    return new_sequence


def group_consecutive_chars(string: str) -> list[tuple[int, str]]:
    result = []
    count_consecutive = 1
    for i in range(1, len(string)):
        if string[i] == string[i - 1]:
            count_consecutive += 1
        else:
            result.append((count_consecutive, string[i - 1]))
            count_consecutive = 1

    # Append the last character
    result.append((count_consecutive, string[-1]))

    return result
