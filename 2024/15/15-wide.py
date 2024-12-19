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
    boxes: [(int, int)] = []
    warehouse_rows = [row.rstrip("\n") for row in [lines[i] for i in range(middle)]]
    for i, r in enumerate(warehouse_rows):
        new_row = []
        for j, s in enumerate(r):
            if s == "#":
                new_row += ["#", "#"]
            elif s == "O":
                new_row += ["[", "]"]
                boxes.append((i, j*2))
            elif s == "." or s == "@":
                new_row += [s, "."]
        warehouse.append(new_row)
    movement_rows = [lines[i].rstrip("\n") for i in range(middle + 1, len(lines))]
    for m in movement_rows:
        movements += [x for x in m]
    return warehouse, movements, boxes


# changes state of warehouse and returns robot position after one move
def move_robot_wide(pos, direction):
    global warehouse, boxes

    nx, ny = move(pos, direction)

    if warehouse[nx][ny] == ".":
        # move robot to next position
        warehouse[pos[0]][pos[1]] = "."
        warehouse[nx][ny] = "@"
        return nx, ny
    elif warehouse[nx][ny] == "#":
        # wall
        return pos
    else:
        # recursive function to fill movable boxes array
        # if boxes can be moved -> true else False
        movable_boxes = set([])

        def get_movable_boxes(position, direction):
            x, y = position
            if warehouse[x][y] == ".":
                return True
            elif warehouse[x][y] == "#":
                return False
            elif (x, y) in boxes:
                left_half = (x, y)
                right_half = (x, y + 1)
            elif (x, y - 1) in boxes:
                left_half = (x, y - 1)
                right_half = (x, y)

            movable_boxes.add(left_half)

            next_left = move(left_half, direction)
            next_right = move(right_half, direction)

            if direction in [Direction.UP, Direction.DOWN]:
                return get_movable_boxes(next_left, direction) and get_movable_boxes(next_right, direction)
            elif direction == Direction.LEFT:
                return get_movable_boxes(next_left, direction)
            else:
                return get_movable_boxes(next_right, direction)

        if get_movable_boxes((nx, ny), direction):
            if direction in [Direction.UP, Direction.DOWN]:
                # sort by vertical distance
                key = lambda box: abs(box[0] - pos[0])
            else:
                # sort by horizontal distance
                key = lambda box: abs(box[1] - pos[1])

            sorted_movable_boxes = sorted(list(movable_boxes), key=key, reverse=True)

            for blx, bly in sorted_movable_boxes:
                brx, bry = blx, bly + 1

                nlx, nly = move((blx, bly), direction)
                nrx, nry = move((brx, bry), direction)

                warehouse[blx][bly] = "."
                boxes.remove((blx, bly))
                warehouse[brx][bry] = "."
                warehouse[nlx][nly] = "["
                boxes.append((nlx, nly))
                warehouse[nrx][nry] = "]"

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


# boxes stores only the left half of each box
warehouse, movements, boxes = parse("day15.txt")
execute_movements()
print(compute_box_coords())
