from enum import Enum
from math import inf


def parse(file):
    result = []
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
            a.append(x)
        result.append(a)

    return result, start, end


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


def find_shortest_paths(pos: (int, int), direction: Direction, current_path: [((int, int), Direction)], current_score: int):
    global shortest_paths, blocked, min_score
    if pos == end_pos:
        # found end
        if current_score <= min_score:
            shortest_paths.append((current_path, current_score))
            min_score = current_score
            print("updated min score")
        print("found path")
        return

    blocked.add(pos)

    for d in [direct for direct in Direction if direct != get_opposite_direction(direction)]:
        # check where to go next
        next_tile = move(pos, d)
        nx, ny = next_tile

        if get_maze(nx, ny) == "#" or next_tile in blocked:
            continue

        # update current score and check if it's above the current min score
        new_score = current_score + 1
        if d != direction:
            # made turn
            new_score += 1000

        if new_score > min_score:
            continue

        if ((nx, ny), d) in visited and visited[((nx, ny), d)] < new_score:
            # visited before with lower score -> can be discarded
            print("visited this node before")
            continue

        visited[((nx, ny), d)] = new_score

        print(f"next: {next_tile}, direction: {d}, score: {new_score}")
        find_shortest_paths(next_tile, d, current_path + [(next_tile, d)], new_score)

    blocked.remove(pos)


def filter_shortest_paths():
    global shortest_paths
    shortest_paths = [(path, score) for (path, score) in shortest_paths if score <= min_score]


def find_best_sitting_spots():
    result = set()
    for (path, _) in shortest_paths:
        for (pos, _) in path:
            result.add(pos)
    return result


maze, start_pos, end_pos = parse("day16.txt")
# cells that are part of the current path buffer
blocked = set()
shortest_paths: [(((int, int), Direction), int)] = []
visited: {((int, int), Direction): int} = dict()
visited[(start_pos, Direction.RIGHT)] = 0
min_score = float(inf)

find_shortest_paths(start_pos, Direction.RIGHT, [(start_pos, Direction.RIGHT)], 0)
filter_shortest_paths()
print(f"Spots: {find_best_sitting_spots()}")
print(f"Amount of Sitting Spots: {len(find_best_sitting_spots())}")
