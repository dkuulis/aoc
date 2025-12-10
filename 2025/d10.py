import re
import lib
from collections import namedtuple
from itertools import combinations
from functools import reduce
import operator

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

def choose_buttons(machine):
    for r in range(len(machine.buttons) + 1):
        for toggles in combinations(machine.buttons, r):
            if machine.lights == reduce(operator.xor, toggles, set()):
                return r

def choose_joltages(machine):
    return 0

def main():
    lines = lib.read_lines()
    machines = [parse(line) for line in lines]

    result1 = sum(choose_buttons(machine) for machine in machines)
    print(result1)

    result2 = sum(choose_joltages(machine) for machine in machines)
    print(result2)

if __name__ == "__main__":
    main()
