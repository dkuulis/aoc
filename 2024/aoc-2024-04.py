import sys
import re
from collections import Counter
from enum import Enum
from itertools import pairwise

def extend3(lines):

    l = len(lines)

    e1 = '.'*l
    e2 = [e1, e1, e1]
    e3 = e2 + lines + e2
    e4 = ["..." + s + "..." for s in e3]

    return e4

def extend2(lines):

    l = len(lines)

    e1 = '.'*l
    e2 = [e1, e1]
    e3 = e2 + lines + e2
    e4 = [".." + s + ".." for s in e3]

    return e4

def find_xmas(t):

    result = 0

    size = len(t) - 3
    for i in range(size):
        for j in range(size):

            s1 = t[i][j] + t[i][j+1] + t[i][j+2] + t[i][j+3]
            s2 = t[i][j] + t[i+1][j+1] + t[i+2][j+2] + t[i+3][j+3]
            s3 = t[i][j] + t[i+1][j] + t[i+2][j] + t[i+3][j]
            s4 = t[i+3][j] + t[i+2][j+1] + t[i+1][j+2] + t[i][j+3]

            result += 1 if s1 =="XMAS" or s1 == "SAMX" else 0
            result += 1 if s2 =="XMAS" or s2 == "SAMX" else 0
            result += 1 if s3 =="XMAS" or s3 == "SAMX" else 0
            result += 1 if s4 =="XMAS" or s4 == "SAMX" else 0
 
    return result
 
def find_x_mas(t):

    result = 0

    size = len(t) - 2
    for i in range(size):
        for j in range(size):

            s1 = t[i][j] + t[i+1][j+1] + t[i+2][j+2]
            s2 = t[i+2][j] + t[i+1][j+1] + t[i][j+2] 

            if (s1 =="MAS" or s1 == "SAM") and (s2 =="MAS" or s2 == "SAM"):
                result += 1
 
    return result
 
def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    #full = extend3(lines)
    #result = find_xmas(full)

    full = extend2(lines)
    result = find_x_mas(full)

    print(result)

if __name__ == "__main__":
    main()
