import re
import lib

def replacemets(text, old, new):
    parts = text.split(old)

    if len(parts) == 1:
        return

    for n in range(1, len(parts)):
        yield old.join(parts[:n]) + new + old.join(parts[n:])

pattern = r"(?P<in>\w+) => (?P<out>\w+)"

def run1(rules, target):
    calibrations = set()
    for old, new in rules:
        calibrations |= set(replacemets(target, old, new))

    return len(calibrations)

def purify(rules):
    pure = []
    rest = []
    for i, (old, new) in enumerate(rules):
        alternate1 = [(j, n) for j, (_, n) in enumerate(rules) if i != j and n in new]
        alternate2 = [(j, n1, n2) for j, (_, n1) in enumerate(rules) if i != j for k, (_, n2) in enumerate(rules) if i != k and new in n1 + n2]

        if not alternate1 and not alternate2:
            pure.append((old, new))
        else:
            rest.append((old, new))

    return pure, rest

def apply_pure(target, rules):
    count = 0
    text = target

    same = False
    while not same:
        same = True
        for old, new in rules:
            parts = text.split(new)
            same &= (len(parts) == 1)
            count += len(parts)-1
            text = old.join(parts)

    return count, text

def main():
    lines = lib.read_lines()
    rules = [(d["in"], d["out"]) for d in [re.match(pattern, line).groupdict() for line in lines[:-2]]]
    target = lines[-1]

    #result1 = run1(rules, target)
    #print(result1)

    pure, rest = purify(rules)
    count, reminder = apply_pure(target, pure)

    if reminder == "e":
        result2 = count
        print(result2)

if __name__ == "__main__":
    main()
