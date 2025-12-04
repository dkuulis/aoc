import lib

decode = {"@": 1, ".": 0}

def main():
    lines = lib.read_lines()
    plan = [[decode[c] for c in line] for line in lines]

    result1 = 0
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
