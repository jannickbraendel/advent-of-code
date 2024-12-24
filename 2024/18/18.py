from collections import deque
from enum import Enum
from math import inf


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


def parse(file):
    result = []
    with open(file, "r") as file:
        for line in file.readlines():
            # turn around indices to (row, column)
            result.append(tuple(map(int, reversed(line.split(",")))))
    return result


def find_shortest_path(start, size, corrupted):
    q = deque([(start, 0)])
    visited = set()
    visited.add(start)

    while q:
        pos, steps = q.popleft()

        if pos == (size, size):
            return steps

        for direction in Direction:
            nx, ny = move(pos, direction)

            if (
                0 <= nx <= size and
                0 <= ny <= size and
                (nx, ny) not in corrupted and
                (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                q.append(((nx, ny), steps + 1))

    # no path is found
    return inf


# Brute Force for part 2
def find_blocking_byte(start, size, corrupted, remaining_bytes):
    c = corrupted[:]
    for byte in remaining_bytes:
        print(f"remaining: {len(remaining_bytes) - (len(c) - (len(corrupted)))}")
        c.append(byte)
        if find_shortest_path(start, size, c) == inf:
            # no path to exit
            return tuple(reversed(byte))


total_bytes = parse("day18.txt")
starting_bytes = 1024
corrupted = total_bytes[:starting_bytes]
bytes_remaining = total_bytes[starting_bytes:]
print(find_shortest_path((0, 0), 70, corrupted))
print(f"First blocking byte: {find_blocking_byte((0, 0), 70, corrupted, bytes_remaining)}")
