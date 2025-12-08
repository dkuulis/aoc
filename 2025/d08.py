import heapq
import lib

def dsquared(p, q):
    return (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2

def part1(flattened, limit):
    circuits: list[set[int]] = []
    for _ in range(limit):
        closest = heapq.heappop(flattened)

        p1 = closest[1][0]
        c1 = next((c for c in circuits if p1 in c), None)
        p2 = closest[1][1]
        c2 = next((c for c in circuits if p2 in c), None)

        if c1 is None and c2 is None:
            circuits.append({p1, p2})
        elif c1 is None:
            c2.add(p1)
        elif c2 is None:
            c1.add(p2)
        elif c1 != c2:
            c1.update(c2)
            circuits.remove(c2)

    sizes = [len(c) for c in circuits]
    sizes.sort(reverse=True)

    return sizes[0] * sizes[1] * sizes[2]

def main():
    lines = lib.read_lines()
    points = [tuple(map(int, line.split(","))) for line in lines]
    size = len(points)

    flattened = [(dsquared(points[i], points[j]), (i, j)) for i in range(size-1) for j in range(i+1, size)]
    heapq.heapify(flattened)

    result1 = part1(flattened, 1000)
    print(result1)

    result2 = 0
    print(result2)


if __name__ == "__main__":
    main()
