import re
import lib

def main():
    lines = lib.read_lines()

    decode = {".": 0, "^": 1}
    beams = {i for i, c in enumerate(lines[0]) if c == "S"}
    counts = {i:1 for i in beams}
    splitters = [[decode[c] for c in line] for line in lines[1:]]

    result1 = 0
    for row in splitters:
        next = set()
        for i in beams:
            if row[i] == 1:
                next.add(i-1)
                next.add(i+1)
                result1 += 1
            else:
                next.add(i)
        beams = next
    print(result1)

    for row in splitters:
        next = {}
        for i, c in counts.items():
            if row[i] == 1:
                next[i-1] = next.get(i-1, 0) + c
                next[i+1] = next.get(i+1, 0) + c
            else:
                next[i] = next.get(i, 0) + c
        counts = next
    result2 = sum(c for c in counts.values())
    print(result2)

if __name__ == "__main__":
    main()
