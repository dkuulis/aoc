import lib

def main():
    lines = lib.read_lines()
    split = next(i for i, e in enumerate(lines) if not e)

    fresh = [tuple(map(int, line.split("-"))) for line in lines[:split]]
    ingredients = [int(line) for line in lines[split+1:]]

    result1 = 0
    for ingredient in ingredients:
        result1 += 1 if  any(1 for r in fresh if r[0] <= ingredient and r[1] >= ingredient) else 0
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
