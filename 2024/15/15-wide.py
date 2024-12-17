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
    boxes = []
    warehouse_rows = [row.rstrip("\n") for row in [lines[i] for i in range(middle)]]
    for i, r in enumerate(warehouse_rows):
        new_row = []
        for j, s in enumerate(r):
            if s == "#":
                new_row += ["#", "#"]
            elif s == "O":
                new_row += ["[", "]"]
                boxes.append(((i, j*2), (i, j*2 + 1)))
            elif s == "." or s == "@":
                new_row += [s, "."]
        warehouse.append(new_row)
    movement_rows = [lines[i].rstrip("\n") for i in range(middle + 1, len(lines))]
    for m in movement_rows:
        movements += [x for x in m]
    return warehouse, movements, boxes


def get_box_positions():
    global boxes
    return [box[0] for box in boxes] + [box[1] for box in boxes]


def push_boxes(box, direction):
    global warehouse, boxes


# changes state of warehouse and returns robot position after one move
def move_robot_wide(pos, direction):
    global warehouse

    nx, ny = move(pos, direction)

    if warehouse[nx][ny] == ".":
        # move robot to next position
        warehouse[pos[0]][pos[1]] = "."
        warehouse[nx][ny] = "@"
        return nx, ny
    elif (nx, ny) in get_box_positions():
        # push boxes if possible
        if push_boxes((nx, ny), direction):
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


warehouse, movements, boxes = parse("day15-small.txt")
print(boxes)
print(get_box_positions())
# execute_movements()
