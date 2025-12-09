import lib

def area(p, q):
    return (p[0]-q[0]+1) * (p[1]-q[1]+1)


def main():
    lines = lib.read_lines()
    tiles = [tuple(map(int, line.split(","))) for line in lines]
    size = len(tiles)

    result1 = max(area(tiles[i], tiles[j]) for i in range(size-1) for j in range(i+1, size))
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
