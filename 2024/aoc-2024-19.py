import sys
import re

def parse(lines):
   towels = [t.strip() for t in lines[0].split(',')]
   patterns = [p.strip() for p in lines[2:]]
   return towels, patterns

def solve1(towels, patterns):
    result = 0
    r = "^((" + ")|(".join(towels) + "))+$"
    regex = re.compile(r)

    for p in patterns:
        if regex.match(p):
            result += 1

    return result

def solve2step(towels, pattern):
    result = 0

    for towel in towels:
        if pattern == towel:
            result += 1
        elif pattern.startswith(towel):
            result += solve2step(towels, pattern[len(towel):])

    return result

def solve2(towels, patterns):
    result = 0
    for p in patterns:
        result += solve2step(towels, p)
    return result

def solve3step(towels, pattern):
    pattern = '^' + pattern
    data = [1 if c == '^' else 0 for c in pattern]

    for i in range(len(pattern)):
        d = data[i]
        if d > 0:
            s = pattern[i+1:]
            for towel in towels:
                if s.startswith(towel):
                    j = i + len(towel)
                    data[j] += d

    return data[-1]

def solve3(towels, patterns):
    result = sum(solve3step(towels, p) for p in patterns)
    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    towels, patterns = parse(lines)

    result1 = solve1(towels, patterns)
    print(result1)

    #result2 = solve2(towels, patterns)
    #print(result2)

    result3 = solve3(towels, patterns)
    print(result3)

if __name__ == "__main__":
    main()
