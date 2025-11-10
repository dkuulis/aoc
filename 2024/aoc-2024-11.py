import sys

def solve1(stones):

    for runs in range(25):

        i = 0
        c = len(stones)

        while i < c:

            v = stones[i]
            s = str(v)
            l = len(s)
            if v == 0:
                stones[i] = 1
            elif l % 2 == 0:
                l2 = l // 2
                stones[i] = int(s[l2:])
                stones.insert(i, int(s[:l2]))
                i += 1
                c += 1
            else:
                stones[i] = v * 2024

            i += 1

    return len(stones)

def solve2(stones2):

    stones = {s : 1 for s in stones2 }

    for runs in range(75):

        n = {1: 0}

        for value, count in stones.items():
            s = str(value)
            l = len(s)

            if value == 0:
                n[1] += count
            elif l % 2 == 0:
                l2 = l // 2
                v1 = int(s[l2:])
                v2 = int(s[:l2])

                c1 = n.get(v1, 0) + count
                n[v1] = c1
                
                c2 = n.get(v2, 0) + count
                n[v2] = c2
            else:
                v = value * 2024
                c = n.get(v, 0) + count
                n[v] = c

        stones = n

    return sum(c for c in stones.values())

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        content = file.read()

    stones = [int(c) for c in content.split()]

    #result1 = solve1(stones)
    result2 = solve2(stones)

    print(result2)

if __name__ == "__main__":
    main()
