import datetime

from src.aoc_utils import is_aoc_season


def get_current_problem_number() -> str | None:
    current_time = datetime.datetime.now()

    # If we are outside AoC dates, returns all problems
    if not is_aoc_season():
        return None

    if current_time.hour >= 6:
        problem_number = current_time.day
    else:
        problem_number = (current_time - datetime.timedelta(days=1)).day

    return str(problem_number).zfill(2)


def get_current_year() -> str:
    return str(datetime.datetime.now().year)