import copy

from src.common.iterators import batched


def parse_input(data: str):
    return data.strip()


def main(password: str) -> tuple[str, str]:
    return (
        level1(password=copy.deepcopy(password)),
        level2(password=copy.deepcopy(password)),
    )


def level1(password: str) -> str:
    return find_next_password(password=password)


def level2(password: str) -> str:
    return find_next_password(password=find_next_password(password=password))


def find_next_password(password: str) -> str:
    while password != "zzzzzzzz":
        password = increment_string(password=password)
        if is_valid(password=password):
            return password


def is_valid(password: str) -> bool:
    for bad_letter in "iol":
        if bad_letter in password:
            return False

    # A triplet of increasing straight letters
    all_triplets = list(
        map(
            lambda s: "".join(s),
            batched(
                iterable=[chr(i) for i in range(97, 123)],
                n=3,
                step=1,
                drop_last_if_shorter=True,
            ),
        )
    )
    for triplet in all_triplets:
        if triplet in password:
            break
    else:
        return False

    # Two different pairs of letters
    nb_of_pairs = 0
    all_pairs = [chr(i) + chr(i) for i in range(97, 123)]
    for pair in all_pairs:
        if pair in password:
            nb_of_pairs += 1
            if nb_of_pairs >= 2:
                break
    else:
        return False

    return True


def increment_string(password: str) -> str:
    password = list(password)

    i = len(password) - 1
    while i >= 0:
        if password[i] == "z":
            # If the character is 'z', wrap it around to 'a'
            password[i] = "a"
        else:
            # Otherwise, increment the character
            password[i] = chr(ord(password[i]) + 1)
            break  # Done incrementing, no need to go further
        i -= 1

    return "".join(password)
