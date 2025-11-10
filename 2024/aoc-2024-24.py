import sys
import re

def parse(lines):

    lines = [l.strip() for l in lines]
    split = next(i for i, e in enumerate(lines) if not e)

    setup = [re.match(r"(\w+): (\d)", line).groups() for line in lines[:split]]
    logic = [re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line).groups() for line in lines[split+1:]]

    return setup, logic

def compile(setup, logic):
    values = {k: int(v) for k, v in setup}
    assignments = {rd: (r1, o, r2) for r1, o, r2, rd in logic}

    return values,assignments

def calculate(values, assignments, name):
    if name not in values:
        r1n, op, r2n = assignments[name]
        r1v = calculate(values, assignments, r1n)
        r2v = calculate(values, assignments, r2n)

        if op == 'AND':
            v = r1v & r2v
        elif op == 'OR':
            v = r1v | r2v
        if op == 'XOR':
            v = r1v ^ r2v

        values[name] = v

    return values[name]

def calculate_all(values, assignments):
    for name in assignments.keys():
        calculate(values, assignments, name)

def dependencies(assignments, name):
    if name in assignments:
        r1n, _, r2n = assignments[name]
        d1 = dependencies(assignments, r1n)
        d2 = dependencies(assignments, r2n)
        return d1 | d2
    else:
        return {name}

def z_dependencies(assignments):

    for k in sorted([x for x in assignments.keys() if x[0] == 'z']):
        d = dependencies(assignments, k)
        print(k, sorted(d))

def gather(values):

    result = 0

    for k, v in values.items():
        if k[0] == 'z':
            i = int(k[1:])
            result |= v << i

    return result

def apply(renames, assignments):
    renamed_assignments = {}
    
    for r3, formula in assignments.items():
        r1, op, r2 = formula

        if r1 in renames:
            r1 = renames[r1]
        if r2 in renames:
            r2 = renames[r2]
        if r3 in renames:
            r3 = renames[r3]

        renamed_assignments[r3] = (r1, op, r2)

    return renamed_assignments


def find_renames(assignments, regex, src, dst):
    renames = {}

    for r3, formula in assignments.items():
        r1, op, r2 = formula
        
        t = f"{r1} {op} {r2} -> {r3}"
        m = re.match(regex, t)
        if m:
            s = src.format(**m.groupdict())
            d = dst.format(**m.groupdict())
            renames[s] = d

    return renames

def rename(assignments):
    renames = {}
    renamed_assignments = assignments

    #1st xor
    #(x|y)\d+ XOR (x|y)\d+ -> [^z]\w+
    #rename to hnn
    r = find_renames(renamed_assignments, r"(x|y)(?P<nn>\d+) XOR (x|y)\d+ -> (?P<src>[a-z]+)", "{src}", "h{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    #2nd xor
    #\w+ XOR \w+ -> z\d+
    #rename non-hnn to cnn
    r = find_renames(renamed_assignments, r"h\d+ XOR (?P<src>[a-z]+) -> z(?P<nn>\d+)", "{src}", "c{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r
    r = find_renames(renamed_assignments, r"(?P<src>[a-z]+) XOR h\d+ -> z(?P<nn>\d+)", "{src}", "c{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    #1st and
    #(x|y)\d+ AND (x|y)\d+ -> [^z]\w+
    #rename to inn
    r = find_renames(renamed_assignments, r"(x|y)(?P<nn>\d+) AND (x|y)\d+ -> (?P<src>[a-z]+)", "{src}", "i{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    # UNUSED
    #2nd and
    #(x|h)\d+ AND (x|h)\d+ -> [^z]\w+
    #rename to jnn
    r = find_renames(renamed_assignments, r"(x|h)(?P<nn>\d+) AND (x|h)\d+ -> (?P<src>[a-z]+)", "{src}", "j{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    # UNUSED
    #3rd and
    #(y|h)\d+ AND (y|h)\d+ -> [^z]\w+
    #rename to knn
    r = find_renames(renamed_assignments, r"(y|h)(?P<nn>\d+) AND (y|h)\d+ -> (?P<src>[a-z]+)", "{src}", "k{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    #unusual and
    #(c|h)\d+ AND (c|h)\d+ -> [^z]\w+
    #rename to knn
    r = find_renames(renamed_assignments, r"(c|h)(?P<nn>\d+) AND (c|h)\d+ -> (?P<src>[a-z]+)", "{src}", "l{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    # UNUSED
    #interim or
    #(i|j|k)\d+ OR (i|j|k)\d+ -> [^c]\w+
    #rename to snn
    r = find_renames(renamed_assignments, r"(i|j|k)(?P<nn>\d+) OR (i|j|k)\d+ -> (?P<src>[a-z]+)", "{src}", "s{nn}")
    renamed_assignments = apply(r, renamed_assignments)
    renames |= r

    return renames, renamed_assignments

def dump(assignments):
    for k, formula in sorted(assignments.items()):
        r1, op, r2 = formula
        print(f"{r1} {op} {r2} -> {k}")

def main():
    filename = sys.argv[0] + ".3.txt"

    with open(filename, 'r') as file:
        lines = file.readlines()

    setup, logic = parse(lines)

    values, assignments = compile(setup, logic)

    #calculate_all(values, assignments)
    #result1 = gather(values)
    #print(result1)

    #z_dependencies(assignments)

    renames, renamed_assignments = rename(assignments)
    dump(renamed_assignments)

if __name__ == "__main__":
    main()
