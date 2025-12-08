import heapq
import lib

def dsquared(p, q):
    return (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2

def connect_closest(flattened: list[tuple[int, tuple[int,int]]], circuits: list[set[int]]):
    closest = heapq.heappop(flattened)

    i = closest[1][0]
    ci = next(c for c in circuits if i in c)

    j = closest[1][1]
    cj = next(c for c in circuits if j in c)

    if ci != cj:
        ci.update(cj)
        circuits.remove(cj)

    return i, j

def part1(flattened, circuits, limit):
    for _ in range(limit):
        connect_closest(flattened, circuits)

    sizes = [len(c) for c in circuits]
    sizes.sort(reverse=True)

    return sizes[0] * sizes[1] * sizes[2]

def part2(flattened, circuits):
    while len(circuits) > 1:
        i, j = connect_closest(flattened, circuits)

    return i, j

def main():
    lines = lib.read_lines()
    points = [tuple(map(int, line.split(","))) for line in lines]
    size = len(points)

    distances = [(dsquared(points[i], points[j]), (i, j)) for i in range(size-1) for j in range(i+1, size)]
    heapq.heapify(distances)

    circuits = [{c} for c in range(size)]

    result1 = part1(distances, circuits, 1000)
    print(result1)

    i, j = part2(distances, circuits)
    result2 = points[i][0] * points[j][0]
    print(result2)

if __name__ == "__main__":
    main()
