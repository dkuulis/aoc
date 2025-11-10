import sys
import re
from collections import Counter
from enum import Enum
from itertools import pairwise

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        content = file.read()

    result = 0
    en = True

    matches = re.finditer(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))", content)

    for match in matches:
        t = match.group(1)

        if t.startswith("mul") and en:
            a = int(match.group(2))
            b = int(match.group(3))
            result += a*b

        if t == "do()":
            en = True

        if t == "don't()":
            en = False

    print(result)

if __name__ == "__main__":
    main()
