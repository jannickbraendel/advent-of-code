
def parse(file):
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
                machines[machine_id].append((prize_x + 10000000000000, prize_y + 10000000000000))

        return machines


def calc_tokens_for_price(machine):
    but_a = machine[0]
    but_b = machine[1]
    prize = machine[2]

    # go through A positions and check if we can get to the price by pressing B
    # max. 100 times
    for a_tokens in range(1, 100):
        pos_x = a_tokens * but_a[0]
        pos_y = a_tokens * but_a[1]

        missing_x = prize[0] - pos_x
        missing_y = prize[1] - pos_y

        for b_tokens in range(1, 100):
            if b_tokens * but_b[0] == missing_x and b_tokens * but_b[1] == missing_y:
                return a_tokens * 3 + b_tokens

    return 0


def calc_tokens(file):
    machines = parse(file)
    result = 0
    for machine in machines:
        print(f"machine: {machines.index(machine)}")
        result += calc_tokens_for_price(machine)

    return result


print(calc_tokens("day13-small.txt"))

