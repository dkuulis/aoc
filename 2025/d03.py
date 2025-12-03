import re
import lib

def joltage(bank, n):
    l = len(bank)

    result = 0
    index = 0

    for r in range(n): # r-th digit
        stop = l - n + r + 1 # last+1 available char 
        position, value = max(enumerate(bank[index:stop]), key=lambda x: x[1])
        index += position + 1
        result = result * 10 + value

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
