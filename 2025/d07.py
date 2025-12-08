import lib

def part1(beams, splitters):
    result = 0
    for row in splitters:
        next = set()
        for i in beams:
            if row[i] == 1:
                next.add(i-1)
                next.add(i+1)
                result += 1
            else:
                next.add(i)
        beams = next
    return result

def part2(counts, splitters):
    for row in splitters:
        next = {}
        for i, c in counts.items():
            if row[i] == 1:
                next[i-1] = next.get(i-1, 0) + c
                next[i+1] = next.get(i+1, 0) + c
            else:
                next[i] = next.get(i, 0) + c
        counts = next

    return sum(c for c in counts.values())

def main():
    lines = lib.read_lines()

    decode = {".": 0, "^": 1}
    beams = {i for i, c in enumerate(lines[0]) if c == "S"}
    counts = {i:1 for i in beams}
    splitters = [[decode[c] for c in line] for line in lines[1:]]

    result1 = part1(beams, splitters)
    print(result1)

    result2 =  part2(counts, splitters)
    print(result2)

if __name__ == "__main__":
    main()
