import re
import lib

rules = [
    re.compile("("+ ")|(".join(chr(97+i)+chr(98+i)+chr(99+i) for i in range(24))+ ")"),
    re.compile(r"^[^iol]{8}$"),
    re.compile(r"(.)\1.*(.)\2")
]

def inc(s):
    c = ord(s[-1])
    c += 1
    if c <= 96+26:
        c += 1 if chr(c) in "iol" else 0
        return s[:-1] + chr(c)
    else:
        return inc(s[:-1]) + "a"

def generate(content, rules):
    password = content

    m = None
    while not m:
        password = inc(password)
        m = all(r.search(password) for r in rules)

    return password

def main():
    content = lib.read_content()

    password = generate(content, rules)
    print(password)

    password = generate(password, rules)
    print(password)

if __name__ == "__main__":
    main()
