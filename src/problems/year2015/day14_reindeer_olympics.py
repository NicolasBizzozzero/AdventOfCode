import copy
from collections import defaultdict
from dataclasses import dataclass

from src.common.structures import defaultdict_to_dict


@dataclass
class Reindeer:
    name: str
    speed: int
    endurance: int
    rest: int


def parse_input(data: str):
    reindeers = []
    for row in data.split("\n"):
        name = row.split(" ")[0]
        speed = int(row.split(" ")[3])
        endurance = int(row.split(" ")[6])
        rest = int(row.split(" ")[-2])
        reindeers.append(Reindeer(*(name, speed, endurance, rest)))

    return reindeers


def main(reindeers: list[Reindeer]) -> tuple[int, int]:
    return (
        level1(reindeers=copy.deepcopy(reindeers)),
        level2(reindeers=copy.deepcopy(reindeers)),
    )


def level1(reindeers: list[Reindeer]) -> int:
    results = distance_after(seconds=2_503, reindeers=reindeers)
    return max(results.values())


def level2(reindeers: list[Reindeer]) -> int:
    results = score_after(seconds=2_503, reindeers=reindeers)
    return max(results.values())


def distance_after(seconds: int, reindeers: list[Reindeer]) -> dict[str, int]:
    results = {}
    for reindeer in reindeers:
        results[reindeer.name] = simulate(reindeer=reindeer, until=seconds)
    return results


def score_after(seconds: int, reindeers: list[Reindeer]) -> dict[str, int]:
    results = defaultdict(int)
    scores = {}
    for second in range(1, seconds + 1):
        for reindeer in reindeers:
            scores[reindeer.name] = simulate(reindeer=reindeer, until=second)

        # Get all best reindeers
        best_score = max(scores.values())
        best_reindeers = [
            reindeer for reindeer, score in scores.items() if score == best_score
        ]

        for reindeer in best_reindeers:
            results[reindeer] += 1
    return defaultdict_to_dict(results)


def simulate(reindeer: Reindeer, until: int) -> int:
    seconds = 0
    distance = 0
    while seconds < until:
        remaining_seconds = until - seconds

        # Check if reindeer can fly a full endurance bar and still having seconds remaining
        if reindeer.rest + reindeer.endurance <= remaining_seconds:
            distance += reindeer.endurance * reindeer.speed
            seconds += reindeer.rest + reindeer.endurance
            continue

        # Check if reindeer can fly a full endurance bar but will be at rest while time expire
        elif reindeer.endurance <= remaining_seconds:
            distance += reindeer.endurance * reindeer.speed
            break

        # Reindeer can only fly a partial endurance bar
        else:
            distance += remaining_seconds * reindeer.speed
            break
    return distance
