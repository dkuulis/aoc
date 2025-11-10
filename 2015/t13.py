import re
import itertools
import lib

def circular_permutations(lst):
    first = lst[0]
    rest = lst[1:]

    for p in itertools.permutations(rest):
        yield [first] + list(p)

def circular_neighbors(lst):
    length = len(lst)
    for i in range(length):
        yield (lst[i], lst[(i + 1) % length])

def happiness(seating, pairs):
    return sum(pairs[(p1, p2)] + pairs[(p2, p1)] for p1, p2 in circular_neighbors(seating))

def max_happiness(persons, pairs):
    return max(happiness(seating, pairs) for seating in circular_permutations(persons))

pattern  = r"(?P<p>\w+) would (?P<sign>(lose)|(gain)) (?P<amount>\d+) happiness units by sitting next to (?P<t>\w+)\."
signs = {"gain": +1, "lose": -1}

def main():
    lines = lib.read_lines()
    data = [re.match(pattern, line).groupdict() for line in lines]

    persons = list({d["p"] for d in data})
    pairs = {(d["p"], d["t"]): signs[d["sign"]]*int(d["amount"]) for d in data}

    result1 = max_happiness(persons, pairs)
    print(result1)

    persons2 = persons + ["Me"]
    pairs2 = pairs | {("Me", p): 0 for p in persons} | {(p, "Me"): 0 for p in persons}

    result2 = max_happiness(persons2, pairs2)
    print(result2)

if __name__ == "__main__":
    main()
