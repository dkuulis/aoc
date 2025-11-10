import sys
import re

def parse(lines):
    codes = [int(line.strip()) for line in lines]
    return codes

def gen(code):
    s1 = code << 6 # mul 64
    s2 = code ^ s1 # mix
    s3 =  s2 & 0xFFFFFF # priune

    s4 = s3 >> 5 # div 32
    s5 = s3 ^ s4 # mix
    s6 =  s5 & 0xFFFFFF # prune

    s7 = s6 << 11 # mul 2024
    s8 = s6 ^ s7 # mix
    s9 =  s8 & 0xFFFFFF # prune

    #print(s9)
    return s9

def gen2000(code):
    for _ in range(2000):
        code = gen(code)

    return code

def prices(code, limit):

    #print()
    #print(code)

    p0 = code % 10

    code = gen(code)
    p1 = code % 10
    d1 = p1 - p0

    code = gen(code)
    p2 = code % 10
    d2 = p2 - p1

    code = gen(code)
    p3 = code % 10
    d3 = p3 - p2

    result = {}
    prev = p3

    for _ in range(4, limit):
        code = gen(code)
        price = code % 10

        d4 = price - prev
        pattern = (d1, d2, d3, d4)
        if pattern not in result:
            result[pattern] = price

        prev = price
        d1, d2, d3 = d2, d3, d4

    return result

def max_banana(codes):

    result = {}
    for code in codes:
        p = prices(code, 2000)

        for k, x in p.items():
            result[k] = x + result.get(k, 0)

    max_key = max(result, key = result.get)
    return result[max_key]

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    codes = parse(lines)

    #result1 = sum(gen2000(code) for code in codes)
    #print(result1)

    result2 = max_banana(codes)
    print(result2)


if  __name__ == "__main__":
    main()