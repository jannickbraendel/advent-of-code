def parse(file):
    file = open(file, "r")
    lines = file.readlines()
    patterns_local = lines[0].rstrip("\n").split(", ")
    designs_local = [lines[i].rstrip("\n") for i in range(2, len(lines))]

    return patterns_local, designs_local


def check_design(design):

    # array of bool values: true if design can be made UNTIL that index
    bool_array = [False for _ in range(len(design) + 1)]

    # empty design can always be made
    bool_array[0] = True

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and bool_array[i - len(pattern)]:
                if design[i - len(pattern) : i] == pattern:
                    bool_array[i] = True

    return bool_array[len(design)]


def check_design_2(design):

    amount_array = [0] * (len(design) + 1)
    amount_array[0] = 1

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and amount_array[i - len(pattern)] > 0:
                if design[i - len(pattern) : i] == pattern:
                    amount_array[i] += amount_array[i - len(pattern)]

    print(amount_array)

    return amount_array[len(design)]

patterns, designs = parse("day19.txt")


possible_designs = 0
for i, d in enumerate(designs):
    possible_designs += check_design_2(d)

print(possible_designs)

