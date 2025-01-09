
def parse(file):
    file = open(file, "r")
    lines = file.readlines()
    patterns_local = lines[0].rstrip("\n").split(", ")
    designs_local = [lines[i].rstrip("\n") for i in range(2, len(lines))]

    return patterns_local, designs_local


def design_pattern_match(design):
    for p in patterns:
        if design == p:
            return True
    return False


# check if design is a prefix of a pattern
def design_pattern_prefix_match(design):
    for p in patterns:
        if p.startswith(design):
            return True
    return False



def check_design(design):
    print(f"checking (sub)-design {design}")
    if len(design) == 0:
        # whole design matches
        return True

    if len(design) == 1:
        return design_pattern_match(design)

    cur_design = ""
    prefix_length = 1
    while True:
        # add letters to current design and check if it corresponds to pattern
        cur_design = design[:prefix_length]

        if design_pattern_prefix_match(cur_design):
            # pattern starts with current sub design -> check next color
            prefix_length += 1
        else:
            prefix_length -= 1
            break

    if not design_pattern_match(design[:prefix_length]):
        # prefix is not matching at all
        return False

    return check_design(design[prefix_length:])


patterns, designs = parse("day19-small.txt")
possible_designs = 0
for d in designs:
    possible_designs += check_design(d)

print(possible_designs)
