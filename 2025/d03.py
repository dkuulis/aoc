import re
import lib

def joltage(bank, digits):
    size = len(bank)

    result = 0
    index = 0
    indexed = list(enumerate(bank))

    for stop in range(size - digits, size):
        index, value = max(indexed[index:stop+1], key=lambda x: x[1])
        index += 1
        result = result * 10 + value # acumulate

    return result

def main():
    lines = lib.read_lines()
    banks = [[int(c) for c in line] for line in lines]

    result1 = sum(joltage(bank, 2) for bank in banks)
    print(result1)

    result2 = sum(joltage(bank, 12) for bank in banks)
    print(result2)

if __name__ == "__main__":
    main()
