import re
import lib

pattern = r"row (?P<r>\d+).*column (?P<c>\d+)"

def main():
    content = lib.read_content()
    data  = lib.ints(re.search(pattern, content, re.DOTALL).groupdict())
    r = data["r"]
    c = data["c"]
    n = r + c - 1
    i = n * (n - 1) // 2 + c
    
    x = 20151125
    for k in range(1, i):
        x = x * 252533 % 33554393

    result1 = x
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
