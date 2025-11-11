import re
import lib

def hlf(instruction: dict, registers: dict):
    r = instruction["register"]
    registers[r] //= 2
    registers["pc"] += 1

def tpl(instruction: dict, registers: dict):
    r = instruction["register"]
    registers[r] *= 3
    registers["pc"] += 1

def inc(instruction: dict, registers: dict):
    r = instruction["register"]
    registers[r] += 1
    registers["pc"] += 1

def jmp(instruction: dict, registers: dict):
    o = instruction["offset"]
    registers["pc"] += o

def jie(instruction: dict, registers: dict):
    r = instruction["register"]
    v = registers[r]
    o = instruction["offset"]
    registers["pc"] += o if v & 1 == 0 else 1

def jio(instruction: dict, registers: dict):
    r = instruction["register"]
    v = registers[r]
    o = instruction["offset"]
    registers["pc"] += o if v == 1 else 1

isa = {
    "hlf": hlf,
    "tpl": tpl,
    "inc": inc,
    "jmp": jmp,
    "jie": jie,
    "jio": jio
}

def execute(instruction: dict, registers: dict):
    code = isa[instruction["opcode"]]
    code(instruction, registers)

def run(program: list, registers: dict):

    length = len(program)
    registers["pc"] = 0

    while registers["pc"] >= 0 and registers["pc"] < length:
        instruction = program[registers["pc"]]
        execute(instruction, registers)

pattern = r"(?P<opcode>[a-z]{3}) (?P<register>[ab])?(, )?(?P<offset>[+-]\d+)?"

def main():
    lines = lib.read_lines()
    program = [lib.ints(re.match(pattern, line).groupdict()) for line in lines]

    registers1 = {"a": 0, "b": 0}
    run(program, registers1)
    result1 = registers1["b"]
    print(result1)

    registers2 = {"a": 1, "b": 0}
    run(program, registers2)
    result2 = registers2["b"]
    print(result2)

if __name__ == "__main__":
    main()
