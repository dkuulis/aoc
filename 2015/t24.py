from math import prod
from itertools import combinations
import lib

def min_length(packages, target):
    weight = 0
    for i, value in enumerate(packages):
        weight += value
        if weight >= target:
            return i + 1

def divide(rest: set, target: int, groups: int):
    packages = list(rest)
    packages.sort(reverse=True)
    minimal = min_length(packages, target)
    length = (len(packages) + 1) // 2
    for r in range(minimal, length + 1):
        for c in combinations(packages, r):
            if sum(c) == target:
                if groups == 2:
                    return True
                else:
                    others = rest - set(c)
                    if divide(others, target, groups-1):
                        return True
            
    return False

def partition(packages: list, target: int, size:int, groups:int):
    temp = set(packages)
    g1 = groups-1
    result = []
    for candidate in combinations(packages, size):
        weight = sum(candidate)
        if weight == target:
            rest = temp - set(candidate)
            if divide(rest, target, g1):
                result.append(candidate)
    return result

def group(packages: list, target: int, groups: int):
    minimal = min_length(packages, target)
    for size in range(minimal, len(packages)-1):
        result = partition(packages, target, size, groups)
        if result:
            best = min(result, key=prod)
            return best    

def main():
    lines = lib.read_lines()
    packages = [int(line) for line in lines]
    packages.sort(reverse=True)
    total = sum(packages)
    target3 = total // 3
    target4 = total // 4

    result1 = group(packages, target3, 3)
    print(prod(result1))

    result2 = group(packages, target4, 4)
    print(prod(result2))

if __name__ == "__main__":
    main()
