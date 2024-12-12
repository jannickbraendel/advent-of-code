
def parse_input(file):
    result = list(map(int, open(file, "r").read().split()))
    return result


def increment_stone(dictionary, stone, incr):
    dictionary[stone] = dictionary.get(stone, 0) + incr
    return dictionary


def decrement_stone(dictionary, stone, decr):
    dictionary[stone] -= decr
    if dictionary[stone] <= 0:
        del dictionary[stone]

    return dictionary


def update_stones():
    global stone_count
    new_dict = dict(stone_count)
    for stone, count in stone_count.items():
        length = len(str(stone))
        if stone == 0:
            new_dict = decrement_stone(new_dict, stone, count)
            new_dict = increment_stone(new_dict, 1, count)
        elif length % 2 == 0:
            half = int(length/2)
            first = str(stone)[:half]
            second = str(stone)[half:]
            new_dict = decrement_stone(new_dict, stone, count)
            new_dict = increment_stone(new_dict, int(first), count)
            new_dict = increment_stone(new_dict, int(second), count)
        else:
            new_dict = decrement_stone(new_dict, stone, count)
            new_dict = increment_stone(new_dict, stone * 2024, count)

    stone_count = new_dict


def count_stones():
    result = 0
    for stone in stone_count.keys():
        result += stone_count[stone]

    return result


def evolve_stones(file):
    stones = parse_input(file)
    # init dictionary
    for stone in stones:
        stone_count[stone] = 1

    for i in range(75):
        print(str(i))
        # update stone_count dictionary
        update_stones()

    return count_stones()


# dictionary for counting stones with the same number
stone_count = {}
print(evolve_stones("day11.txt"))
print(stone_count)
