import lib

def interval_range(i, j):
    if i <= j:
        return range(i, j+1)
    else:
        return range(i, j-1, -1) # handles descending order
    
def circular(l):
    size = len(l)
    for i in range(size):
        j = (i+1) % size
        yield l[i], l[j]

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

def collect_outline(tiles):
    return {(x,y) for p1, p2 in circular(tiles) for x in interval_range(p1[0], p2[0])  for y in interval_range(p1[1], p2[1])}

def is_good(p1, p2, perimeter):
    x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    for p in perimeter:
        if x1 < p[0] < x2 and y1 < p[1] < y2:
            return False

    return True

def part1(tiles):
    size = len(tiles)
    areas = (area(tiles[i], tiles[j]) for i in range(size-1) for j in range(i+1, size))
    return max(areas)

def part2(tiles):
    size = len(tiles)
    outline = collect_outline(tiles)

    areas = ((area(tiles[i], tiles[j]), i, j) for i in range(size-1) for j in range(i+1, size))
    for result, i, j in sorted(areas, reverse=True, key = lambda x: x[0]):
        if is_good(tiles[i], tiles[j], outline):
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
