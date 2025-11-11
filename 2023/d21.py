from typing import Generator
import lib

def neighbours(t: tuple[int, int], size: int) -> Generator[tuple[int, int], None, None]:
    x, y = t
    s1 = size - 1
    if x > 0:
        yield (x-1, y)
    if y > 0:
        yield (x, y-1)
    if x < s1:
        yield (x+1, y)
    if y < s1:
        yield (x, y+1)

def move(maze: list[list[int]], tiles: set[tuple[int, int]], previous:set[tuple[int, int]]) -> set[tuple[int, int]]:
    size = len(maze)
    future = set()
    for t in tiles:
        for n in neighbours(t, size):
            if maze[n[1]][n[0]] == 0 and n not in previous:
                future.add(n)
    return future

def main():
    lines = lib.read_lines()
    maze = [[1 if c == "#" else 0 for c in line] for line in lines]
    tiles = {(x,y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "S"}
    steps = 64

    older = set()
    previous = set()
    for _ in range(steps):
        forward = move(maze, tiles, previous)
        tiles, previous, older = forward, tiles | older, previous

    result1 = len(tiles | older)
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
