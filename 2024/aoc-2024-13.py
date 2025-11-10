import sys
import re
from collections import namedtuple

Machine = namedtuple('Machine', ['ax', 'ay', 'bx', 'by', 'px', 'py'])


def parse(lines):
    
    machines = []
    for i in range(0, len(lines), 4):

        atext = re.findall(r'\d+', lines[i])
        a = [int(num) for num in atext]

        btext = re.findall(r'\d+', lines[i+1])
        b = [int(num) for num in btext]

        ptext = re.findall(r'\d+', lines[i+2])
        p = [int(num) for num in ptext]

        m = Machine(a[0], a[1], b[0], b[1], p[0], p[1])

        machines.append(m)

    return machines

def play1(machine):

    a = 0
    b = min(100, machine.px // machine.bx, machine.py // machine.by)

    while True:

        bx = b * machine.bx
        by = b * machine.by

        tx = machine.px - bx
        ty = machine.py - by

        a = min(tx // machine.ax, ty // machine.ay)

        if a > 100:
            return 0

        if a*machine.ax == tx and a*machine.ay == ty:
            return a*3 + b

        b -= 1

        if b < 0:
            return 0

def solve1(machines):
    
    return sum(play1(m) for m in machines)

def solve_linear_system(a1, b1, c1, a2, b2, c2):

    # Calculate the determinant
    D = a1 * b2 - a2 * b1

    if D == 0:
        return 0
    
    # Cramer's Rule
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1

    x = Dx // D
    y = Dy // D

    t1 = a1*x + b1*y - c1
    t2 = a2*x + b2*y - c2

    if t1 == 0 and t2 == 0 and x >= 0 and y >= 0:
        return x*3 + y
    else:
        return 0

def play2(machine):

    px = machine.px + 10000000000000
    py = machine.py + 10000000000000

    result =  solve_linear_system(machine.ax, machine.bx, px, machine.ay, machine.by, py)
    return result

def solve2(machines):
    
    return sum(play2(m) for m in machines)

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    machines = parse(lines)
    result1 = solve1(machines)
    result2 = solve2(machines)

    print(result1, result2)

if __name__ == "__main__":
    main()
