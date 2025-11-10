import sys

def parse(lines):
    size = len(lines) + 2
    chart = [([10]+ list(map(int, s.strip())) + [10]) for s in lines]
    extra = [10] * size
    return [extra] + chart + [extra]

def solve1(chart):

    size = len(chart)
    field = [[None for _ in range(size)] for _ in range(size)]

    i = 1
    for y, row in enumerate(chart):
        for x, height in enumerate(row):
            if height == 9:
                field[y][x] = set([i])
                i += 1

    for h in range(9, 0, -1):
        h1 = h - 1
        for y in range (1, size-1):
            for x in range (1, size-1):
                if chart[y][x] == h1:
                    s = set()
                    if  chart[y][x+1] == h:
                        s = s | field[y][x+1]
                    if  chart[y+1][x] == h:
                        s = s | field[y+1][x]
                    if  chart[y][x-1] == h:
                        s = s | field[y][x-1]
                    if  chart[y-1][x] == h:
                        s = s | field[y-1][x]
                    field[y][x] = s

    result = 0
    for y in range (1, size-1):
        for x in range (1, size-1):
            if chart[y][x] == 0:
                result += len(field[y][x])

    return result

def solve2(chart):

    size = len(chart)
    field = [[0 for _ in range(size)] for _ in range(size)]

    for y, row in enumerate(chart):
        for x, height in enumerate(row):
            if height == 9:
                field[y][x] = 1

    for h in range(9, 0, -1):
        h1 = h - 1
        for y in range (1, size-1):
            for x in range (1, size-1):
                if chart[y][x] == h1:
                    t = 0
                    if  chart[y][x+1] == h:
                        t += field[y][x+1]
                    if  chart[y+1][x] == h:
                        t += field[y+1][x]
                    if  chart[y][x-1] == h:
                        t += field[y][x-1]
                    if  chart[y-1][x] == h:
                        t += field[y-1][x]
                    field[y][x] = t

    result = 0
    for y in range (1, size-1):
        for x in range (1, size-1):
            if chart[y][x] == 0:
                result += field[y][x]

    return result

def main():
    filename = sys.argv[0] + ".initial.txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    chart = parse(lines)
    result1 = solve1(chart)
    result2 = solve2(chart)
    
    print(result1, result2)

if __name__ == "__main__":
    main()
