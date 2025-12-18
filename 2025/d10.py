import re
import lib
import sys
from functools import cache
from collections import namedtuple
from itertools import combinations
from functools import reduce

Machine = namedtuple('Machine', ["lights", "buttons", "joltages"])

def parse(line):

    pattern = r"\[(?P<lights>[.#]+)\] (?P<buttons>[\d,\(\) ]+) \{(?P<joltages>[\d,]+)\}"
    m = re.match(pattern, line)

    lights_str = m["lights"]
    lights = tuple(int(c  == "#")for c in lights_str)

    size = len(lights)

    buttons_re = r"\((?P<button>\d+(,\d+)*)\)"
    buttons_str = m["buttons"]
    buttons_map = [set(map(int, b["button"].split(","))) for b in re.finditer(buttons_re, buttons_str)]
    buttons = [tuple(int(i in b) for i in range(size)) for b in buttons_map]

    joltages_str = m["joltages"]
    joltages = tuple(map(int, joltages_str.split(",")))

    return Machine(lights, buttons, joltages)

def part1(buttons: list[tuple[int, ...]], lights: tuple[int, ...]) -> int:
    empty = (0,) * len(buttons[0])
    for r in range(len(buttons) + 1):
        for selection in combinations(buttons, r):
            if lights == reduce(lambda a, b: tuple(x ^ y for x, y in zip(a,b)), selection, empty):
                return r

def combine(buttons: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    result = {}

    empty = (0,) * len(buttons[0])
    for r in range(len(buttons) + 1):
        for selection in combinations(buttons, r):
            pattern = reduce(lambda a, b: tuple(x + y for x, y in zip(a,b)), selection, empty)
            result.setdefault(pattern, r)

    return result

def part2(buttons: list[tuple[int, ...]], joltages: tuple[int, ...]) -> int:
    costs = combine(buttons)

    @cache
    def solve(target: tuple[int, ...]) -> int:
        if max(target) == 0:
            return 0

        result = sys.maxsize
        for pattern, cost in costs.items():
            if cost < result and all(a <= b and a & 1 == b & 1 for a, b in zip(pattern, target)):
                next = tuple((b - a) // 2 for a, b in zip(pattern, target))
                result = min(result, 2 * solve(next) + cost)

        return result

    return solve(joltages)

def main():
    lines = lib.read_lines()
    machines = [parse(line) for line in lines]

    result1 = sum(part1(machine.buttons, machine.lights) for machine in machines)
    print(result1)

    result2 = sum(part2(machine.buttons, machine.joltages) for machine in machines)
    print(result2)

if __name__ == "__main__":
    main()
