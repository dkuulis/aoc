from itertools import accumulate
import re
import lib

pattern = r"(?P<dir>[LR])(?P<count>\d+)"
directions = {"L": -1, "R": 1}

def zero_x_point(input, delta):
    point = input[0]

    result = point + delta

    c = 0 if delta > 0 else 1 # zero click point
    h1 = (point - c) // 100 # starting hundred
    h2 = (result - c) // 100 # final hundred
    xing = abs(h1 - h2) # crossings

    return result, xing

def main():
    lines = lib.read_lines()
    moves = [lib.ints(re.match(pattern, line).groupdict()) for line in lines]
    deltas = [directions[m["dir"]] * m["count"] for m in moves]

    points = list(accumulate(deltas, lambda x, y: (x + y) % 100, initial = 50))
    result1 = points.count(0)
    print(result1)

    xings = list(accumulate(deltas, zero_x_point, initial = (50,0)))
    result2 = sum(x[1] for x in xings)
    print(result2)

if __name__ == "__main__":
    main()
