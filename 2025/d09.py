import lib

def interval_range(i, j):
    if i <= j:
        return range(i, j+1)
    else:
        return range(i, j-1, -1) # handles descending order

def area(p, q):
    return (abs(p[0]-q[0])+1) * (abs(p[1]-q[1])+1)

def map_tiles(tiles):
    index_x = sorted({t[0] for t in tiles} | {t[0]+1 for t in tiles} | {-1})
    map_x = {x:i for i, x in enumerate(index_x)}
    size_x = len(index_x)

    index_y = sorted({t[1] for t in tiles} | {t[1]+1 for t in tiles} | {-1})
    map_y = {y:j for j, y in enumerate(index_y)}
    size_y = len(index_y)

    mapped = [(map_x[t[0]], map_y[t[1]]) for t in tiles]

    return size_x, size_y, mapped

def outline_grid(size, size_x, size_y, mapped):
    grid = [[2 for _ in range(size_x)] for _ in range(size_y)]
    for i in range(size):
        j = (i+1) % size
        p1 = mapped[i]
        p2 = mapped[j]
        for x in interval_range(p1[0], p2[0]):
            for y in interval_range(p1[1], p2[1]):
                grid[y][x] = 1

    return grid

def fill(grid, sr, sc, orig, new):
    rows, cols = len(grid), len(grid[0])

    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == orig:
            grid[r][c] = new
            stack.append((r+1, c))
            stack.append((r-1, c))
            stack.append((r, c+1))
            stack.append((r, c-1))

def is_good(grid, mapped, i, j):
    p1 = mapped[i]
    p2 = mapped[j]
    for x in interval_range(p1[0], p2[0]):
        for y in interval_range(p1[1], p2[1]):
            if grid[y][x] == 0:
                return False
    return True

def part2(tiles, size):
    size_x, size_y, mapped = map_tiles(tiles)
    grid = outline_grid(size, size_x, size_y, mapped)
    fill(grid, 0, 0, 2, 0)

    areas = ((area(tiles[i], tiles[j]), i, j) for i in range(size-1) for j in range(i+1, size))

    for result, i, j in sorted(areas, reverse=True, key = lambda x: x[0]):
        if is_good(grid, mapped, i, j):
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
