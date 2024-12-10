from itertools import repeat


def parse_input(input):
    current_disk_map = []
    current_id = 0
    for i, x in enumerate(open(input, "r").read()):
        if i % 2 == 0:
            # equal index
            current_disk_map += repeat(current_id, int(x))
            current_id += 1
        else:
            current_disk_map += repeat(".", int(x))

    return current_disk_map, current_id - 1


# puzzle 1
def compact_file(current_disk_map):
    for i, file_id in reversed(list(enumerate(current_disk_map))):
        # reverse loop to bring files to front

        if "." not in current_disk_map:
            return current_disk_map

        if file_id != ".":
            free_idx = current_disk_map.index(".")
            current_disk_map[free_idx] = file_id

        current_disk_map.pop(i)

    return current_disk_map


# puzzle 2

def find_segment_space(current_disk_map, last_index, length):
    space = 0
    for i in range(last_index):
        if current_disk_map[i] != ".":
            space = 0
            continue

        space += 1
        if space == length:
            return i - length + 1

    return -1


def compact_file_segments(current_disk_map, id_max):
    # last index with a file_id

    for file_id in reversed(range(max_id + 1)):
        current_index = (len(current_disk_map) - 1) - list(reversed(current_disk_map)).index(file_id)
        file_length = current_disk_map.count(file_id)
        start_index = find_segment_space(current_disk_map, current_index, file_length)
        if start_index != -1:
            for i in range(file_length):
                current_disk_map[start_index + i] = file_id
                current_disk_map[current_index - i] = "."

    return current_disk_map


def checksum(compact_disk_map):
    result = 0
    for i, x in enumerate(compact_disk_map):
        if x != ".":
            result += i*x

    return result


disk_map, max_id = parse_input("day09.txt")
# disk_map = compact_file(disk_map)
disk_map = compact_file_segments(disk_map, max_id)
print(disk_map)
print(checksum(disk_map))
