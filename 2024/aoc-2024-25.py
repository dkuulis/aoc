import sys
import re

def trailing_hash(s):
    match = re.search(r"(#+)$", s)
    count = len(match.group(1)) if match else 0
    return count

# the keys have the top row empty and the bottom row filled
def decode_key(buffer):
    transposed = [''.join(chars) for chars in zip(*buffer[1:-1])]
    return [trailing_hash(t) for t in transposed]

def leading_hash(s):
    match = re.search(r"^(#+)", s)
    count = len(match.group(1)) if match else 0
    return count

# The locks are schematics that have the top row filled (#) and the bottom row empty (.)
def decode_lock(buffer):
    transposed = [''.join(chars) for chars in zip(*buffer[1:-1])]
    return [leading_hash(t) for t in transposed]

def parse(lines):

    lines = [line.strip() for line in lines]
    lines.append('')

    keys = []
    locks = []

    buffer = []
    for line in lines:
        if line:
            buffer.append(line)
        else:
            if buffer[0][0] == ".":
                keys.append(decode_key(buffer))
            else:
                locks.append(decode_lock(buffer))
            buffer = []

    return keys, locks

def match(lock, key):
    for l, k in zip(lock, key):
        if l+k > 5:
            return False
    return True

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    keys, locks = parse(lines)

    result1 = 0
    for l in locks:
        for k in keys:
            result1 += 1 if match(l,k) else 0
    print(result1)


if __name__ == "__main__":
    main()
