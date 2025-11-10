import re
import lib

def calculate(name, wiring, cache):

    if name in cache:
        return cache[name]

    rule = wiring[name]

    if "v1" in rule and rule["v1"]:
        v1 = int(rule["v1"])
    elif "a1" in rule and rule["a1"]:
        n1 = rule["a1"]
        v1 = calculate(n1, wiring, cache)
    else:
        v1 = None

    if "v2" in rule and rule["v2"]:
        v2 = int(rule["v2"])
    elif "a2" in rule and rule["a2"]:
        n2 = rule["a2"]
        v2 = calculate(n2, wiring, cache)
    else:
        v2 = None

    op = rule["op"]

    if op == "AND":
        result = v1 & v2
    elif op == "OR":
        result = v1 | v2
    elif op == "NOT":
        result = ~v2
    elif op == "LSHIFT":
        result = v1 << v2
    elif op == "RSHIFT":
        result = v1 >> v2
    elif op is None:
        result = v2
    else:
        raise ValueError(f"Unknown operation {op}.")

    result = result & 0xFFFF
    cache[name] = result
    return result

pattern  = r"((?P<a1>[a-z]+) |(?P<v1>[0-9]+) |)((?P<op>[A-Z]+) )?((?P<a2>[a-z]+)|(?P<v2>[0-9]+)) -> (?P<d>\w+)"

def main():
    lines = lib.read_lines()
    rules = [re.match(pattern, line).groupdict() for line in lines]
    wiring = {r["d"]: r for r in rules}

    result1 = calculate("a", wiring, {})
    print(result1)

    result2 = calculate("a", wiring, {"b": result1})
    print(result2)

if __name__ == "__main__":
    main()
