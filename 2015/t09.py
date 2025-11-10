import re
import itertools
import lib

pattern  = r"(?P<p1>\w+) to (?P<p2>\w+) = (?P<d>\d+)"

def distance(path, links):
    steps = [path[i:i+2] for i in range(len(path) - 1)]
    return sum(links[(s1, s2)] for s1, s2 in steps)

def find_min(locations, links):
    paths = itertools.permutations(locations)
    return min(distance(path, links) for path in paths)

def find_max(locations, links):
    paths = itertools.permutations(locations)
    return max(distance(path, links) for path in paths)

def main():
    lines = lib.read_lines()
    pairs = [re.match(pattern, line).groupdict() for line in lines]
    routes = [(p["p1"], p["p2"], int(p["d"])) for p in pairs] + [(p["p2"], p["p1"], int(p["d"])) for p in pairs]

    locations = {r[0] for r in routes}
    links = {(r[0], r[1]): r[2] for r in routes}

    result1 = find_min(locations, links)
    print(result1)

    result2 = find_max(locations, links)
    print(result2)

if __name__ == "__main__":
    main()
