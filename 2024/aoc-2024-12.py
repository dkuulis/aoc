import sys

def parse(lines):
    size = len(lines) + 2
    chart = [(['.']+ list(s.strip()) + ['.']) for s in lines]
    extra = ['.'] * size
    return [extra] + chart + [extra]

def count_fences(chart):
    size = len(chart)
    fences = [[[0 for _ in range(4)] for _ in range(size)] for _ in range(size)]
    for y in range (1, size-1):
        for x in range (1, size-1):
            r = chart[y][x]
            for i, dy, dx in [(0, -1,0), (1, 1,0), (2, 0,-1), (3, 0,1)]:
                fences[y][x][i] = 0 if chart[y+dy][x+dx] == r else 1
        
    return fences

def straight_fences(chart, fences):
    
    size = len(chart)
    straight = [[[0 for _ in range(4)] for _ in range(size)] for _ in range(size)]

    for y in range (1, size-1):
        for x in range (1, size-1):
            r = chart[y][x]
            for i, dy, dx in [(0, 0,-1), (1, 0,-1), (2, -1,0), (3, -1,0)]:
                straight[y][x][i] = fences[y][x][i]
                if chart[y+dy][x+dx] == r:
                    if fences[y+dy][x+dx][i] > 0:
                        straight[y][x][i] = 0

    return straight

def summarize(fences, regions):
    result = 0
    for r in regions:
        size = len(r)
        count = sum(sum(fences[y][x][i] for i in range(4)) for y, x in r)
        result += count * size
    return result

def find_same_value_regions(matrix):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    regions = []

    def dfs(r, c, value, region):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r][c] or matrix[r][c] != value):
            return
        visited[r][c] = True
        region.append((r, c))
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            dfs(r + dr, c + dc, value, region)

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region = []
                dfs(r, c, matrix[r][c], region)
                regions.append(region)

    return regions

def debug(chart, fences):

    size = len(chart)

    for y in range (1, size-1):
        l1 = ""
        l2 = ""
        l3 = ""

        for x in range (1, size-1):
            l1 += "." + ("-" if fences[y][x][0] > 0 else " ") + "."
            l2 += ("|" if fences[y][x][2] > 0 else " ") + chart[y][x] + ("|" if fences[y][x][3] > 0 else " ")
            l3 += "." + ("-" if fences[y][x][1] > 0 else " ") + "."

        print(l1)
        print(l2)
        print(l3)

def solve1(chart):

    fences = count_fences(chart)
    regions = find_same_value_regions(chart)
    result = summarize(fences, regions)

    return result

def solve2(chart):

    fences = count_fences(chart)
    #debug(chart, fences)
    straight = straight_fences(chart, fences)
    #debug(chart, straight)
    regions = find_same_value_regions(chart)
    result = summarize(straight, regions)

    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    chart = parse(lines)
    result1 = solve1(chart)
    result2 = solve2(chart)
    
    print(result1, result2)

if __name__ == "__main__":
    main()
