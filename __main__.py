import os
import sys
import time

from src.aoc_utils import (
    get_path_input,
    format_problem_results,
    save_input,
    submit_answer,
    is_aoc_season,
    find_module_path_for_problem,
    assert_answer,
)
from src.common.dates import get_current_problem_number, get_current_year
from src.common.meta import load_module

sys.setrecursionlimit(sys.getrecursionlimit())

if "AOC_TOKEN_SESSION" not in os.environ:
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "AOC_TOKEN_SESSION.txt"
        )
    ) as fp:
        os.environ["AOC_TOKEN_SESSION"] = fp.read()


def main(year: str, problem: str):
    execute_problem(year=year, problem_number=problem, send_answer=False)


def main_whole_year(year: str):
    for problem_number in range(1, 25):
        problem_number = str(problem_number).zfill(2)
        execute_problem(year=year, problem_number=problem_number, send_answer=False)


def main_aoc_season():
    execute_problem(
        year=get_current_year(),
        problem_number=get_current_problem_number(),
        send_answer=True,
    )


def execute_problem(year: str, problem_number: str, send_answer: bool):
    # Process and assert problem number
    if isinstance(problem_number, int):
        problem_number = str(problem_number)
    if len(problem_number) == 1:
        problem_number = problem_number.zfill(2)
    elif (not isinstance(problem_number, str)) or len(problem_number) != 2:
        raise ValueError(f"Invalid problem number {problem_number}")
    elif not (1 <= int(problem_number) <= 25):
        raise ValueError(
            f"Problem number must be between 1 and 25, but got {problem_number}"
        )

    # Potentially create input dir and retrieve input file for this day
    path_file_input = get_path_input(
        path_dir_input=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "inputs"
        ),
        problem_number=problem_number,
        year=year,
    )
    if not os.path.exists(path_file_input):
        os.makedirs(os.path.join("inputs", year), exist_ok=True)
        save_input(year=year, day=problem_number, path_file_output=path_file_input)

    # Dynamically load module to execute it
    path_file_module = find_module_path_for_problem(
        year=year,
        problem_number=problem_number,
        path_dir_root=os.path.dirname(os.path.realpath(__file__)),
    )
    module = load_module(module_path=path_file_module)

    # Execute it
    t1 = time.time()
    with open(path_file_input, newline="\n") as fp:
        data = module.parse_input(data=fp.read().strip())
    results = module.main(data)
    t2 = time.time()

    # Beautifully display result
    print(
        format_problem_results(
            problem_number=problem_number,
            results=results,
            time_to_completion=t2 - t1,
        )
    )

    # Optionally submit answer to AOC
    if send_answer:
        if len(results) == 1:
            submit_answer(year=year, day=problem_number, level=1, answer=results[0])
        elif len(results) == 2:
            submit_answer(year=year, day=problem_number, level=2, answer=results[1])
        else:
            raise ValueError(
                f"Impossible to determine level of answer with those results : {results}"
            )
    else:
        # Check answers if the problem has already been resolved
        assert_answer(year=year, day=problem_number, answers=results)


if __name__ == "__main__":
    # During AOC season, override any parameter
    if is_aoc_season():
        main_aoc_season()
        exit(0)

    main(year="2015", problem="19")
