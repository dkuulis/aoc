import sys
from collections import Counter

def read_file_lines():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines
    
def process1(lft, rgh):

    lft.sort()
    rgh.sort()

    i = 0
    for a, b in zip(lft, rgh):
        i = i + abs(a - b)

    print(i)

def process2(lft, rgh):

    counts = Counter(rgh)

    i = 0
    for x in lft:
        i = i + x * counts.get(x, 0)

    print(i)

def main():
    lines = read_file_lines()

    lft = []
    rgh = []

    for line in lines:
        a, b = map(int, line.split())
        lft.append(a)
        rgh.append(b)

    process2(lft, rgh)

if __name__ == "__main__":
    main()
