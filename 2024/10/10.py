from enum import Enum


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
            print(trail_ends)
            return 1

    next_positions = []
    for direction in Direction:
        new_pos = hike(cur_position, direction)
        nx, ny = new_pos
        if 0 <= nx < len(topography) and 0 <= ny < len(topography[0]):
            if topography[nx][ny] == height + 1:
                # next position is 1 level higher -> add to new-positions
                next_positions.append(new_pos)

    if len(next_positions) == 0:
        # trail stops
        return 0

    scores = [get_trailhead_score(topography, trail_head, next_pos, height + 1) for next_pos in next_positions]
    return sum(scores)


def compute_trailhead_scores(file):
    global trail_ends
    topography = parse_map(file)
    n = len(topography)
    m = len(topography[0])

    score = 0

    trailheads = [(x, y) for x in range(n) for y in range(m) if topography[x][y] == 0]
    for head in trailheads:
        trail_ends[head] = set()
        score += get_trailhead_score(topography, head, head, 0)

    return score


def hike(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


# dictionary of trailheads (key) and their trailends(set, value)
trail_ends = {}
print(compute_trailhead_scores("day10.txt"))
