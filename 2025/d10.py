import re
import lib
import sys
import operator
from collections import namedtuple
from itertools import combinations
from functools import reduce

Machine = namedtuple('Machine', ["lights", "buttons", "joltages"])

def iterate_with_rest(l):
    for i in range(len(l)):
        chosen = l[i]
        rest = l[:i] + l[i+1:]
        yield chosen, rest

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

def part1(machine: Machine):
    for r in range(len(machine.buttons) + 1):
        for toggles in combinations(machine.buttons, r):
            if machine.lights == reduce(operator.xor, toggles, set()):
                return r

def count_pushes(buttons, joltages, best, previous):

    if not buttons:
        return sys.maxsize # no solution

    button = buttons[0]
    rest = buttons[1:]
    remaining = list(joltages)
    solution = previous + [0]

    max_pushes = min(joltages[counter] for counter in button)
    for pushes in range(max_pushes, -1, -1):

        # new remaining joltages
        for counter in button:
            remaining[counter] = joltages[counter] - pushes

        max_needed_j = max(remaining)
        if pushes + max_needed_j >= best: # cannot improve
            continue

        solution[-1] = pushes
        if max_needed_j > 0: # more push needed
            pushes += count_pushes(rest, remaining, best - pushes, solution)
        else: # already solution
            print(solution)
            pass

        if pushes < best:
            best = pushes

    return best

def part2(machine: Machine):
    print("----")
    descending = sorted(machine.buttons, reverse=True, key=lambda b: len(b))
    remaining = list(machine.joltages)
    result = count_pushes(descending, remaining, sys.maxsize, [])
    if result == sys.maxsize:
        print("xxxxxxx")
    return result

def main():
    lines = lib.read_lines()
    machines = [parse(line) for line in lines]

    result1 = sum(part1(machine) for machine in machines)
    print(result1)

    result2 = sum(part2(machine) for machine in machines)
    print(result2)

if __name__ == "__main__":
    main()
