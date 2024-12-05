rules = []
updates = []


def parse_input(input):
    file = open(input, "r")

    for line in file.readlines():
        if "|" in line:
            rule = [x for x in map(int, line.split("|"))]
            rules.append(rule)
        elif "," in line:
            update = [x for x in map(int, line.split(","))]
            updates.append(update)


def get_correct_pred_succ(x):
    correct_pred = [a for [a, b] in rules if b == x]
    correct_succ = [b for [a, b] in rules if a == x]
    return correct_pred, correct_succ


def check_rules(update):
    for x in update:
        idx = update.index(x)
        before = [update[i] for i in range(idx)]
        if idx + 1 == len(update):
            after = []
        else:
            after = [update[i] for i in range(idx + 1, len(update))]
        # print(f"update: {update}, idx: {idx}, before: {before}, after: {after}")

        correct_pred, correct_succ = get_correct_pred_succ(x)
        # print(f"x: {x}, pre_rules: {pre_rules}, post_rules: {post_rules}")
        for i in before:
            if i in correct_succ:
                return False
        for i in after:
            if i in correct_pred:
                return False
    return True


def sort_update(update):
    new_indices = []
    for x in update:
        correct_pred, _ = get_correct_pred_succ(x)

        others = list(update)
        others.remove(x)
        new_index = 0
        for other in others:
            if other in correct_pred:
                new_index += 1
        new_indices.append((x, new_index))

    sorted_update = [x for (x, _) in sorted(new_indices, key=lambda elem: elem[1])]
    # print(f"update: {update}, sorted: {sorted_update}")
    return sorted_update


def day05_first(input):
    parse_input(input)

    result = 0

    for update in updates:
        if check_rules(update):
            # add middle page number to result
            result += update[int((len(update) - 1) / 2)]

    return result


def day05_second(input):
    parse_input(input)

    result = 0

    for update in updates:
        if not check_rules(update):
            update = sort_update(update)
            # add middle page number to result
            result += update[int((len(update) - 1) / 2)]

    return result


# print(day05_first("day05.txt"))
print(day05_second("day05.txt"))
