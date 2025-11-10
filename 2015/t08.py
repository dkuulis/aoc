import re
import lib

pattern1 = r'(\\\\)|(\\\")|(\\x[0-9a-f]{2})'
pattern2 = r'(\\)|(\")'

def decode_diff(line):
    return sum(m.end() - m.start() - 1 for m in re.finditer(pattern1, line[1:-1])) + 2

def encode_diff(line):
    return sum(1 for m in re.finditer(pattern2, line)) + 2

def main():
    lines = lib.read_lines()

    result1 = sum(decode_diff(line) for line in lines)
    print(result1)

    result2 = sum(encode_diff(line) for line in lines)
    print(result2)

if __name__ == "__main__":
    main()
