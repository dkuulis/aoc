import re
import lib

def check(s, size):
    length = len(s)

    if length % size != 0: # framents must fit exactly
        return False

    for j in range(1, length // size): # each fragment but the first
        if s[:size] != s[j*size:(j+1)*size]: # fragment does't match
            return False

    return True

def multi(id):
    for size in range(1, len(id)//2+1): # check each valid fragment size
        if check(id, size):
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
