from enum import Enum
from typing import Dict, Tuple, Set


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def parse_map(file):
    topography = []
    for line in open(file, "r").readlines():
        row = []
        for x in line:
            if x == "\n":
                continue
            elif x != ".":
                row.append(int(x))
            else:
                row.append(x)
        topography.append(row)
    return topography


def get_trailhead_score(topography, trail_head, cur_position, height):
    global trail_ends
    x, y = cur_position
    if topography[x][y] == 9:
        # found trail-end -> score + 1
        if cur_position not in trail_ends[trail_head]:
            trail_ends[trail_head].add(cur_position)
            return 1

    next_positions = []
    for direction in Direction:
        new_pos = hike(cur_position, direction)
        nx, ny = new_pos
        if 0 <= nx < len(topography) and 0 <= ny < len(topography[0]):
            if topography[nx][ny] == height + 1:
                # next position is 1 level higher -> add to next-positions
                next_positions.append(new_pos)

    if len(next_positions) == 0:
        # trail stops
        return 0

    scores = [get_trailhead_score(topography, trail_head, next_pos, height + 1) for next_pos in next_positions]
    return sum(scores)


def get_trailhead_rating(topography, trail_head, path, height):
    global trail_paths
    # current position
    cur_position = path[-1]
    x, y = cur_position
    if topography[x][y] == 9:
        # found trail-end -> rating + 1
        if path not in trail_paths[trail_head]:
            trail_paths[trail_head].add(path)
            return 1

    next_positions = []
    for direction in Direction:
        new_pos = hike(cur_position, direction)
        nx, ny = new_pos
        if 0 <= nx < len(topography) and 0 <= ny < len(topography[0]):
            if topography[nx][ny] == height + 1:
                # next position is 1 level higher -> add to next-positions
                next_positions.append(new_pos)

    if len(next_positions) == 0:
        return 0

    ratings = [get_trailhead_rating(topography, trail_head, path + (next_pos, ), height + 1) for next_pos in next_positions]
    return sum(ratings)


def compute_trailhead_stats(file):
    global trail_ends
    topography = parse_map(file)
    n = len(topography)
    m = len(topography[0])

    score = 0
    rating = 0

    trailheads = [(x, y) for x in range(n) for y in range(m) if topography[x][y] == 0]
    for head in trailheads:
        trail_ends[head] = set()
        trail_paths[head] = set()
        score += get_trailhead_score(topography, head, head, 0)
        # initial path is a tuple with one tuple inside (starting point) -> can be hashed through instead of list
        init_path = (head, ) + ()
        rating += get_trailhead_rating(topography, head, init_path, 0)

    return score, rating


def hike(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


# dictionary of trailheads (key) and their trail-ends(set, value)
trail_ends = {}
# dict of trailheads and set of their paths as tuples of position-tuples to trail-ends
trail_paths = {}
print(compute_trailhead_stats("day10.txt"))
