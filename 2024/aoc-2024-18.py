import sys
from collections import deque

def parse(lines):
   sx, sy, l = [int(num) for num in lines[0].strip().split(',')]
   bytes = [tuple(int(num) for num in line.strip().split(',')) for line in lines[2:]]
   return (sx, sy), l, bytes

def generate(size, bytes):

    sx, sy = size
    line = [1 for _ in range(sx+2)]
    maze = [line] + [[1] + [0 for _ in range(sx)] + [1] for _ in range(sy)] + [line]

    for c in bytes:
        x, y = c[0]+1, c[1]+1
        maze[y][x] = 1
    
    return maze

def solve1(maze, big):

    sx, sy = len(maze[0]), len(maze)
    distance = [[big for _ in range(sx)] for _ in range(sy)]

    start = (1,1,0)
    queue = deque([start])

    while queue:
        x, y, d = queue.popleft()
        t = distance[y][x]
        if t > d:
            distance[y][x] = d

            # extend
            for dx, dy in [(0, 1), (1, 0), (0,-1), (-1, 0)]:
                if maze[y+dy][x+dx] == 0:
                    queue.append((x+dx,y+dy,d+1))

    return distance[sy-2][sx-2]

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    size, l, bytes = parse(lines)
    big = 2*size[0]*size[1]
    maze = generate(size, bytes[:l])
    result = solve1(maze, big)
    print(result)

    while l < len(bytes):
        x, y = bytes[l][0]+1, bytes[l][1]+1
        maze[y][x] = 1

        result2 = solve1(maze, big)
        print(l, result2, bytes[l])
        if result2 == big:
            print(l, bytes[l])
            break

        l += 1

if __name__ == "__main__":
    main()
