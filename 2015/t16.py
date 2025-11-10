import re
import lib

readings = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

readings2 = {
    "children": (3,3),
    "cats": (8,9999),
    "samoyeds": (2,2),
    "pomeranians": (0,2),
    "akitas": (0,0),
    "vizslas": (0,0),
    "goldfish": (0,4),
    "trees": (4,9999),
    "cars": (2,2),
    "perfumes": (1,1)
}

split = r"Sue (?P<name>[\d]+): (?P<rest>.*)"
attrs = r"(?P<trait>\w+): (?P<value>-?\d+)(, )?"

def extract(line):
    m = re.match(split, line)
    name = m["name"]
    rest = m["rest"]

    result = {m["trait"]: int(m["value"]) for m in re.finditer(attrs, rest)}
    return name, result

def match(data):
    m = all(readings[k] == v for k, v in data.items())
    return m

def match2(data):
    m = all(readings2[k][0] <= v and readings2[k][1] >= v for k, v in data.items())
    return m

def main():
    lines = lib.read_lines()
    facts = {k: v for k, v in (extract(line) for line in lines)}

    matches1 = (name for name, data in facts.items() if match(data))
    result1 = next(matches1)
    print(result1)

    matches2 = (name for name, data in facts.items() if match2(data))
    result2 = next(matches2)
    print(result2)

if __name__ == "__main__":
    main()
