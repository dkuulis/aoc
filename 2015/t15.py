import re
import lib
from math import prod

split  = r"(?P<name>\w+): (?P<rest>.*)"
attrs  = r"(?P<trait>\w+) (?P<value>-?\d+)(, )?"

def extract(line):
    m = re.match(split, line)
    name = m["name"]
    rest = m["rest"]

    result = {m["trait"]: int(m["value"]) for m in re.finditer(attrs, rest)}
    return name, result

def compose(components, weight):
    if len(components) == 0 or weight == 0:
        return

    first = components[0]
    yield {first: weight}

    if len(components) == 1:
        return
    
    rest = components[1:]

    for first_weight in range(weight-1, 0, -1):
        for x in compose(rest, weight - first_weight):
            yield {first: first_weight} | x
    
    yield from compose(rest, weight)

def compose_calories(components, weight, calories, definitions):
    if len(components) == 0 or weight == 0 or calories <= 0:
        return

    first = components[0]
    first_calories = definitions[first]["calories"]

    if (weight * first_calories == calories):
        yield {first: weight}

    if len(components) == 1:
        return
    
    rest = components[1:]

    for first_weight in range(weight-1, 0, -1):
        c = first_weight * first_calories
        for x in compose_calories(rest, weight - first_weight, calories - c, definitions):
            yield {first: first_weight} | x
    
    yield from compose(rest, weight)

def score(recipee, definitions):
    traits = [max(sum(definitions[i][t]*a for i, a in recipee.items()), 0) for t in ["capacity", "durability", "flavor", "texture"]]
    return prod(traits)

def main():
    lines = lib.read_lines()
    definitions = {k: v for k, v in (extract(line) for line in lines)}
    components = list(definitions.keys())

    result1 = max(score(recipee, definitions) for recipee in compose(components, 100))
    print(result1)

    result2 = max(score(recipee, definitions) for recipee in compose_calories(components, 100, 500, definitions))
    print(result2)

if __name__ == "__main__":
    main()
