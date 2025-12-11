from collections import defaultdict, deque
import lib

def count_paths(graph, start, end, path):
    path = path + [start]

    if start == end:
        return 1

    total = 0
    for node in graph[start]:
        total += count_paths(graph, node, end, path)

    return total


def topological_sort(graph):
    inputs = defaultdict(int)

    for u in graph:
        for v in graph[u]:
            inputs[v] += 1

    queue = deque(u for u in graph if inputs[u] == 0)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)

        for v in graph[u]:
            inputs[v] -= 1
            if inputs[v] == 0:
                queue.append(v)

    return order

def count_paths_dp(graph, source, destination):

    counts = defaultdict(int)
    counts[source] = 1

    for u in topological_sort(graph):
        for v in graph[u]:
            counts[v] += counts[u]

    return counts[destination]

def main():
    lines = lib.read_lines()
    connections = {key: value.split() for key, value in (line.split(":", 1) for line in lines)}
    graph = defaultdict(list, connections)

    result1 = count_paths(graph, "you", "out", [])
    print(result1)

    a1 = count_paths_dp(graph, "svr", "dac")
    a2 = count_paths_dp(graph, "dac", "fft")
    a3 = count_paths_dp(graph, "fft", "out")

    b1 = count_paths_dp(graph, "svr", "fft")
    b2 = count_paths_dp(graph, "fft", "dac")
    b3 = count_paths_dp(graph, "dac", "out")

    result2 = a1*a2*a3 + b1*b2*b3
    print(result2)

if __name__ == "__main__":
    main()
