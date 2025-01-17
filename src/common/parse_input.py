import os
import re

from src.common.iterators import batched


def get_path_input(path_dir_input: str, problem_number: int):
    return os.path.join(path_dir_input, f"{problem_number}.txt")


def parse_input(path_dir_input: str, problem_number: int):
    path_input = get_path_input(
        path_dir_input=path_dir_input, problem_number=problem_number
    )

    with open(path_input) as fp:
        match problem_number:
            case 2:
                lines = []
                for line in fp.readlines():
                    # For both problems, no need to split between each cube draw
                    # Furthermore, we can deduce game ID with line index, so we can safely remove it.
                    line = re.sub("[;,:]", "", line).split()[2:]
                    line = batched(line, 2)  # Split in chunks of 2
                    lines.append(line)
                return lines
            case 4:
                lines = []
                for line in fp.readlines():
                    line = line.split(":")[1]  # Remove card number

                    # Parse numbers
                    numbers_winning, numbers_i_have = line.split(" | ")
                    numbers_winning = numbers_winning.strip().split(" ")
                    numbers_i_have = numbers_i_have.strip().split(" ")
                    numbers_winning = [
                        int(number) for number in numbers_winning if number != ""
                    ]
                    numbers_i_have = [
                        int(number) for number in numbers_i_have if number != ""
                    ]
                    lines.append([numbers_winning, numbers_i_have])
                return lines
            case 5:
                seeds, *maps = fp.read().split("\n\n")

                seeds = list(map(int, seeds.split(": ")[1].split(" ")))

                maps_cleaned = []
                for m in maps:
                    m = m.split("map:")[1]  # Remove useless data
                    m = m.strip().split("\n")  # Split each map
                    m = [
                        {
                            "dest_range_start": int(line[0]),
                            "src_range_start": int(line[1]),
                            "range_length": int(line[2]),
                        }
                        for line in [data.split() for data in m]
                    ]
                    maps_cleaned.append(m)
                return {"seeds": seeds, "almanac": maps_cleaned}
            case 7:
                lines = []
                for line in fp.readlines():
                    hand, bid = line.split(" ")
                    lines.append({"hand": hand, "bid": int(bid)})
                return lines
            case 8:
                lines = fp.readlines()
                instructions = lines[0].strip()
                nodes = [node.strip() for node in lines[2:]]
                parsed_nodes = []
                for node in nodes:
                    node = node.split(" = ")
                    node[1] = node[1][1:-1].split(", ")
                    parsed_nodes.append(node)
                cleaned_nodes = {}
                for node, (node_left, node_right) in parsed_nodes:
                    cleaned_nodes[node] = {"left": node_left, "right": node_right}
                return (instructions, cleaned_nodes)
            case 9:
                return [list(map(int, line.strip().split())) for line in fp.readlines()]
            case 12:
                lines = []
                for line in fp.readlines():
                    springs, damaged_springs = line.split(" ")
                    damaged_springs = list(map(int, damaged_springs.strip().split(",")))
                    lines.append((springs, damaged_springs))
                return lines
            case 13:
                return list(map(lambda line: line.split(), fp.read().split("\n\n")))
            case 15:
                return fp.read().strip().split(",")
            case 17:
                lines = []
                for line in fp.readlines():
                    lines.append([int(c) for c in line.strip()])
                return lines
            case 18:
                lines = []
                for line in fp.readlines():
                    line = line.strip().split(" ")
                    lines.append(
                        {
                            "dig_direction": line[0],
                            "dig_depth": int(line[1]),
                            "color": line[2].replace("(", "").replace(")", ""),
                        }
                    )
                return lines
            case _:
                return [line.strip() for line in fp.readlines()]
