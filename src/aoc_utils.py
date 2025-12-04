import datetime
import glob
import os
import re
from typing import Any

import requests


class AdventOfCodeConnector:
    url: str = "https://adventofcode.com/{year}/day/{day}"

    def __init__(self, token_session: str):
        self.token_session = token_session

    def get_input(self, year: str, day: str) -> str:
        url = f"{self.url.format(year=year, day=int(day))}/input"

        response = requests.get(
            url, headers={"Cookie": f"session={self.token_session}"}
        )

        match response.status_code:
            case 200:
                return response.text
            case _:
                print(
                    f"Error HTTP {response.status_code}: {response.reason}, {response.text}"
                )
                exit(1)

    def submit_answer(self, year: str, day: str, level: str, answer: str):
        assert str(level) in ("1", "2"), "Level must be only two values, 1 or 2"

        url = f"{self.url.format(year=year, day=int(day))}/answer"
        response = requests.post(
            url,
            data={"level": level, "answer": answer},
            headers={"Cookie": f"session={self.token_session}"},
        )

        if response.status_code != 200:
            print(
                f"Error HTTP {response.status_code}: {response.reason}, {response.text}"
            )
        elif "You don't seem to be solving the right level." in response.text:
            print(
                f"Level already solved, cannot submit answer. Your answer was {self.get_answers(year=year, day=day)[int(level) - 1]}"
            )
        elif "That's the right answer!" in response.text:
            if "[Continue to Part Two]" in response.text:
                print("Successfully answered level 1 !")
            else:
                print("Successfully answered level 2 !")
        elif "That's not the right answer" in response.text:
            if "your answer is too low" in response.text:
                print("Wrong answer, your answer is too low")
            elif "your answer is too high" in response.text:
                print("Wrong answer, your answer is too high")
            else:
                print("Wrong answer")
        elif "You gave an answer too recently" in response.text:
            print(
                f"You gave an answer too recently, please wait 1 min between each answers"
            )
        else:
            print(f"Error while submitting answer : {response.text}")

    def get_answers(self, year: str, day: str) -> list[int]:
        url = f"{self.url.format(year=year, day=int(day))}"
        response = requests.post(
            url,
            headers={"Cookie": f"session={self.token_session}"},
        )
        if response.status_code != 200:
            print(
                f"Error HTTP {response.status_code}: {response.reason}, {response.text}"
            )
        matches = re.findall(
            r"Your puzzle answer was <code>(.*?)</code>", response.text
        )
        return [match for match in matches]


def get_path_input(path_dir_input: str, problem_number: str, year: str):
    return os.path.abspath(os.path.join(path_dir_input, year, f"{problem_number}.txt"))


def format_problem_results(
    problem_number: str,
    results: tuple[int, int],
    time_to_completion: float,
) -> str:
    return f"Day {problem_number} : {', '.join(str(result) for result in results)} ({round(time_to_completion, 4)}s)"


def save_input(year: str, day: str, path_file_output: str):
    connector = AdventOfCodeConnector(token_session=os.environ["AOC_TOKEN_SESSION"])
    result = connector.get_input(year=year, day=day)

    with open(path_file_output, "w", newline="\n") as fp:
        fp.write(result)


def submit_answer(year: str, day: str, level: int, answer: int):
    connector = AdventOfCodeConnector(token_session=os.environ["AOC_TOKEN_SESSION"])
    connector.submit_answer(year=year, day=day, level=str(level), answer=str(answer))


def is_aoc_season() -> bool:
    current_time = datetime.datetime.now()

    if current_time.month != 12 or current_time.day < 1 or current_time.day > 25:
        return False
    return True


def find_module_path_for_problem(
    year: str, problem_number: str, path_dir_root: str
) -> str:
    path_dir_module = os.path.join(
        path_dir_root,
        "src",
        "problems",
        f"year{year}",
    )
    path_file_module = os.path.join(
        path_dir_module,
        f"day{problem_number}.py",
    )

    if os.path.exists(path_file_module):
        return path_file_module

    # Have not found a simple file, trying to find a single file for this day with an underscore and a name
    path_file_module = os.path.join(
        path_dir_module,
        f"day{problem_number}_*.py",
    )
    potential_files = list(glob.glob(path_file_module))
    if len(potential_files) == 1:
        return potential_files[0]

    raise ValueError(
        f"Code for year {year} and day {problem_number} cannot be found {path_file_module}"
    )


def assert_answer(year: str, day: str, answers: tuple[Any, Any]):
    connector = AdventOfCodeConnector(token_session=os.environ["AOC_TOKEN_SESSION"])
    correct_answers = connector.get_answers(year=year, day=day)

    if len(correct_answers) == 0:
        return
    elif len(correct_answers) == 1:
        answers = [answers[0]]
    else:
        answers = list(answers)

    if correct_answers == answers:
        print(f"  Your answer(s) are correct")
    else:
        print(
            f"  Your answer(s) are incorrect. Expected {correct_answers}, got {answers}"
        )
