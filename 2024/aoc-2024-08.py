import sys
from itertools import permutations

def parse(lines):

    antennas = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char != '.':
                l = antennas.get(char, list())
                l.append((x,y))
                antennas[char] = l

    return antennas

def antinodes(size, antennas):

    result = 0
    field = [[0 for _ in range(size)] for _ in range(size)]

    for points in antennas.values():
        for a, b in permutations(points, 2):

            dx = a[0] - b[0]
            dy = a[1] - b[1]

            x = a[0]
            y = a[1]

            while True:

                if x < 0 or x >= size or y < 0 or y >= size:
                    break

                if field[y][x] == 0:
                    result += 1

                field[y][x] += 1

                x += dx 
                y += dy

    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    size = len(lines)
    antennas = parse(lines)
    result = antinodes(size, antennas)
    
    print(result)

if __name__ == "__main__":
    main()
