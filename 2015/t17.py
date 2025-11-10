import lib

def fill(containers, capacity):

    if capacity <= 0:
        return

    first = containers[0]
    if first == capacity:
        yield [first]

    if len(containers) == 1:
        return

    rest = containers[1:]
    for f in fill(rest, capacity - first):
        yield [first] + f

    yield from fill(rest, capacity)

def main():
    lines = lib.read_lines()
    containers = [int(line) for line in lines]

    fills = list(fill(containers, 150))
    result1 = len(fills)
    print(result1)

    m = min(len(f) for f in fills)
    result2 = sum(1 for f in fills if len(f) == m)
    print(result2)

if __name__ == "__main__":
    main()
