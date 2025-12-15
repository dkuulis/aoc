import re
import lib
import sys
import operator
from collections import namedtuple
from itertools import combinations
from functools import reduce

Machine = namedtuple('Machine', ["lights", "buttons", "joltages"])

def parse(line):

    pattern = r"\[(?P<lights>[.#]+)\] (?P<buttons>[\d,\(\) ]+) \{(?P<joltages>[\d,]+)\}"
    m = re.match(pattern, line)

    lights_str = m["lights"]
    lights = {i for i, c in enumerate(lights_str) if c  == "#"}

    buttons_re = r"\((?P<button>\d+(,\d+)*)\)"
    buttons_str = m["buttons"]
    buttons = [set(map(int, b["button"].split(","))) for b in re.finditer(buttons_re, buttons_str)]

    joltages_str = m["joltages"]
    joltages = list(map(int, joltages_str.split(",")))

    return Machine(lights, buttons, joltages)

def part1(buttons: list[set[int]], lights: set[int]):
    for r in range(len(buttons) + 1):
        for toggles in combinations(buttons, r):
            if lights == reduce(operator.xor, toggles, set()):
                return r

def part2(buttons: list[set[int]], joltages: list[int]):

    result = 0
    m = 1
    while any(j for j in joltages if j > 0):
        odds = {i for i, j in enumerate(joltages) if j & 1}
        t = part1(buttons, odds)
        result += m*t
        m *= 2
        joltages = [j // 2 for j in joltages]

    return result

def main():
    lines = lib.read_lines()
    machines = [parse(line) for line in lines]

    result1 = sum(part1(machine.buttons, machine.lights) for machine in machines)
    print(result1)

    result2 = sum(part2(machine.buttons, machine.joltages) for machine in machines)
    print(result2)

if __name__ == "__main__":
    main()
