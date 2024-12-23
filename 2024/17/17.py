

def parse(file):
    regs: [int] = []
    # contains opcode and operands alternating
    prog: [int] = []
    with open(file, "r") as file:
        for line in file.readlines():
            if line.startswith("R"):
                regs.append(int(line.split()[2]))
            elif line.startswith("P"):
                prog = list(map(int, line.lstrip("Program: ").split(",")))

    return regs, prog


def get_combo_operand(operand):
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return registers[operand - 4]
    else:
        return -1


def adv(a, operand):
    op = get_combo_operand(operand)
    return int(a / pow(2, op))


def bxl(b, operand):
    return b ^ operand


def bst(operand):
    return get_combo_operand(operand) % 8


def jnz(pointer, a, operand):
    # returns new pointer if needed
    if a == 0:
        return pointer
    else:
        return operand


def bxc(b, c):
    return b ^ c


def out(operand):
    return str(get_combo_operand(operand) % 8)


def bdv(operand):
    pass


def cdv(operand):
    pass


def run_program():
    global registers, program
    inst_pointer = 0
    output: [str] = []
    while inst_pointer < len(program):
        new_pointer = inst_pointer + 2
        operand = program[inst_pointer + 1]
        match program[inst_pointer]:
            case 0:
                registers[0] = adv(registers[0], operand)
            case 1:
                registers[1] = bxl(registers[1], operand)
            case 2:
                registers[1] = bst(operand)
            case 3:
                # jump
                if registers[0] != 0:
                    new_pointer = operand
            case 4:
                registers[1] = bxc(registers[1], registers[2])
            case 5:
                output.append(out(operand))
            case 6:
                registers[1] = adv(registers[0], operand)
            case 7:
                registers[2] = adv(registers[0], operand)

        inst_pointer = new_pointer

    return ",".join(output)


registers, program = parse("day17.txt")
a = registers[0]
output = run_program()
print(f"First output: {output} with registers: {registers}")


# puzzle 2
x = 0

while True:
    if x != a:
        print(x)
        registers[0] = x
        new_output = run_program()

        if new_output == ",".join(map(str, program)):
            print(f"New Register A: {x}")
            break
    x += 1

