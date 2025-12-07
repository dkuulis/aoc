import lib
import math

def execute(operations, numbers):
    decode = {"+": sum, "*": math.prod}
    return sum(decode[o](data) for o, data in zip(operations, numbers))

def part1(lines):
    chunks = [line.strip().split() for line in lines]
    transposed = [[int(n) for n in line] for line in chunks[:-1]]

    operations = chunks[-1]

    size = len(operations)
    numbers = [[row[i] for row in transposed] for i in range(size)]

    return execute(operations, numbers)

def split_by_empty(arr):
    result = []
    current = []
    for item in arr:
        if not item:  # treat empty string or None as separator
            result.append(current)
            current = []
        else:
            current.append(item)
    result.append(current)
    return result

def part2(lines):
    operations = lines[-1].strip().split()
    data = lines[:-1]

    size = len(lines[0])
    digits = [[row[i] for row in data] for i in range(size)]
    strings = ["".join(r).strip() for r in digits]
    splits = split_by_empty(strings)
    numbers = [[int(n) for n in data] for data in splits]

    return execute(operations, numbers)


def main():
    lines = lib.read_lines()

    result1 = part1(lines)
    print(result1)

    result2 = part2(lines)
    print(result2)

if __name__ == "__main__":
    main()
