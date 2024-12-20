from enum import Enum
from math import inf


def parse(file):
    result = []
    walls = []
    rows = [line.rstrip("\n") for line in open(file, "r").readlines()]
    start = (0, 0)
    end = (0, 0)
    for i, row in enumerate(rows):
        a = []
        for j, x in enumerate(row):
            if x == "S":
                start = (i, j)
            elif x == "E":
                end = (i, j)
            elif x == "#":
                walls.append((i, j))
            a.append(x)
        result.append(a)

    return result, start, end, walls


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def move(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


def get_opposite_direction(direction: Direction):
    directions = [d for d in Direction]
    idx = (directions.index(direction) + 2) % 4
    return directions[idx]


def get_maze(i, j):
    return maze[i][j]


def find_shortest_path(pos: (int, int), direction: Direction, current_path: [((int, int), Direction)]):
    global paths, blocked
    if pos == end_pos:
        # found end
        paths.append(current_path)
        return

    blocked.add(pos)

    for d in [direct for direct in Direction if direct != get_opposite_direction(direction)]:
        # check where to go next
        next_tile = move(pos, d)
        nx, ny = next_tile

        if get_maze(nx, ny) == "#" or next_tile in blocked:
            continue

        print(f"next: {next_tile}, direction: {d}, maze-character: {get_maze(nx, ny)}")
        find_shortest_path(next_tile, d, current_path + [(next_tile, d)])

    blocked.remove(pos)


def score(path):
    turns = 0
    current_direction = Direction.RIGHT
    for (_, direction) in path:
        if direction != current_direction:
            turns += 1
            current_direction = direction

    steps = set([pos for (pos, _) in path])

    return len(steps) - 1 + 1000 * turns


def minimum_score():
    result = inf
    for path in paths:
        s = score(path)
        result = min(s, result)

    return result


maze, start_pos, end_pos, walls = parse("day16.txt")
# cells that are part of the current path buffer
blocked = set()
paths = []
print(walls)

find_shortest_path(start_pos, Direction.RIGHT, [(start_pos, Direction.RIGHT)])
print(minimum_score())

