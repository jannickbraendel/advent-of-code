from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def move(pos, direction):
    return tuple(map(lambda i, j: i + j, pos, direction.value))


def parse_farm(file):
    result = []
    for line in open(file, "r").readlines():
        result.append(list(line.rstrip("\n")))

    return result


def update_region_stats(pos, region_id):
    global farm, n, m, region_areas, region_sides, plots_in_region
    if pos in plots_in_region:
        return 0

    plots_in_region.add(pos)
    region_areas[region_id] += 1

    x, y = pos
    plant = farm[x][y]
    local_perimeter = 0
    next_positions = []

    for direction in Direction:
        nx, ny = move(pos, direction)

        side = (direction, nx, ny)

        if not (0 <= nx < n and 0 <= ny < m):
            # border to outside of farm
            local_perimeter += 1
            # add side to region_sides (does not matter if already contained)
            region_sides[region_id].append(side)
        else:
            if farm[nx][ny] == plant:
                # found new part of same region
                next_positions.append((nx, ny))
            else:
                # border to other region
                local_perimeter += 1
                region_sides[region_id].append(side)

    if len(next_positions) == 0:
        return local_perimeter

    return local_perimeter + sum(update_region_stats(next_pos, region_id) for next_pos in next_positions)


def get_farm_regions():
    global plots_in_region, farm, n, m, region_perimeters
    region_id = 0
    for i in range(n):
        for j in range(m):
            if (i, j) not in plots_in_region:
                region_areas[region_id] = 0  # is updated in update_region_stats
                region_sides[region_id] = []  # is updated in update_region_stats
                region_perimeters[region_id] = update_region_stats((i, j), region_id)
                print(f"pos: ({i, j}), letter: {farm[i][j]}, area: {region_areas[region_id]}, perimeter: {region_perimeters[region_id]}")
                region_id += 1


def reduce_sides_for_direction(direction, sides):
    result = []
    if direction in [Direction.UP, Direction.DOWN]:
        rows = set([side[1] for side in sides])
        for row in sorted(rows):
            # Get sides with same row
            sides_for_row = [side for side in sides if side[1] == row]
            # Sort by column
            sides_for_row.sort(key=lambda side: side[2])
            result.append(sides_for_row[0])
            for i in range(len(sides_for_row) - 1):
                if sides_for_row[i+1][2] - sides_for_row[i][2] > 1:
                    # same direction and not next to each other -> separate sides
                    result.append(sides_for_row[i+1])
    else:
        columns = set([side[2] for side in sides])
        for col in sorted(columns):
            # Get sides with same column
            sides_for_col = [side for side in sides if side[2] == col]
            # Sort by row
            sides_for_col.sort(key=lambda side: side[1])
            result.append(sides_for_col[0])
            for i in range(len(sides_for_col) - 1):
                if sides_for_col[i + 1][1] - sides_for_col[i][1] > 1:
                    # same direction and not next to each other -> separate sides
                    result.append(sides_for_col[i + 1])

    return result


def reduce_region_sides():
    global region_sides
    reduced_sides = {}
    for region, sides in region_sides.items():
        result = []
        for direction in Direction:
            direction_sides = [side for side in sides if side[0] == direction]
            result += reduce_sides_for_direction(direction, direction_sides)
        print(f"region: {region}, reduced sides: {result}")
        reduced_sides[region] = result

    return reduced_sides


def fencing_price_1():
    result = 0
    for reg_id in region_areas.keys():
        result += region_areas[reg_id] * region_perimeters[reg_id]

    return result


def fencing_price_2():
    global region_sides
    result = 0
    region_sides = reduce_region_sides()
    for reg_id in region_areas.keys():
        result += region_areas[reg_id] * len(region_sides[reg_id])

    return result


# contains garden plots that are already part of a region
plots_in_region = set()
# dictionary region_id: area
region_areas = {}
# dictionary region_id: perimeter (puzzle 1)
region_perimeters = {}
# dictionary region_id: sides (list of all sides, but filtered later) (puzzle 2)
region_sides = {}

farm = parse_farm("day12.txt")
n = len(farm)
m = len(farm[0])

get_farm_regions()
print(fencing_price_2())


