import sys
from collections import deque

def parse(lines):
    maze = [list(line.strip()) for line in lines]
    return maze

def find(maze, symbol):
    for y, row in enumerate(maze):
        if symbol in row:
            return (row.index(symbol), y)

directions = [(1,0), (0,1), (-1,0), (0,-1)]

def neighbours(p, maze):
    size = len(maze)
    x, y = p
    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < size and ny >= 0 and ny < size:
            yield (nx,ny)

def get(data, coord):
    x, y = coord
    return data[y][x]

def set(data, coord, value):
    x, y = coord
    data[y][x] = value

def analyze(maze, head, finish):

    size = len(maze)
    distance = [[-1 for _ in range(size)] for _ in range(size)]
    path = []
    d = 0
    
    while True:
        path.append(head)
        set(distance, head, d)

        if head == finish:
            break

        d += 1
        for next in neighbours(head, maze):
            if get(maze, next) != '#' and get(distance, next) == -1:
                head = next
                break

    return path, distance

def stepcheats2(maze, distance, p1, p2):

    if get(maze, p2) != '#':
        return

    d1 = get(distance, p1)

    for p3 in neighbours(p2, maze):

        d3 = get(distance, p3)
        save = d3 - d1 - 2
        if save > 0:
            yield (save, p1, p2, p3)

def stepcheats(maze, path, distance):
    cheats = []

    for p in path:
        for next in neighbours(p, maze):
            cheats.extend(stepcheats2(maze, distance, p, next))

    return cheats

def fillwalls(maze, start, limit):
    region = {start: 0}
    queue = deque([start])

    while queue:
        p = queue.popleft()
        d = region[p] + 1

        if p == start or get(maze, p) == '#':
            for n in neighbours(p, maze):
                t = region.get(n, 10000000)
                if (t > d):
                    region[n] = d
                    queue.append(n)

    return {k: v for k, v in region.items() if v <= limit and v > 0}

def jumpcheats2(maze, distance, start, limit):

    region = fillwalls(maze, start, limit)
    ds = get(distance, start)

    result = []
    for p, d in region.items():
        dp = get(distance, p)
        save = dp - ds - d
        if save > 0:
            result.append((save, start, p))

    return result

def jumpcheats(maze, path, distance, limit):
    jumps = []

    for p in path:
        jumps.extend(jumpcheats2(maze, distance, p, limit))

    return jumps

def areacheats2(maze, distance, start, limit):

    result = []
    size = len(maze)
    x, y = start
    ds = get(distance, start)
    
    for dx in range(-limit, limit+1):
         adx = abs(dx)
         for dy in range(-limit+adx, limit+1-adx):
             if dx != 0 or dy != 0:
                nx = x + dx
                ny = y + dy
                if nx >= 0 and nx < size and ny >= 0 and ny < size:
                    ady = abs(dy)
                    p = (nx, ny)
                    dn = get(distance, p)
                    save = dn - ds - adx - ady
                    if save >= 100:
                        result.append((save, start, p))

    return result

def areacheats(maze, path, distance, limit):
    jumps = []

    for p in path:
        jumps.extend(areacheats2(maze, distance, p, limit))

    return jumps

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    maze = parse(lines)
    start = find(maze, 'S')
    finish = find(maze, 'E')
    path, distance = analyze(maze, start, finish)

    #cheats  = stepcheats(maze, path, distance)
    #result1 = sum(1 for c in cheats if c[0] >= 100)
    #print(result1)

    cheats2  = areacheats(maze, path, distance, 20)
    result2 = sum(1 for c in cheats2 if c[0] >= 100)
    print(result2)

if __name__ == "__main__":
    main()
