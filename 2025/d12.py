import re
import lib

def parse(lines):
    size = len(lines)
    pattern = r"((?P<index>\d+):)|((?P<x>\d+)x(?P<y>\d+):(?P<shapes>[\d ]+))"
    decode = {"#":1, ".":0}

    tiles = []
    grids = []

    i = 0
    while i < size:
        m = re.match(pattern, lines[i])

        # tile definition
        if m["index"]:
            shape = []
            i += 1
            while i < size and lines[i]:
                shape.append(lines[i])
                i += 1
            tiles.append([[decode[c] for c in l] for l in shape])

        # grid specifications
        if m["shapes"]:
            x = int(m["x"])
            y = int(m["y"])
            indexes = list(map(int, m["shapes"].split()))
            grids.append(((x,y),indexes))

        # advance
        i += 1

    return tiles, grids

def main():
    lines = lib.read_lines()
    tiles, grids = parse(lines)

    size = [sum(sum(inner) for inner in outer) for outer in tiles]
    result1 = sum(1 for g in grids if g[0][0]*g[0][1] > sum(size[i]*u for i, u in enumerate(g[1])))
    print(result1)

if __name__ == "__main__":
    main()
