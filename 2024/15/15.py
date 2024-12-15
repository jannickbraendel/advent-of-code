from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def move(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


def parse(file):
    lines = open(file, "r").readlines()
    middle = lines.index("\n")
    warehouse = []
    movements = []
    warehouse_rows = [row.rstrip("\n") for row in [lines[i] for i in range(middle)]]
    for r in warehouse_rows:
        warehouse.append([x for x in r])

    movement_rows = [lines[i].rstrip("\n") for i in range(middle + 1, len(lines))]
    for m in movement_rows:
        movements += [x for x in m]
    return warehouse, movements


# changes state of warehouse and returns robot position after one move
def move_robot(pos, direction):
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
        while warehouse[x][y] == "O":
            x, y = move((x, y), direction)
        if warehouse[x][y] == ".":
            # boxes can be moved -> move 1st box to the end of box row
            warehouse[x][y] = "O"
            # move robot to ex-1st box position
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

        robot_pos = move_robot(robot_pos, direction)
        print(f"Move: {mvt}, Robot: {robot_pos}")


def compute_box_coords():
    global warehouse
    result = 0
    n = len(warehouse)
    m = len(warehouse[0])
    for i in range(n):
        for j in range(m):
            if warehouse[i][j] == "O":
                result += 100 * i + j
    return result


warehouse, movements = parse("day15.txt")
execute_movements()
print(f"Sum of Box Coordinates: {compute_box_coords()}")


