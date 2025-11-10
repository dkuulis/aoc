import sys
import re
from enum import Enum
from collections import namedtuple

class Operand(Enum):
    LITERAL = 1
    COMBO = 2

Instruction = namedtuple("Instruction", ["execute", "operand"])

REG_A = 4
REG_B = 5
REG_C = 6
REG_PC = 7

def parse(content):
    
    # Extract register values
    registers_match = re.findall(r'Register (\w): (\d+)', content)
    registers_named = {reg: int(val) for reg, val in registers_match}
    registers = [0, 1, 2, 3, registers_named["A"], registers_named["B"], registers_named["C"], 0]

    # Extract program values
    program_match = re.search(r'Program: ([\d,]+)', content)
    program = list(map(int, program_match.group(1).split(','))) if program_match else []

    return program, registers

# The numerator is the value in the A register.
# The denominator is found by raising 2 to the power of the instruction's combo operand.
# The result of the division operation is truncated to an integer and then written to the A register.
def xdv(value, registers):
    numerator = registers[REG_A]
    denominator = 2 ** value
    result = numerator // denominator
    return result

def adv(value, registers, output):
    result = xdv(value, registers)
    registers[REG_A] = result
    return True

# Calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
def bxl(value, registers, output):
    input = registers[REG_B]
    result = input ^ value
    registers[REG_B] = result
    return True

# Calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
def bst(value, registers, output):
    result = value  % 8
    registers[REG_B] = result
    return True

# Does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
# if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
def jnz(value, registers, output):
    input = registers[REG_A]
    if input != 0:
        registers[REG_PC] = value
    return True

# Calculates the bitwise XOR of register B and register C, then stores the result in register B.
# For legacy reasons, this instruction reads an operand but ignores it.
def bxc(value, registers, output):
    input1 = registers[REG_B]
    input2 = registers[REG_C]
    result = input1 ^ input2
    registers[REG_B] = result
    return True

# Calculates the value of its combo operand modulo 8, then outputs that value.
def out(value, registers, output):
    result = value % 8
    return output(result)

# Works exactly like the adv instruction except that the result is stored in the B register. 
# The numerator is still read from the A register.
def bdv(value, registers, output):
    result = xdv(value, registers)
    registers[REG_B] = result
    return True

# Wworks exactly like the adv instruction except that the result is stored in the C register.
# The numerator is still read from the A register.
def cdv(value, registers, output):
    result = xdv(value, registers)
    registers[REG_C] = result
    return True

opcodes = [
    # adv 0
    Instruction(adv, Operand.COMBO),
    # bxl 1
    Instruction(bxl, Operand.LITERAL),
    # bst 2
    Instruction(bst, Operand.COMBO),
    # jnz 3
    Instruction(jnz, Operand.LITERAL),
    # bxc 4
    Instruction(bxc, Operand.LITERAL),
    # out 5
    Instruction(out, Operand.COMBO),
    # bdv 6
    Instruction(bdv, Operand.COMBO),
    # cdv 7
    Instruction(cdv, Operand.COMBO)
]

def execute1(program, registers):
    registers[REG_PC] = 0
    buffer = []
    count = len(program)

    while True:
        pc = registers[REG_PC]
        if pc < 0 or pc > count-2:
            break

        opcode = program[pc]
        operand = program[pc+1]

        instruction = opcodes[opcode]
        value = operand if instruction.operand == Operand.LITERAL else registers[operand]

        registers[REG_PC] = pc + 2
        instruction.execute(value, registers, buffer.append)

    return buffer

def execute2(program, registers, position):
    registers[REG_PC] = 0
    count = len(program)

    def output(value):
        nonlocal position
        if position >= count:
            return False
        if program[position] != value:
            return False
        position += 1
        return True

    while True:
        pc = registers[REG_PC]
        if pc < 0 or pc > count-2:
            break

        opcode = program[pc]
        operand = program[pc+1]

        instruction = opcodes[opcode]
        value = operand if instruction.operand == Operand.LITERAL else registers[operand]

        registers[REG_PC] = pc + 2
        success = instruction.execute(value, registers, output)
        if not success:
            return False

    return position == count

def solve1(program, registers):
    output = execute1(program, registers)
    print(','.join(str(o) for o in output))

def solve2step(program, registers, known, position):

    position -= 1
    prefix = known << 3
    for da in range(8):
        temp = list(registers)
        a = prefix | da
        temp[REG_A] = a

        #print(position, program[position], da, a)

        if execute2(program, temp, position):
            if position == 0:
                print(a)
                return True
            else:
                if solve2step(program, registers, a, position):
                    return True

    return False

def solve2(program, registers):
    solve2step(program, registers, 0, len(program))

def main():
    filename = sys.argv[0] + ".txt"

    with open(filename, 'r') as file:
        content = file.read()

    program, registers = parse(content)
    #solve1(program, registers)
    solve2(program, registers)


if __name__ == "__main__":
    main()
