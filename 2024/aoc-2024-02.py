import sys
from collections import Counter
from enum import Enum
from itertools import pairwise

class Direction(Enum):
    UNKNOWN = 0
    UP = 1
    DOWN = 2

def is_safe1(report):

    direction = Direction.UNKNOWN
    previous = None

    for level in report:

        if previous:

            delta = level - previous

            if delta == 0:
                return False

            if delta > 3 or  delta < -3:
                return False

            if delta > 0 and direction == Direction.DOWN:
                return False

            if delta < 0 and direction == Direction.UP:
                return False

            if direction == Direction.UNKNOWN:
                direction = Direction.UP if delta > 0 else Direction.DOWN

        previous = level

    return True

def is_good(x, r):
    return (
        (x in {-3, -2, -1, 1, 2, 3}) and
        ((x > 0) if r > 0 else (x < 0))
    )

def is_safe1a(report):
    
    deltas = [b-a for a, b in pairwise(report)]
    return all([is_good(x, deltas[0]) for x in deltas])

def is_safe2(report):

    if len(report) <= 2:
        return True

    deltas = [b-a for a, b in pairwise(report)]

    e = (i for i, x in enumerate(deltas) if not is_good(x, deltas[0]))
    bad = next(e, -1)
    bad2 = next(e, -1)

    if bad == -1:
        return True
    
    r1 = report[:bad] + report[bad+1:]
    r2 = report[:bad+1] + report[bad+2:]

    s1 = is_safe1a(r1)
    s2 = is_safe1a(r2)

    if not s1 and not s2:
        print(bad, bad2, report, deltas)

    return s1 or s2

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    safe = 0
    for line in lines:
        report = list(map(int, line.split()))
        if is_safe2(report):
            safe += 1

    print(safe)

if __name__ == "__main__":
    main()
