from itertools import accumulate
import lib

buttons = {"(": 1, ")": -1}

def main():
    content = lib.read_content()

    actions = [buttons[c] for c in content]
    floors = list(accumulate(actions))
    result1 = floors[-1]
    print(result1)

    result2 = next((i for i, floor in enumerate(floors) if floor < 0), -1) + 1
    print(result2)

if __name__ == "__main__":
    main()
