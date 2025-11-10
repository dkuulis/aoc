import sys
from itertools import accumulate

def solve1(lengths):

    files = lengths[::2]
    spaces = lengths[1::2]

    fwd = 0
    bck = len(files)-1
    bcks = 0

    result = 0
    block = 0

    map = []

    while True:
        if fwd > bck:
            break

        # go forward
        while files[fwd] > 0:
            files[fwd] -= 1

            result += block*fwd
            map.append(fwd)
            block += 1

        # next file forward
        fwd += 1

        if fwd > bck:
            break

        # go backward
        while spaces[bcks] > 0:
            # check last unused file
            while files[bck] == 0:
                bck -= 1

            spaces[bcks] -= 1
            files[bck] -= 1

            result += block*bck
            map.append(bck)
            block += 1

        # next free space
        bcks += 1

    return result

def solve2(lengths):

    ends = list(accumulate(lengths))
    starts = [0] + ends[:-1]

    files = lengths[::2]
    spaces = lengths[1::2]

    file_starts = starts[::2]
    space_starts = starts[1::2]

    count = len(files)

    for i in range(count-1, 0, -1):

        size = files[i]
        position = file_starts[i]

        for j in range(len(spaces)):

            if space_starts[j] > position:
                break

            if (spaces[j] >= size):
                file_starts[i] = space_starts[j]
                spaces[j] -= size
                space_starts[j] += size
                break

    result = sum(file * (start * size + size * (size - 1) // 2 ) for file, size, start in zip(range(count), files, file_starts))
    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        content = file.read()

    lengths = [int(c) for c in content]

    #result = solve1(lengths)
    result = solve2(lengths)

    print(result)

if __name__ == "__main__":
    main()
