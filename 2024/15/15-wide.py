from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def move(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


def reverse_direction(direction):
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.UP
    elif direction == Direction.LEFT:
        return Direction.RIGHT
    else:
        return Direction.LEFT


def parse(file):
    lines = open(file, "r").readlines()
    middle = lines.index("\n")
    warehouse = []
    movements = []
    warehouse_rows = [row.rstrip("\n") for row in [lines[i] for i in range(middle)]]
    for r in warehouse_rows:
        new_row = []
        for x in r:
            if x == "#":
                new_row += ["#", "#"]
            elif x == "O":
                new_row += ["[", "]"]
            elif x == "." or x == "@":
                new_row += [x, "."]
        warehouse.append(new_row)
    movement_rows = [lines[i].rstrip("\n") for i in range(middle + 1, len(lines))]
    for m in movement_rows:
        movements += [x for x in m]
    return warehouse, movements


# changes state of warehouse and returns robot position after one move
def move_robot_wide(pos, direction):
    global warehouse

    nx, ny = move(pos, direction)

    if warehouse[nx][ny] == ".":
        # move robot to next position
        warehouse[pos[0]][pos[1]] = "."
        warehouse[nx][ny] = "@"
        return nx, ny
    else:
        # find last box in the way
        x, y = nx, ny
        while warehouse[x][y] == "]":
            # move 2 steps
            x, y = move(move((x, y), direction), direction)
            print(f"move boxes: {x, y}")
        if warehouse[x][y] == ".":
            # move each part of box one step further
            # loop from free field towards new robot position
            ix, iy = x, y
            reverse = reverse_direction(direction)
            while (ix, iy) != (nx, ny):
                warehouse[ix][iy] = "["
                ix, iy = move((ix, iy), reverse)
                warehouse[ix][iy] = "]"

            # move robot to next position
            warehouse[pos[0]][pos[1]] = "."
            warehouse[nx][ny] = "@"
            return nx, ny

    # next position is wall or non-movable box
    return pos


def execute_movements():
    global warehouse, movements
    # find robot
    n = len(warehouse)
    m = len(warehouse[0])
    robot_pos = (0, 0)
    for i in range(n):
        for j in range(m):
            if warehouse[i][j] == "@":
                robot_pos = (i, j)

    print(f"Initial: {robot_pos}")
    for i in range(n):
        print(warehouse[i])

    for mvt in movements:
        direction = Direction.UP
        match mvt:
            case "^":
                direction = Direction.UP
            case "v":
                direction = Direction.DOWN
            case "<":
                direction = Direction.LEFT
            case ">":
                direction = Direction.RIGHT

        robot_pos = move_robot_wide(robot_pos, direction)
        print(f"Move: {mvt}, Robot: {robot_pos}")
        for i in range(n):
            print(warehouse[i])


def compute_box_coords():
    global warehouse
    result = 0
    n = len(warehouse)
    m = len(warehouse[0])
    for i in range(n):
        for j in range(m):
            if warehouse[i][j] == "[":
                result += 100 * i + j
    return result


warehouse, movements = parse("day15-small.txt")
print(warehouse)
print(movements)
execute_movements()
