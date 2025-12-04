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

def main():
    lines = lib.read_lines()

    decode = {"@": 1, ".": 0}
    map = [[decode[c] for c in line] for line in lines]

    size = len(map)
    result1 = 0
    for y in range(size):
        for x in range(size):
            if map[y][x] > 0:
                n = sum(map[ny][nx] for nx, ny in neighbours(x, y, size))
                result1 += 1 if n < 4 else 0

    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
