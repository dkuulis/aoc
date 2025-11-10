import re
import lib

def execute(command, lights):
    c = command['action']
    for x in range(int(command['x1']), int(command['x2'])+1):
        for y in range(int(command['y1']), int(command['y2'])+1):
            lights[y][x] = 1 if c == "turn on" else 0 if c == "turn off" else lights[y][x] ^ 1

def execute2(command, lights):
    c = command['action']
    for x in range(int(command['x1']), int(command['x2'])+1):
        for y in range(int(command['y1']), int(command['y2'])+1):
            lights[y][x] = max(0, lights[y][x] + (1 if c == "turn on" else -1 if c == "turn off" else 2))

pattern  = r"(?P<action>(turn on|turn off|toggle)) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)"

def main():
    lines = lib.read_lines()
    commands = [re.match(pattern, line).groupdict() for line in lines]

    size = 1000
    lights = [[0 for _ in range(size)] for _ in range(size)]
    lights2 = [[0 for _ in range(size)] for _ in range(size)]

    for command in commands:
        execute(command, lights)
    result1 = sum(sum(row) for row in lights)
    print(result1)

    for command in commands:
        execute2(command, lights2)
    result2 = sum(sum(row) for row in lights2)
    print(result2)

if __name__ == "__main__":
    main()
