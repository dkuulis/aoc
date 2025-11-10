import lib

def neighbours(x, y, size):
    for dx in [-1, 0, 1]:
        nx = x + dx
        if nx >= 0 and nx < size:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                ny = y + dy
                if ny >= 0 and ny < size:
                    yield (nx, ny)

def onoff(x, y, grid, size):
    c = sum(grid[n[1]][n[0]] for n in neighbours(x, y, size))
    v = grid[y][x]
    g = 1 if (v == 1 and c == 2) or (c == 3) else 0
    return g

def onoff2(x, y, grid, size):
    s1 = size - 1

    if (x == 0 and y == 0 or
       x == s1 and y == 0 or
       x == 0 and y == s1 or
       x == s1 and y == s1):
        return 1

    return onoff(x, y, grid, size)

def count(grid):
    return sum(sum(g for g in line) for line in grid)

def run1(lines, size):
    grid = [[1 if c == "#" else 0 for c in line] for line in lines]
    for _ in range(100):
        updated = [[onoff(x, y, grid, size) for x in range(size)] for y in range(size)]
        grid = updated
    result1 = count(grid)
    return grid,result1

def run2(lines, size):
    s1 = size - 1

    grid = [[1 if c == "#" else 0 for c in line] for line in lines]

    grid[0][0] = 1
    grid[s1][0] = 1
    grid[0][s1] = 1
    grid[s1][s1] = 1

    for _ in range(100):
        updated = [[onoff2(x, y, grid, size) for x in range(size)] for y in range(size)]
        grid = updated
    result2 = count(grid)
    return result2

def main():
    lines = lib.read_lines()
    size = len(lines)

    #result1 = run1(lines, size)
    #print(result1)

    result2 = run2(lines, size)
    print(result2)





if __name__ == "__main__":
    main()
