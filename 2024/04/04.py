from itertools import product


def day04_first(input):
    file = open(input, "r")
    rows = file.readlines()

    n = len(rows)
    m = len(rows[0]) - 1

    # directions: where to go next in the grid
    directions = [elm for elm in product(range(-1, 2), range(-1, 2)) if elm != (0,0)]

    result = 0

    for rowIndex in range(n):
        for colIndex in range(m):
            for direction in directions:
                # print("New direction:" + str(direction))
                dx, dy = direction
                has_xmas = True
                for offset, c in enumerate("XMAS"):
                    curRow = rowIndex + offset * dx
                    curCol = colIndex + offset * dy
                    # print("Row: " + str(curRow) + " Col: " + str(curCol))
                    if not (0 <= curRow < n and 0 <= curCol < m):
                        has_xmas = False
                    elif rows[curRow][curCol] != c:
                        has_xmas = False
                result += has_xmas

    return result


def day04_second(input):
    file = open(input, "r")
    rows = file.readlines()

    n = len(rows)
    m = len(rows[0]) - 1
    result = 0

    for row in range(n):
        for col in range(m):
            allowed = ["MAS", "SAM"]
            first = ""
            second = ""
            for offset in range(3):
                rowIdx, rowIdx2, colIdx = row + offset, row + 2 - offset, col + offset
                if 0 <= rowIdx < n and 0 <= rowIdx2 < n and 0 <= colIdx < m:
                    first += rows[rowIdx][colIdx]
                    second += rows[rowIdx2][colIdx]
            result += first in allowed and second in allowed

    return result


print(day04_first("day04.txt"))
print(day04_second("day04.txt"))
