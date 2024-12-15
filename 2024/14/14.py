from functools import reduce
from operator import mul

small_size = (11, 7)
size = (101, 103)

# dict: (start, velocity) : position
robots = {}
with open("day14.txt") as file:
    for line in file.readlines():
        s = line.split(",")
        start = (int(s[0].lstrip("p=")), int(s[1].split()[0]))
        vel = (int(s[1].split()[1].lstrip("v=")), int(s[2]))
        # starts at starting position
        robots[(start, vel)] = start


def move_per_second(robot, size):
    global robots
    # current position
    x, y = robots[robot]
    _, velo = robot

    # modulo leads robot to teleport on edges
    nx, ny = (x + velo[0]) % size[0], (y + velo[1]) % size[1]
    robots[robot] = (nx, ny)


def safety_factor(size):
    global robots
    robots_per_quadrant = [0 for _ in range(4)]
    quad_size = int((size[0] - 1) / 2), int((size[1] - 1) / 2)
    # top left corners of each quadrant
    quad_corners = [(0, 0), (quad_size[0] + 1, 0), (0, quad_size[1] + 1), (quad_size[0] + 1, quad_size[1] + 1)]
    for i, quad in enumerate(quad_corners):
        tiles = [(quad[0] + x, quad[1] + y) for x in range(quad_size[0]) for y in range(quad_size[1])]
        for tile in tiles:
            amount_robots = len([pos for pos in robots.values() if pos == tile])
            if amount_robots != 0:
                robots_per_quadrant[i] += amount_robots
    result = reduce(mul, robots_per_quadrant)
    return result


def check_christmas_tree(size):
    global robots
    result = False

    return result


def visualize(size):
    global robots
    result = ""
    for y in range(size[1]):
        row_string = ""
        for x in range(size[0]):
            if (x, y) in robots.values():
                row_string += "#"
            else:
                row_string += "."
        result += row_string + "\n"
    return result


def puzzle_1(size):
    for i in range(100):
        for robot in robots.keys():
            move_per_second(robot, size)
    print(safety_factor(size))


def puzzle_2(size):
    seconds_passed = 0
    while True:
        for robot in robots.keys():
            move_per_second(robot, size)
        if check_christmas_tree(size):
            return seconds_passed

        if seconds_passed >= 10000:
            # safety net
            return 0


# VISUALIZE:
for i in range(2000):
    print(i)
    print(visualize(size))
    for robot in robots.keys():
        move_per_second(robot, size)








