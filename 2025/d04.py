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

def check(map, x, y, size):
    if map[y][x] > 0:
        n = sum(map[ny][nx] for nx, ny in neighbours(x, y, size))
        if n < 4:
            yield x, y

def accessible(map):
    result = set()

    size = len(map)
    for y in range(size):
        for x in range(size):
            result.update(check(map, x, y, size))

    return result

def removable(map):

    result = 0
    size = len(map)

    remove = accessible(map)
    
    while True:
        result += len(remove)
        
        if len(remove) == 0:
            break

        next = set()
        for x, y in remove:
            map[y][x] = 0
            next.update(neighbours(x, y, size))

        remove = set()
        for x, y in next:
            remove.update(check(map, x, y, size))
    # end while

    return result

def main():
    lines = lib.read_lines()

    decode = {"@": 1, ".": 0}
    map = [[decode[c] for c in line] for line in lines]

    result1 = len(accessible(map))
    print(result1)

    result2 = removable(map)
    print(result2)

if __name__ == "__main__":
    main()
