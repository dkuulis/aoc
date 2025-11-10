import sys
import re

def parse(lines):
    return [(line[0:2], line[3:5]) for line in lines]

def triplets_t(edges, graph):

    triples = set()
    for u, v in edges:
        common = graph[u] & graph[v]
        for t in common:
            l = tuple(sorted([u, v, t]))
            triples.add(l)

    result = sum(1 for u, v, t in triples if u.startswith('t') or v.startswith('t') or t.startswith('t'))
    return result

def bk(r, p, x, graph):
    if not p and not x:
        yield r

    while p:
        v = p.pop()
        n = graph[v]

        yield from bk(r | {v}, p & n, x & n, graph)

        x.add(v)

def max_cluster(graph):

    size = 0
    result = set()

    for c in bk(set(), set(graph.keys()), set(), graph):
        l = len(c)
        if l > size:
            size = l
            result = c

    return result

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    edges = parse(lines)

    graph = {}
    for u, v in edges:
        graph.setdefault(u, set()).add(v)
        graph.setdefault(v, set()).add(u)

    #result1 = triplets_t(edges, graph)
    #print(result1)

    result2 = max_cluster(graph)
    print(",".join(sorted(result2)))

if  __name__ == "__main__":
    main()