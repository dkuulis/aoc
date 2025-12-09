import lib

def circular(l):
    size = len(l)
    for i in range(size):
        j = (i+1) % size
        yield l[i], l[j]

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

def is_good(p1, p2, tiles):
    # min/max coordinates
    px1, px2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    py1, py2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    for q1, q2 in circular(tiles):
        # min/max coordinates
        qx1, qx2 = min(q1[0], q2[0]), max(q1[0], q2[0])
        qy1, qy2 = min(q1[1], q2[1]), max(q1[1], q2[1])

        # Two rectangles do not intersect if one is completely to the left, right, above, or below the other
        if not(px2 <= qx1 or qx2 <= px1 or py2 <= qy1 or qy2 <= py1):
            return False # part of outline is inside

    return True

def part1(tiles):
    size = len(tiles)
    areas = (area(tiles[i], tiles[j]) for i in range(size-1) for j in range(i+1, size))
    return max(areas)

def part2(tiles):
    size = len(tiles)
    areas = ((area(tiles[i], tiles[j]), i, j) for i in range(size-1) for j in range(i+1, size))
    for result, i, j in sorted(areas, reverse=True, key = lambda x: x[0]):
        if is_good(tiles[i], tiles[j], tiles):
            return result

def main():
    lines = lib.read_lines()
    tiles = [tuple(map(int, line.split(","))) for line in lines]

    result1 = part1(tiles)
    print(result1)

    result2 = part2(tiles)
    print(result2)

if __name__ == "__main__":
    main()
