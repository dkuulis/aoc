from typing import Generator
import lib

maze: list[list[int]] = [[0]]
size: int = 0
size1: int = 0

def fixed_neighbours(t: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    x, y = t
    if x > 0:
        yield (x-1, y)
    if y > 0:
        yield (x, y-1)
    if x < size1:
        yield (x+1, y)
    if y < size1:
        yield (x, y+1)

def fixed_test(n: tuple[int, int]) -> bool:
    return maze[n[1]][n[0]] == 0

def infinite_neighbours(t: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    x, y = t
    yield (x-1, y)
    yield (x, y-1)
    yield (x+1, y)
    yield (x, y+1)

def infinite_test(n: tuple[int, int]) -> bool:
    x, y = n
    x %= size
    y %= size
    return maze[y][x] == 0

def move(tiles: set[tuple[int, int]], previous:set[tuple[int, int]], neighbours, test) -> set[tuple[int, int]]:
    future = set()
    for t in tiles:
        for n in neighbours(t):
            if test(n) and n not in previous:
                future.add(n)
    return future

def run(tiles: set[tuple[int, int]], steps: int, neighbours, test) -> int:
    older = set()
    previous = set()
    for _ in range(steps):
        forward = move(tiles, previous, neighbours, test)
        tiles, previous, older = forward, tiles | older, previous

    return tiles | older

def filter_box(tiles: set[tuple[int, int]], p1: tuple[int, int], p2:tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    filter = ((x,y) for x, y in tiles if x >= p1[0] and y >= p1[1] and x < p2[0] and y < p2[1])
    return filter

def count_box(tiles: set[tuple[int, int]], i:int, j:int) -> int:
    x = i*size
    y = j*size
    count = sum(1 for _ in filter_box(tiles, (x,y), (x+size, y+size)))
    return count
        
def main():
    global maze
    global size
    global size1

    lines = lib.read_lines()

    tiles = {(x,y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "S"}
    maze = [[1 if c == "#" else 0 for c in line] for line in lines]
    size = len(maze)
    size1 = size - 1

    places = run(tiles, 64, fixed_neighbours, fixed_test)
    result1 = len(places)
    print(result1)

    steps2 = 26501365
    size2 = size * 2
    n = steps2 // size2
    r = steps2 % size2

    bigger = run(tiles, size2 + r, infinite_neighbours, infinite_test)
    c = [[count_box(bigger, i, j) for i in range(-2, 3) ]for j in range(-2, 3)]
 
    # c:
    # +-----+-----+-----+-----+-----+
    # |  0  |  t4 |  n  |  t1 |  0  |
    # +-----+-----+-----+-----+-----+
    # |  t4 |  b4 |  fb |  b1 |  t1 |
    # +-----+-----+-----+-----+-----+
    # |  w  |  fb |  fa |  fb |  e  |
    # +-----+-----+-----+-----+-----+
    # |  t3 |  b3 |  fb |  b2 |  t2 |
    # +-----+-----+-----+-----+-----+
    # |  0  |  t3 |  s  |  t2 |  0  |
    # +-----+-----+-----+-----+-----+
    #
    # n/e/s/w - noth/south/east/west - just 1
    # t1/t2/t3/t4 - tiny - 2*n  for each
    # b1/b2/b3/b4 - big - 2*n-1 for each
    # fa - full a - (2n-1)^2 
    # fb - full b - 2n^2

    result2 = 0
    result2 += c[0][2] + c[2][4] + c[4][2] + c[2][0] # n e s w
    result2 += 2 * n * (c[0][1] +  c[0][3] + c[4][1] + c[4][3]) # t1234
    result2 += (2 * n - 1 ) * (c[1][1] +  c[1][3] + c[3][1] + c[3][3]) # b1234
    result2 += (2 * n - 1 ) ** 2 * c[2][2] # fa
    result2 += (2 * n) ** 2 * c[2][1] # fb

    print(result2)

if __name__ == "__main__":
    main()
