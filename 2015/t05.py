import re
import lib

def nice(line):

    if not re.search(r"([aeiou].*){3}", line):
        return False

    if not re.search(r"(.)\1", line):
        return False

    if re.search(r"(ab|cd|pq|xy)", line):
        return False
    
    return True

def nice2(line):

    if not re.search(r"(..).*\1", line):
        return False

    if not re.search(r"(.).\1", line):
        return False

    return True

def main():
    lines = lib.read_lines()

    result1 = sum(1 if nice(line) else 0 for line in lines)
    print(result1)

    result2 = sum(1 if nice2(line) else 0 for line in lines)
    print(result2)


if __name__ == "__main__":
    main()
