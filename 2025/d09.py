import lib

def interval_range(i, j):
    if i <= j:
        return range(i, j+1)
    else:
        return range(i, j-1, -1) # handles descending order

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

def shrink_coordinate(tiles, accessor):
    coordinates = {accessor(t) for t in tiles}
    spaces = {c+1 for c in coordinates}
    index = sorted(coordinates | spaces | {-1})
    mapper = {x:i for i, x in enumerate(index)}
    return mapper

def shrink(tiles):
    mapper_x = shrink_coordinate(tiles, lambda t: t[0])
    mapper_y = shrink_coordinate(tiles, lambda t: t[1])

    shrunk = [(mapper_x[t[0]], mapper_y[t[1]]) for t in tiles]
    return shrunk

def outline(mapped):
    size = len(mapped)
    perimeter = set()
    for i in range(size):
        j = (i+1) % size
        p1 = mapped[i]
        p2 = mapped[j]
        for x in interval_range(p1[0], p2[0]):
            for y in interval_range(p1[1], p2[1]):
                perimeter.add((x,y))
    return perimeter

def is_good(p1, p2, perimeter):
    x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    for p in perimeter:
        if x1 < p[0] < x2 and y1 < p[1] < y2:
            return False

    return True

def part2(tiles, size):
    small = shrink(tiles)
    perimeter = outline(small)

    areas = ((area(tiles[i], tiles[j]), i, j) for i in range(size-1) for j in range(i+1, size))

    for result, i, j in sorted(areas, reverse=True, key = lambda x: x[0]):
        if is_good(small[i], small[j], perimeter):
            return result

def main():
    lines = lib.read_lines()
    tiles = [tuple(map(int, line.split(","))) for line in lines]
    size = len(tiles)

    result1 = max(area(tiles[i], tiles[j]) for i in range(size-1) for j in range(i+1, size))
    print(result1)

    result2 = part2(tiles, size)
    print(result2)

if __name__ == "__main__":
    main()
