import re
import lib

def check(s, f):
    l = len(s)

    if l % f != 0: # framents must fit exactly
        return False

    n = l // f # number of fragments

    for i in range(f): # each char in fragment
        for j in range(1, n): # each fragment but the first
            if s[i] != s[i+j*f]: # letter does't match
                return False

    return True

def multi(s):
    for f in range(1, len(s)//2+1): # fragment lengths
        if check(s, f): # check each fragment length
            return True

    return False

def main():
    pattern = r"(?P<start>\d+)-(?P<end>\d+),?"

    content = lib.read_content()
    ranges = [lib.ints(m.groupdict()) for m in re.finditer(pattern, content)]

    repeats = r"^(.+)\1$"
    result1 = sum(n for r in ranges for n in range(r["start"], r["end"]+1) if re.search(repeats, str(n)))
    print(result1)

    result2 = sum(n for r in ranges for n in range(r["start"], r["end"]+1) if multi(str(n)))
    print(result2)

if __name__ == "__main__":
    main()
