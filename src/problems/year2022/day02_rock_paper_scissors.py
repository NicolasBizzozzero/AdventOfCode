""" Day 2: Rock Paper Scissors

The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

"""

import os
import copy


PATH_DIR_INPUT = "res"
PATH_FILE_INPUT = os.path.join(
    PATH_DIR_INPUT, f"{__file__.split('/')[-1].split('_')[0]}_input.txt"
)


def main():
    problem = parse_input(path_file_input=PATH_FILE_INPUT)

    part1_check_strategy(problem=copy.deepcopy(problem))
    part2_updated_strategy(problem=copy.deepcopy(problem))


def part1_check_strategy(problem):
    total_score = sum(map(lambda round: score(*round), problem))

    print("Problem 1")
    print("  Total score:", total_score)


def part2_updated_strategy(problem):
    # Map result to move I need to make
    translated_problem = []
    for round in problem:
        move_opponent, result = round
        move_player = result_to_move(move_opponent, result)
        translated_problem.append([move_opponent, move_player])

    # Compute score like previously
    total_score = sum(map(lambda round: score(*round), translated_problem))

    print("Problem 2")
    print("  Total score:", total_score)


def parse_input(path_file_input: str):
    problem = []

    with open(path_file_input) as fp:
        for line in fp:
            line = line.strip()
            if len(line) != 0:
                problem.append(line.split(" "))
    return problem


def result_to_move(move_opponent: str, result: str) -> str:
    match move_opponent:
        case "A":  # Rock
            match result:
                case "X":  # Lose
                    return "Z"
                case "Y":  # Draw
                    return "X"
                case "Z":  # Win
                    return "Y"
        case "B":  # Paper
            match result:
                case "X":  # Lose
                    return "X"
                case "Y":  # Draw
                    return "Y"
                case "Z":  # Win
                    return "Z"
        case "C":  # Scissors
            match result:
                case "X":  # Lose
                    return "Y"
                case "Y":  # Draw
                    return "Z"
                case "Z":  # Win
                    return "X"


def score(move_opponent: str, move_player: str) -> int:
    return round_score(move_opponent, move_player) + move_score(move_player)


def round_score(move_opponent: str, move_player: str) -> int:
    score_lose = 0
    score_draw = 3
    score_win = 6

    match move_opponent:
        # Rock
        case "A":
            match move_player:
                case "X":
                    return score_draw
                case "Y":
                    return score_win
                case "Z":
                    return score_lose
        # Paper
        case "B":
            match move_player:
                case "X":
                    return score_lose
                case "Y":
                    return score_draw
                case "Z":
                    return score_win
        # Scissors
        case "C":
            match move_player:
                case "X":
                    return score_win
                case "Y":
                    return score_lose
                case "Z":
                    return score_draw


def move_score(move_player: str) -> int:
    match move_player:
        case "X":
            return 1
        case "Y":
            return 2
        case "Z":
            return 3


if __name__ == "__main__":
    main()
