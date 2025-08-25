import copy
from collections import defaultdict

from src.common.structures import defaultdict_to_dict


def parse_input(data: str):
    replacements = defaultdict(list)
    for row in data.split("\n"):
        if len(row) == 0:
            break

        source, dest = row.split(" => ")
        replacements[source].append(dest)
    replacements = defaultdict_to_dict(replacements)

    starting_molecule = data.split("\n")[-1]

    return replacements, starting_molecule


def main(data: tuple[dict[str, list[str]], str]) -> tuple[int, int]:
    replacements, molecule = data

    return (
        level1(
            replacements=copy.deepcopy(replacements),
            starting_molecule=copy.deepcopy(molecule),
        ),
        level2(
            replacements=copy.deepcopy(replacements),
            molecule=copy.deepcopy(molecule),
        ),
    )


def level1(replacements: dict[str, list[str]], starting_molecule: str) -> int:
    molecules = generate_molecules(
        starting_molecule=starting_molecule, replacements=replacements
    )
    return len(molecules)


def level2(replacements: dict[str, list[str]], molecule: str) -> int:
    return min_steps_to_molecule(target=molecule, replacements=replacements)


def generate_molecules(
    starting_molecule: str, replacements: dict[str, list[str]]
) -> set[str]:
    results = set()
    # Iterate through the starting molecule
    for i in range(len(starting_molecule)):
        # Check each replacement rule
        for target, substitutions in replacements.items():
            # If the target substring matches the molecule at the current position
            if starting_molecule[i : i + len(target)] == target:
                for substitution in substitutions:
                    # Replace the target substring with the substitution
                    # eg substring insertion but we substitute the rest of the string by ignoring `len(target)`
                    new_molecule = (
                        starting_molecule[:i]
                        + substitution
                        + starting_molecule[i + len(target) :]
                    )
                    results.add(new_molecule)
    return results


def min_steps_to_molecule(target: str, replacements: dict[str, list[str]]) -> int:
    # Reverse the replacements for backtracking
    reverse_replacements = {
        replacement: source
        for source, replacements_list in replacements.items()
        for replacement in replacements_list
    }

    # Start with the target molecule
    steps = 0
    current_molecule = target

    # Backtrack until we reduce to "e"
    while current_molecule != "e":
        replaced = False
        for replacement, source in reverse_replacements.items():
            # Find if the replacement can be reversed
            if replacement in current_molecule:
                # Replace the first occurrence of the replacement with its source
                current_molecule = current_molecule.replace(replacement, source, 1)
                steps += 1
                replaced = True
                break
        if not replaced:
            raise ValueError(
                f"Cannot reduce the molecule {current_molecule} to 'e' using the given rules."
            )

    return steps
