from itertools import count
import lib

def sum_factors(n):
    result = 0
    for x in range(1, int(n**0.5) + 1):
        if n % x == 0:
            r = n // x
            result += x
            result += r if r != x else 0
    return result

def sum_factors_w_limit(n, l):
    result = 0
    for x in range(1, int(n**0.5) + 1):
        if n % x == 0:
            r = n // x
            result += x if r <= l else 0
            result += r if x <= l and r != x else 0
    return result

def walk1(target):
    for house in count(1):
        presents = sum_factors(house) * 10
        if presents >= target:
            return house

def walk2(target):
    for house in count(1):
        presents = sum_factors_w_limit(house, 50) * 11
        if presents >= target:
            return house

def main():
    content = lib.read_content()
    target = int(content)

    result1 = walk1(target)
    print(result1)

    result2 = walk2(target)
    print(result2)

if __name__ == "__main__":
    main()
