from itertools import accumulate
import lib

directions = {"^": (0,-1), ">": (1,0), "v": (0,1), "<": (-1,0)}

def move(p, d):
    return (p[0]+d[0], p[1]+d[1])

def main():
    content = lib.read_content()

    moves = [directions[c] for c in content]
    positions = set(accumulate([(0,0)] + moves, move))
    result1 = len(positions)
    print(result1)

    moves1 = moves[0::2]
    moves2 = moves[1::2]
    positions1 = set(accumulate([(0,0)] + moves1, move))
    positions2 = set(accumulate([(0,0)] + moves2, move))
    result2 = len(positions1 | positions2)
    print(result2)


if __name__ == "__main__":
    main()
