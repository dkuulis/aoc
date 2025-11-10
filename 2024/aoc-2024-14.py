import sys
import re
from collections import namedtuple

Robot = namedtuple('Machine', ['px', 'py', 'dx', 'dy'])

def parse(lines):
    
    size = [int(num) for num in lines[0].split()]

    robots = []

    for line in lines[1:]:

        match = re.findall(r'-?\d+', line)
        d = [int(num) for num in match]
        r = Robot(d[0], d[1], d[2], d[3])

        robots.append(r)

    return size[0], size[1], robots

def sign(n):
    return (n > 0) - (n < 0)

def solve1(sx, sy, robots, t):

    quadrants = [0 for _ in range(9)]
    debug = [[0 for _ in range(sx)] for _ in range(sy)]

    hx = sx //2
    hy = sy //2

    for r in robots:
        x = (r.px + t*r.dx) % sx
        y = (r.py + t*r.dy) % sy

        debug[y][x] += 1

        ax = sign(x - hx)
        ay = sign(y - hy)

        q = (ax+1)+3*(ay+1)
        quadrants[q] += 1

    return quadrants[0]*quadrants[2]*quadrants[6]*quadrants[8], debug

def has_five_consecutive_ones(arr):
    count = 0
    for num in arr:
        if num == 1:
            count += 1
            if count == 5:
                return True
        else:
            count = 0
    return False


def has_line(debug):
    for line in debug:
        count = 0
        for n in line:
            if n > 0:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
    return False

def display(debug):

    for row in debug:
        t = ''.join(['.' if d == 0 else chr(48 + d) for d in row])
        print(t)

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    sx, sy, robots = parse(lines)

    result1, debug1 = solve1(sx, sy, robots, 100)
    print(result1)

    t = 0
    while True:
        t += 1
        result2, debug2 = solve1(sx, sy, robots, t)
        if has_line(debug2):
            print()
            print(t)
            display(debug2)

if __name__ == "__main__":
    main()
