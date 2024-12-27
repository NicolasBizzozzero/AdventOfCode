import copy
from dataclasses import dataclass
from itertools import combinations_with_replacement, permutations
from math import inf


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_input(data: str):
    ingredients = []
    for row in data.split("\n"):
        name = row.split(":")[0]
        capacity = int(row.split(" ")[2][:-1])
        durability = int(row.split(" ")[4][:-1])
        flavor = int(row.split(" ")[6][:-1])
        texture = int(row.split(" ")[8][:-1])
        calories = int(row.split(" ")[10])
        ingredients.append(
            Ingredient(*(name, capacity, durability, flavor, texture, calories))
        )

    return ingredients


def main(ingredients: list[Ingredient]) -> tuple[int, int]:
    return (
        level1(ingredients=copy.deepcopy(ingredients)),
        level2(ingredients=copy.deepcopy(ingredients)),
    )


def level1(ingredients: list[Ingredient]) -> int:
    best_combination, best_score = find_best_ingredients(
        ingredients=ingredients, max_combination=100
    )
    return best_score


def level2(ingredients: list[Ingredient]) -> int:
    best_combination, best_score = find_best_ingredients(
        ingredients=ingredients, max_combination=100, target_calories=500
    )
    return best_score


def find_best_ingredients(
    ingredients: list[Ingredient],
    max_combination: int,
    target_calories: int = None,
) -> tuple[list[int], int]:
    best_score = -inf
    best_combination = None
    for combination in all_ingredient_combinations(
        n=len(ingredients), target_sum=max_combination
    ):
        if (
            target_calories
            and score_calories(combination=combination, ingredients=ingredients)
            != target_calories
        ):
            continue

        score = score_combination(combination=combination, ingredients=ingredients)
        if score > best_score:
            best_score, best_combination = score, combination
    return best_combination, best_score


def all_ingredient_combinations(n: int, target_sum: int) -> list[list[int]]:
    # Generate combinations with replacement where the sum is `target_sum`
    combinations = [
        combo
        for combo in combinations_with_replacement(range(target_sum + 1), n)
        if sum(combo) == target_sum
    ]

    # Generate all permutations for each valid combination
    permutations_list = []
    for combo in combinations:
        permutations_list.extend(permutations(combo))

    # Remove duplicates (since permutations might overlap for some inputs)
    unique_permutations = set(permutations_list)

    return [list(perm) for perm in unique_permutations]


def score_combination(combination: list[int], ingredients: list[Ingredient]) -> int:
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    for ingredient, amount in zip(ingredients, combination):
        capacity += ingredient.capacity * amount
        durability += ingredient.durability * amount
        flavor += ingredient.flavor * amount
        texture += ingredient.texture * amount

    if any((capacity < 0, durability < 0, flavor < 0, texture < 0)):
        return 0

    return capacity * durability * flavor * texture


def score_calories(combination: list[int], ingredients: list[Ingredient]) -> int:
    return sum(
        ingredient.calories * amount
        for ingredient, amount in zip(ingredients, combination)
    )
