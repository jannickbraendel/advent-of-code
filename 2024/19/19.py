def parse(file):
    file = open(file, "r")
    lines = file.readlines()
    patterns_local = lines[0].rstrip("\n").split(", ")
    designs_local = [lines[i].rstrip("\n") for i in range(2, len(lines))]

    return patterns_local, designs_local


class TowelNode:
    def __init__(self, pattern):
        self.pattern = pattern
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def search_design(design):
    print(f"design: {design}")
    root = TowelNode("")
    queue = [root]
    while len(queue) > 0:
        current = queue.pop(0)

        if current.pattern == design:
            return True
        print(f"queue: {len(queue)}")

        child_patterns = [(current.pattern + p) for p in patterns]
        for cp in child_patterns:
            if not design.startswith(cp):
                continue
            node = TowelNode(cp)
            current.add_child(node)
            queue.append(node)

    return False


patterns, designs = parse("day19-small.txt")


possible_designs = 0
for i, d in enumerate(designs):
    print(i)
    possible_designs += search_design(d)

print(possible_designs)

