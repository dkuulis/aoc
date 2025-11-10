import sys
import re
from collections import Counter
from enum import Enum
from itertools import pairwise
from collections import defaultdict


def parse(lines):

    lines = [l.strip() for l in lines]
    split = next(i for i, e in enumerate(lines) if not e)

    maze = [list(line) for line in lines[:split]]
    moves = ''.join(lines[split+1:])

    return maze, moves

def find_robot(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '@':
                return [x, y]

def maze_gps(maze, symbol):
    gps = 0
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == symbol:
                 gps += 100*y + x
    return gps


directions = { #d y, dx, vertical
    '^': (-1,  0, True),
    '>': ( 0,  1, False),
    'v': ( 1,  0, True),
    '<': ( 0, -1, False)
}

def can_push1(maze, x, y, dx, dy):
    x += dx
    y += dy

    if maze[y][x] == '#':
        return False

    if maze[y][x] == '.':
        return True
    
    return can_push1(maze, x, y, dx, dy)

def do_push1(maze, x, y, dx, dy):
    p = maze[y][x]
    maze[y][x] = '.'

    x += dx
    y += dy

    if maze[y][x] != '.':
        do_push1(maze, x, y, dx, dy)

    maze[y][x] = p


def execute1(maze, move, coords):

    dy, dx, _ = directions[move]
    x, y = coords

    if can_push1(maze, x, y, dx, dy):
        do_push1(maze, x, y, dx, dy)
        coords[0] += dx
        coords[1] += dy

def simulate1(maze, moves, coords):
    
    for move in moves:
        execute1(maze, move, coords)

box = ['[', ']']

def expand_row(row):
    result =  [box[i] if x == 'O' else x for x in row for i in range(2)]
    return result

def expand(maze, corods):
    new_coords = [corods[0]*2, corods[1]]
    new_maze = [expand_row(row) for row in maze]
    new_maze[new_coords[1]][new_coords[0]+1] = "."
    return new_maze, new_coords

def can_push_v2(maze, dy, x, y):
    y += dy

    if maze[y][x] == '#' or maze[y][x+1] == '#':
        return False

    if maze[y][x-1] == '[':
        if not can_push_v2(maze, dy, x-1, y):
            return False

    if maze[y][x] == '[':
        if not can_push_v2(maze, dy, x, y):
            return False

    if maze[y][x+1] == '[':
        if not can_push_v2(maze, dy, x+1, y):
            return False

    return True

def can_push_v1(maze, dy, x, y):
    y += dy

    if maze[y][x] == '#':
        return False

    if maze[y][x-1] == '[':
        return can_push_v2(maze, dy, x-1, y)

    if maze[y][x] == '[':
        return can_push_v2(maze, dy, x, y)
    
    return True

def can_push_h(maze, dx, x, y):
    x += dx
    
    if maze[y][x] == '#':
        return False
    
    if maze[y][x] == '.':
        return True
    
    return can_push_h(maze, dx, x+dx, y)

def can_push2(maze, move, x, y):

    dy, dx, vertical = directions[move]

    if vertical:
        return can_push_v1(maze, dy, x, y)
    else: # horizontal
        return can_push_h(maze, dx, x, y)

def do_push_v2(maze, dy, x, y):

    y += dy
    m1 = maze[y][x-1]
    m2 = maze[y][x]
    m3 = maze[y][x+1]


    if m1 == '[':
        do_push_v2(maze, dy, x-1, y)
        maze[y][x-1] = '.'
    if m2 == '[':
        do_push_v2(maze, dy, x, y)
    if m3 == '[':
        do_push_v2(maze, dy, x+1, y)
        maze[y][x+2] = '.'

    maze[y][x] = '['
    maze[y][x+1] = ']'

def do_push_v1(maze, dy, x, y):

    p = maze[y][x]
    maze[y][x] = '.'

    y += dy
    m1 = maze[y][x-1]
    m2 = maze[y][x]

    if m1 == '[':
        do_push_v2(maze, dy, x-1, y)
        maze[y][x-1] = '.'

    if m2 == '[':
        do_push_v2(maze, dy, x, y)
        maze[y][x+1] = '.'

    maze[y][x] = p

def do_push_h(maze, dx, x, y):

    p = maze[y][x]
    maze[y][x] = '.'

    x += dx

    if maze[y][x] != '.':
        do_push_h(maze, dx, x, y)

    maze[y][x] = p


def do_push2(maze, move, x, y):

    dy, dx, vertical = directions[move]

    if vertical:
        return do_push_v1(maze, dy, x, y)
    else: # horizontal
        return do_push_h(maze, dx, x, y)

def execute2(maze, move, coords):

    x, y = coords
    dy, dx, _ = directions[move]

    if can_push2(maze, move, x, y):
        do_push2(maze, move, x, y)
        coords[0] += dx
        coords[1] += dy

def simulate2(maze, moves, coords):
    
    for move in moves:
        execute2(maze, move, coords)

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    maze, moves = parse(lines)
    coords = find_robot(maze)
    #maze[coords[1]][coords[0]] = '.'

    maze2, coords2 = expand(maze, coords)

    simulate1(maze, moves, coords)
    result1 = maze_gps(maze, 'O')

    simulate2(maze2, moves, coords2)
    result2 = maze_gps(maze2, '[')

    print(result1)
    print(result2)

if __name__ == "__main__":
    main()
