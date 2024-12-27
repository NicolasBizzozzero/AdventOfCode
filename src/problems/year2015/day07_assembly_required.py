import copy
from dataclasses import dataclass


@dataclass
class Wire:
    gate: str
    source1: str
    source2: str | None


def parse_input(data: str):
    wires = dict()
    for row in data.split("\n"):
        row = row.strip()
        gate, source1, source2, destination = None, None, None, None
        if row.startswith("NOT"):
            gate = "NOT"
            source1 = row.split("NOT ")[1].split(" ->")[0]
            destination = row.split("-> ")[-1]
        elif len(row.split(" ")) == 3:
            gate = "INPUT"
            source1 = row.split(" ->")[0]
            destination = row.split("-> ")[-1]
        else:
            gate = row.split(" ")[1]
            source1 = row.split(" ")[0]
            source2 = row.split(" ")[2]
            destination = row.split(" ")[-1]

        wires[destination] = Wire(gate=gate, source1=source1, source2=source2)
    return wires


def main(wires: dict[str, Wire]) -> tuple[int, int]:
    return (level1(wires=copy.deepcopy(wires)), level2(wires=copy.deepcopy(wires)))


def level1(wires: dict[str, Wire]) -> int:
    return signal(wire="a", wires=wires)


def level2(wires: dict[str, Wire]) -> int:
    return signal(
        wire="a", wires=wires, computed_signals={"b": signal(wire="a", wires=wires)}
    )


def signal(wire: str, wires: dict[str, Wire], computed_signals: dict = None) -> int:
    if computed_signals is None:
        computed_signals = {}

    # If "wire" is an int (a signal), just return it
    try:
        return int(wire)
    except ValueError:
        pass

    wire_name = wire
    if wire not in computed_signals:
        wire = wires[wire]
        match wire.gate:
            case "INPUT":
                result = signal(
                    wire=wire.source1,
                    wires=wires,
                    computed_signals=computed_signals,
                )
            case "NOT":
                result = ~signal(
                    wire=wire.source1,
                    wires=wires,
                    computed_signals=computed_signals,
                )
            case "AND":
                result = signal(
                    wire=wire.source1,
                    wires=wires,
                    computed_signals=computed_signals,
                ) & signal(
                    wire=wire.source2,
                    wires=wires,
                    computed_signals=computed_signals,
                )
            case "OR":
                result = signal(
                    wire=wire.source1, wires=wires, computed_signals=computed_signals
                ) | signal(
                    wire=wire.source2, wires=wires, computed_signals=computed_signals
                )
            case "LSHIFT":
                result = signal(
                    wire=wire.source1, wires=wires, computed_signals=computed_signals
                ) << int(wire.source2)
            case "RSHIFT":
                result = signal(
                    wire=wire.source1, wires=wires, computed_signals=computed_signals
                ) >> int(wire.source2)
        computed_signals[wire_name] = result
    return computed_signals[wire_name]
