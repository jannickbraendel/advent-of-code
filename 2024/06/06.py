from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def parse_map(input):
    obstructions = []
    start_pos = (0, 0)

    file = open(input, "r")
    guard_map = list(map(list, file.readlines()))

    n = len(guard_map)
    m = len(guard_map[0]) - 1

    for i in range(n):
        for j in range(m):
            x = guard_map[i][j]
            if x == "#":
                obstructions.append((i, j))
            elif x == "^":
                start_pos = (i, j)

    return guard_map, n, m, obstructions, start_pos


def turn_right(direction):
    # change direction (turn right):
    if direction == Direction.UP:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    else:
        return Direction.UP


def run_step(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


def compute_guard_pattern(input):
    guard_map, n, m, obstructions, start_pos = parse_map(input)

    # set of tuples (position, direction) to check for loops later
    visited = set([])
    distinct_positions = set([])

    direction = Direction.UP

    cur_pos = start_pos

    while 0 <= cur_pos[0] < n and 0 <= cur_pos[1] < m:

        # get to next field
        if (run_step(cur_pos, direction)) in obstructions:
            direction = turn_right(direction)

        visited.add((cur_pos, direction))
        distinct_positions.add(cur_pos)
        cur_pos = run_step(cur_pos, direction)

    return visited, len(distinct_positions)


def count_potential_loops(input, visited):
    guard_map, n, m, obstructions, start_pos = parse_map(input)
    potential_loops = set([])

    for (pos, _) in visited:
        if pos == start_pos:
            continue
        # dictionary (pos, direction) : visit_count
        temp_visited = {}
        # init dictionary
        for (position, direction) in visited:
            temp_visited[(position, direction)] = 0

        temp_obstructions = obstructions[:]
        temp_obstructions.append(pos)

        cur_pos = start_pos
        direction = Direction.UP

        while 0 <= cur_pos[0] < n and 0 <= cur_pos[1] < m:

            # get to next field
            if run_step(cur_pos, direction) in temp_obstructions:
                direction = turn_right(direction)

            # print(f"added obstr.: {pos}, current: {cur_pos}, direction: {direction.name}")

            if (cur_pos, direction) in temp_visited.keys():
                # update visit_count if position was visited before
                temp_visited[(cur_pos, direction)] += 1
            else:
                # print(f"added to visited: {(cur_pos, direction, 0)}")
                temp_visited[(cur_pos, direction)] = 0

            # check for loop
            if temp_visited[(cur_pos, direction)] >= 2:
                print(f"found loop: {pos}")
                potential_loops.add(pos)
                break

            cur_pos = run_step(cur_pos, direction)

    return len(potential_loops)


visited, position_count = compute_guard_pattern("day06.txt")
print(position_count)
print(count_potential_loops("day06.txt", visited))

# print((0, 0) <= (1, -1))

