import sys
import re
from collections import Counter
from enum import Enum
from itertools import pairwise
from collections import defaultdict

def topological_sort(pages, rules):
    visited = set()
    stack = []
    all = set(pages)

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in rules.get(node, set()) & all:
            dfs(neighbor)
        stack.append(node)

    for node in pages:
        dfs(node)

    return stack[::-1]  # reverse the stack to get topological order

def extract_input(lines):
    lines = [l.strip() for l in lines]
    split = next(i for i, e in enumerate(lines) if not e)
    updates = [list(map(int, line.split(","))) for line in lines[split+1:]]

    raw_rules = [tuple(map(int, line.split("|"))) for line in lines[:split]]

    rules = {}
    for prv, nxt in raw_rules:
        s = rules.get(prv, set())
        s.add(nxt)
        rules[prv] = s

    return rules, updates

def is_ok(pages, rules):

    for i in range(1, len(pages)):

        page = pages[i]
        follows = rules.get(page, set())

        preceding = set(pages[0:i])

        violations = preceding & follows

        if violations:
            return False
        
    return True

def execute1(rules, updates):
    result = 0

    for pages in updates:
        if is_ok(pages, rules):
            mid = len(pages) // 2
            result += pages[mid]

    return result

def execute2(rules, updates):
    result = 0

    for pages in updates:
        if not is_ok(pages, rules):
            sorted_pages = topological_sort(pages, rules)
            mid = len(sorted_pages) // 2
            result += sorted_pages[mid]

    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    rules, updates = extract_input(lines)

    result = execute2(rules, updates)

    print(result)

if __name__ == "__main__":
    main()
