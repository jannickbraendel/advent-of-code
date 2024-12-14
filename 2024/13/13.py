
def parse(file, largePrize):
    machines = [[]]
    with (open(file, "r") as file):
        machine_id = 0
        for line in file.readlines():
            if line == "\n":
                machine_id += 1
                machines.append([])
            elif "A" in line:
                a_x = int(line.lstrip("Button A: X+").split(",")[0])
                a_y = int(line.split(",")[1].lstrip(" Y+").rstrip("\n"))
                machines[machine_id].append((a_x, a_y))
            elif "B" in line:
                b_x = int(line.lstrip("Button B: X+").split(",")[0])
                b_y = int(line.split(",")[1].lstrip(" Y+").rstrip("\n"))
                machines[machine_id].append((b_x, b_y))
            else:
                prize_x = int(line.lstrip("Prize: X=").split(",")[0])
                prize_y = int(line.split(",")[1].lstrip(" Y=").rstrip("\n"))
                if largePrize:
                    machines[machine_id].append((prize_x + 10000000000000, prize_y + 10000000000000))
                else:
                    machines[machine_id].append((prize_x, prize_y))

        return machines


def calc_tokens_for_price(machine):
    but_a, but_b, prize = machine

    # go through A positions and check if we can get to the price by pressing B
    # max. 100 times
    for a in range(1, 101):
        for b in range(1, 101):
            pos = a * but_a[0] + b * but_b[0], a * but_a[1] + b * but_b[1]
            if pos[0] == prize[0] and pos[1] == prize[1]:
                return a * 3 + b

    return 0


def solve_tokens_large(machine):
    # solve linear equation system instead of bruteforce
    but_a, but_b, prize = machine
    a = (prize[0] * but_b[1] - prize[1] * but_b[0]) / (but_a[0] * but_b[1] - but_a[1] * but_b[0])
    b = (prize[0] - a * but_a[0]) / but_b[0]

    if a % 1 == b % 1 == 0:
        return int(a * 3 + b)
    return 0


def calc_tokens(file):
    machines = parse(file, True)
    result = 0
    for machine in machines:
        print(f"machine: {machines.index(machine)}")
        result += solve_tokens_large(machine)

    return result


print(calc_tokens("day13.txt"))

