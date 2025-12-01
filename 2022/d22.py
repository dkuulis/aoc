import re
import lib

maze: list[list[int]] = [[0]]
sizex: int = 0
sizey: int = 0

stitch: dict[tuple[int, int, int], tuple[int, int, int]] = {}

decode = {' ': -1, '.': 0, '#': 1}
turns = {'L': -1, 'R': 1}
directions = [(1,0), (0,1), (-1,0), (0,-1)]
arrows = ">v<^"

pattern = r"(?P<turn>[LR])|(?P<move>\d+)"

def parse(lines):
    global maze
    global sizex
    global sizey

    sizey = len(lines)
    sizex = max(len(line) for line in lines)
    maze = [[decode[c] for c in (line + ' ' * sizex)[:sizex]] for line in lines]

def hop(p, d):
    dx, dy = directions[d]
    return p[0] + dx, p[1] + dy

def outside(p):
    x, y = p
    return x < 0 or y < 0 or x >= sizex or y >= sizey or maze[y][x] == -1

def wrap_stitch():
    global stitch

    wrapx = [lib.min_max(x for x in range(sizex) if maze[y][x] >= 0) for y in range(sizey)]
    wrapy = [lib.min_max(y for y in range(sizey) if maze[y][x] >= 0) for x in range(sizex)]

    stitch = {}
    for y, (x1, x2) in enumerate(wrapx):
        stitch[(x1, y, 2)] = (x2, y, 2)
        stitch[(x2, y, 0)] = (x1, y, 0)

    for x, (y1, y2) in enumerate(wrapy):
        stitch[(x, y1, 3)] = (x, y2, 3)
        stitch[(x, y2, 1)] = (x, y1, 1)

def trace_border(start, initial):

    current = start
    direction = initial
    border = []

    while True:

        border.append((current, direction))

        external = hop(current, direction)
        advance = (direction + 1) % 4

        test1 = hop(current, advance)
        test2 = hop(external, advance)

        if not outside(test2):
            # left turn
            current = test2
            direction = (direction - 1) % 4
        
        else:
            if outside(test1):
                # right turn
                # current is curenton corner, just change direction
                direction = advance

            else:
                # continue straight
                current = test1
                # direction does not change

        if current == start and direction == initial:
            return border

def cube_stitch(start):
    global stitch

    border = trace_border(start[0:2], 3)
    count = len(border)

    leads = []
    for i in range(count):
        j = (i + 1) % count
        pi, di = border[i]
        pj, dj = border[j]
        if hop(pi, di) == hop(pj, dj):
            leads.append((i, j))

    stitch = {}
    while leads:

        leads2 = []
        for i, j in leads:
            bi = border[i]
            bj = border[j]

            si = (bi[0][0], bi[0][1], bi[1])
            sj = (bj[0][0], bj[0][1], bj[1])
            ei = (bi[0][0], bi[0][1], (bi[1] + 2 ) % 4)
            ej = (bj[0][0], bj[0][1], (bj[1] + 2 ) % 4)

            if si not in stitch:
                stitch[si] = ej
                stitch[sj] = ei
                leads2.append(((i - 1) % count, (j + 1) % count))

        leads = leads2

def get_start():
    x = min(x for x in range(sizex) if maze[0][x] >= 0)
    return x, 0, 0

def step(x, y, d):

    s = stitch.get((x,y,d))
    if s:
        return s

    dx, dy = directions[d]
    return x + dx, y + dy, d

def navigate(start, path):
    x, y, d = start
    trace = []

    # for each instruction
    for m in re.finditer(pattern, path):
        turn = m["turn"]
        move = m["move"]

        if turn:
            d = (d + turns[turn]) % 4
            trace.append((x, y, d))

        if move:
            # do a number of steps
            for _ in range(int(move)):
                nx, ny, nd = step(x, y, d)

                # advance if not blocked
                if maze[ny][nx] == 0:
                    x, y, d = nx, ny, nd
                    trace.append((x, y, d))

    return x, y, d, trace

def score(x, y, d):
    return (y + 1) * 1000 + (x + 1) * 4 + d

def main():
    lines = lib.read_lines()
    path = lines[-1]
    lines = lines[:-2]

    parse(lines)

    start = get_start()

    wrap_stitch()
    x, y, d, trace = navigate(start, path)
    result1 = score(x, y, d)
    print(result1)

    cube_stitch(start)
    x, y, d, trace = navigate(start, path)
    result2= score(x, y, d)
    print(result2)


if __name__ == "__main__":
    main()
