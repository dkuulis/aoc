import lib

def main():
    lines = lib.read_lines()
    split = next(i for i, e in enumerate(lines) if not e)

    fresh = [tuple(map(int, line.split("-"))) for line in lines[:split]]
    ingredients = [int(line) for line in lines[split+1:]]

    result1 = sum(1 if any(1 for r in fresh if r[0] <= i and r[1] >= i) else 0 for i in ingredients)
    print(result1)

    fresh.sort(key = lambda x: x[0])
    unified = []
    start, end = 0, -1
    for lo, hi in fresh:
        if lo > end:
            unified.append((start, end))
            start = lo
            end = hi
        else:
            end = max(end, hi)
    unified.append((start, end))

    result2 = sum(hi-lo+1 for lo, hi in unified)
    print(result2)

if __name__ == "__main__":
    main()
