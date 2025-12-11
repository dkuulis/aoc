import lib

def count_paths(graph, start, end, path):
    path = path + [start]

    if start == end:
        return 1

    total = 0
    for node in graph[start]:
        total += count_paths(graph, node, end, path)

    return total

def main():
    lines = lib.read_lines()
    connections = {key: value.split() for key, value in (line.split(":", 1) for line in lines)}

    result1 = count_paths(connections, "you", "out", [])
    print(result1)

    result2 = 0
    print(result2)

if __name__ == "__main__":
    main()
