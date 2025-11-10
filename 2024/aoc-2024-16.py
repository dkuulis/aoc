import sys
import heapq

def parse(lines):
    maze = [line.strip() for line in lines]
    return maze

def find(maze, symbol):
    for y, row in enumerate(maze):
        x = row.find(symbol)
        if x >= 0:
            return (x, y)

definitions = [(1,0), (0,1), (-1,0), (0,-1)]
neighbours = [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,-1), (0,0,1)]

def solve1(maze, start, finish):

    size = len(maze)
    distance = [[[[-1, set()] for _ in range(4)] for _ in range(size)] for _ in range(size)]

    queue = []
    heapq.heappush(queue, (0, (start) + (0,None)))

    while queue:
        cost, coord = heapq.heappop(queue)
        x, y, d, parent = coord
        known = distance[y][x][d]

        if known[0] == -1 or known[0] >= cost:

            distance[y][x][d][0] = cost
            if parent:
                distance[y][x][d][1].add(parent)
            dx, dy = definitions[d]

            # extend queue - add neighbours

            np = (x, y, d)
            nx = x + dx
            ny = y + dy
            if maze[ny][nx] != '#':
                heapq.heappush(queue, (cost+1, (nx, ny, d, np)))

            heapq.heappush(queue, (cost+1000, (x, y, (d+1)%4, np)))
            heapq.heappush(queue, (cost+1000, (x, y, (d-1)%4, np)))

    x, y = finish
    results = [distance[y][x][d][0] for d in range(4)]
    return min(results), distance

def solve2(maze, start, finish, distance, level):

    x, y = finish
    points = set()
    heads = [(x, y, d) for d, c in enumerate(distance[y][x] )if c[0] == level]

    while heads:
        coord = heads.pop()
        x, y, d = coord
        head = distance[y][x][d]
        points.add((x, y))
        maze[y] = maze[y][:x]+'O'+maze[y][x+1:]
        heads.extend(head[1])

    return len(points)

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    maze = parse(lines)
    start = find(maze, 'S')
    finish = find(maze, 'E')

    result1, distance = solve1(maze, start, finish)
    result2 = solve2(maze, start, finish, distance, result1)

    print(result1)
    print(result2)

if __name__ == "__main__":
    main()
