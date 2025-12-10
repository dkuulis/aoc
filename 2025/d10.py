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

def choose_buttons(machine: Machine):
    for r in range(len(machine.buttons) + 1):
        for toggles in combinations(machine.buttons, r):
            if machine.lights == reduce(operator.xor, toggles, set()):
                return r

def count_pushes(buttons, joltages, best, pressed):
    for button, rest in iterate_with_rest(buttons):

        button_pushes = min(joltages[counter] for counter in button)
        if button_pushes == 0: # buton cannot be pushed
            continue

        # new remaining joltages
        remaining_js = list(joltages)
        for counter in button:
            remaining_js[counter] -= button_pushes

        max_needed_j = max(remaining_js)
        if button_pushes + max_needed_j >= best: # cannot improve
            continue

        result = pressed | {str(button): button_pushes}
        if max_needed_j > 0: # more push needed
            button_pushes += count_pushes(rest, remaining_js, best - button_pushes, result)
        else:
            print(result) 

        if button_pushes < best:
            best = button_pushes

    return best

def choose_joltages(machine: Machine):
    print("----")
    descending = sorted(machine.buttons, reverse=True, key=lambda b: len(b))
    remaining = list(machine.joltages)
    return count_pushes(descending, remaining, sys.maxsize, {})

def main():
    lines = lib.read_lines("init")
    machines = [parse(line) for line in lines]

    result1 = sum(choose_buttons(machine) for machine in machines)
    print(result1)

    result2 = sum(choose_joltages(machine) for machine in machines)
    print(result2)

if __name__ == "__main__":
    main()
