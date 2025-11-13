import heapq
from typing import Generator
import lib

map: list[list[int]] = [[0]]
size: int = 0
size1: int = 0
inf = 9999999

directions = [(1,0), (0,1), (-1,0), (0,-1)]

#simple neighbourhood
def simple(position: tuple[tuple[int,int], int, int]):

    (x,y), direction, length = position
    for d, (dx, dy) in enumerate(directions):

        # cant turn around
        if (d + 2) % 4 == direction:
            continue

        # max 3 steps forward
        if d == direction and length >= 3:
            continue

        nx, ny = x + dx, y + dy

        # stay within map
        if nx < 0 or ny < 0 or nx >= size or ny >= size:
            continue

        # count steps
        l = length + 1 if d == direction else 1
        delta = map[ny][nx]

        yield ((nx, ny), d, l), delta

#ultra neighbourhood
def ultra(position: tuple[tuple[int,int], int, int]):

    (x,y), direction, length = position
    for d, (dx, dy) in enumerate(directions):

        # cant turn around
        if (d + 2) % 4 == direction:
            continue

        # max 10 steps forward
        if d == direction and length >= 10:
            continue

        nx, ny, delta = x, y, 0
        steps = 1 if d == direction else 4
        l = length + 1 if d == direction else 4
        for _ in range(steps):
            nx += dx
            ny += dy
            if nx >= 0 and ny >= 0 and nx < size and ny < size:
                delta += map[ny][nx]

        # stay within map
        if nx < 0 or ny < 0 or nx >= size or ny >= size:
            continue

        yield ((nx, ny), d, l), delta

def search(start, goal, neighbours):

    visited = set()
    distance = {}
    heap = [(0, (start, -1, 0))] # (cost, (point, direction, length))

    while heap:
        cost, position = heapq.heappop(heap)
        if position[0] == goal:
            return cost
        
        if position in visited:
            continue
        visited.add(position)

        for next, delta in neighbours(position):
            new_cost = cost + delta
            if new_cost < distance.get(next, inf):
                distance[next] = new_cost
                heapq.heappush(heap, (new_cost, next))

    return None

def main():
    global map
    global size
    global size1

    lines = lib.read_lines()
    map = [[int(c) for c in line] for line in lines]
    size = len(map)
    size1 = size - 1

    result1 = search((0,0), (size1, size1), simple)
    print(result1)

    result2 = search((0,0), (size1, size1), ultra)
    print(result2)

if __name__ == "__main__":
    main()
