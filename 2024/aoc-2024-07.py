import sys
import re
from collections import Counter
from enum import Enum
from itertools import pairwise
from collections import defaultdict

def parse(line):
    
    start, rest = line.split(':', 1)

    test = int(start)
    numbers = [(int(chunk)) for chunk in rest.strip().split(' ')]
    
    return (test, numbers)

def is_possible(test, numbers):

    tail = numbers[-1]

    if len(numbers) == 1:
        return test == tail
    
    rest = numbers[:-1]

    if (test % tail == 0):
        if (is_possible(test // tail, rest)):
            return True

    if (test - tail > 0):
        if (is_possible(test - tail, rest)):
            return True

    # extra
    test_str = str(test)
    tail_str = str(tail)
    if (test_str.endswith(tail_str)):
        test2 = int(test_str[:-len(tail_str)])
        if (is_possible(test2, rest)):
            return True

    return False

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    data = [parse(line) for line in lines]
    result = sum(test for test, numbers in data if is_possible(test, numbers))

    print(result)

if __name__ == "__main__":
    main()
