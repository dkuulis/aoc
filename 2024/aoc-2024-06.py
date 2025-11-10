import sys
import re

EMPTY = 0
BLOCK = 16
OBSTACLE = 32
OUTSIDE = 64
VISITED = 15

directions = [1, 2, 4, 8]
deltas = [(0,-1), (1,0), (0,1), (-1,0)]

decode = {'.': EMPTY, '#': BLOCK, '^': directions[0]}

def find_guard(maze):

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell in directions:
                return x, y

def parse(lines):

    l = len(lines) + 2

    tmp = [[OUTSIDE] + [decode[c] for c in line.strip()] + [OUTSIDE] for line in lines]
    maze =  [[OUTSIDE] * l] + tmp + [[OUTSIDE] * l]

    x,y = find_guard(maze)
    maze[y][x] = EMPTY

    return maze, x, y

def walk(maze, x, y, d):

    result = 1

    while True:

        dx, dy = deltas[d]
        nx = x + dx
        ny = y + dy

        m = maze[ny][nx]

        if m == OUTSIDE:
            return result

        if m == BLOCK:
            d = (d + 1) % 4
            continue

        if m == EMPTY:
            result += 1
            maze[y][x] = VISITED

        x, y = nx, ny

def loops(maze, x, y, d):

    loop = set()

    while True:

        p = (x, y, d)
        if p in loop:
            return True
        
        loop.add(p)

        dx, dy = deltas[d]
        nx = x + dx
        ny = y + dy

        m = maze[ny][nx]

        if m == OUTSIDE:
            return False

        if m in [BLOCK, OBSTACLE]:
            d = (d + 1) % 4
            continue

        x, y = nx, ny

def obstacles(maze, x, y, d):

    result = 0

    while True:

        maze[y][x] = VISITED

        dx, dy = deltas[d]
        nx = x + dx
        ny = y + dy
        m = maze[ny][nx]

        if m == OUTSIDE:
            return result

        if m == EMPTY:
            maze[ny][nx] = OBSTACLE
            if loops(maze, x, y, d):
                result += 1
            maze[ny][nx] = EMPTY

        if m in [BLOCK, OBSTACLE]:
            d = (d + 1) % 4
            continue

        x, y = nx, ny

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    maze, x, y = parse(lines)

    #result1 = walk(maze, x, y, 0)
    #print(result1)

    result2 = obstacles(maze, x, y, 0)
    print(result2)

if __name__ == "__main__":
    main()
