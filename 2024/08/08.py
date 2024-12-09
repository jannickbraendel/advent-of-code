from itertools import combinations


def parse_input(input):
    grid = []
    with open(input, "r") as file:
        for line in file.readlines():
            grid.append(list(line.rstrip("\n")))

    n = len(grid)
    m = len(grid[0])

    frequencies = []
    antenna_positions = []

    for i in range(n):
        for j in range(m):
            c = grid[i][j]
            if c == ".":
                continue
            else:
                if c not in frequencies:
                    frequencies.append(c)
                    antenna_positions.append([(i, j)])
                else:
                    antenna_positions[frequencies.index(c)].append((i, j))
    return antenna_positions, n, m


# for puzzle 1
def get_antinodes_for_antenna_1(antennas, n, m):
    if len(antennas) <= 1:
        return []
    antinodes = set()
    antenna_pairs = list(combinations(antennas, 2))

    for ant1, ant2 in antenna_pairs:
        d_x = ant2[0] - ant1[0]
        d_y = ant2[1] - ant1[1]

        # add 2 antinodes in line with antennas
        x_1 = ant1[0] - d_x
        y_1 = ant1[1] - d_y

        if 0 <= x_1 < n and 0 <= y_1 < m:
            antinodes.add((x_1, y_1))

        x_2 = ant2[0] + d_x
        y_2 = ant2[1] + d_y

        if 0 <= x_2 < n and 0 <= y_2 < m:
            antinodes.add((x_2, y_2))

    return antinodes


# for puzzle 2
def get_antinodes_for_antenna_2(antennas, n, m):
    if len(antennas) <= 1:
        return 0
    antinodes = set()
    antenna_pairs = list(combinations(antennas, 2))

    for ant1, ant2 in antenna_pairs:
        antinodes.add(ant1)
        antinodes.add(ant2)
        d_x = ant2[0] - ant1[0]
        d_y = ant2[1] - ant1[1]

        x_1 = ant1[0] - d_x
        y_1 = ant1[1] - d_y
        while 0 <= x_1 < n and 0 <= y_1 < m:
            antinodes.add((x_1, y_1))
            x_1 -= d_x
            y_1 -= d_y

        x_2 = ant2[0] + d_x
        y_2 = ant2[1] + d_y
        while 0 <= x_2 < n and 0 <= y_2 < m:
            antinodes.add((x_2, y_2))
            x_2 += d_x
            y_2 += d_y

    return antinodes


def count_antinodes(input):
    antenna_positions, n, m = parse_input(input)
    antinodes = set()

    for antennas in antenna_positions:
        current_nodes = get_antinodes_for_antenna_2(antennas, n, m)
        antinodes = antinodes.union(current_nodes)

    return len(antinodes)


print(count_antinodes("day08.txt"))


