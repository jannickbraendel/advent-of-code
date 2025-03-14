
def parse_codes(file):
    with open(file, 'r') as file:
        codes = [line.strip() for line in file.readlines()]
        return codes


def find_directions(dx, dy):
    res = ''
    if dx < 0:
        x = '<'
    else:
        x = '>'

    res += x * abs(dx)

    if dy < 0:
        y = 'v'
    else:
        y = '^'

    res += y * abs(dy)

    return res


def numerical_sequence(code):
    x, y = num_keypad_positions['A']
    result = ''

    for i in code:
        key_x, key_y = num_keypad_positions[i][0], num_keypad_positions[i][1]

        diff_x, diff_y = key_x - x, key_y - y
        result += find_directions(diff_x, diff_y)
        result += 'A'
        x, y = key_x, key_y

    return result


def dir_sequence(num_sequence):
    x, y = dir_keypad_positions['A']
    result = ''

    for i in num_sequence:
        key_x, key_y = dir_keypad_positions[i][0], dir_keypad_positions[i][1]

        diff_x, diff_y = key_x - x, key_y - y
        result += find_directions(diff_x, diff_y)
        result += 'A'
        x, y = key_x, key_y

    return result


num_keypad_positions = {
    '0': (1, 0), 'A': (2, 0),
    '1': (0, 1), '2': (1, 1), '3': (2, 1),
    '4': (0, 2), '5': (1, 2), '6': (2, 2),
    '7': (0, 3), '8': (1, 3), '9': (2, 3)
}

dir_keypad_positions = {
    '<': (0, 0), 'v': (1, 0), '>': (2, 0),
    '^': (1, 1), 'A': (2, 1)
}

codes = parse_codes('day21-small.txt')
directional_sequences = []
complexity = 0

for code in codes:
    num_sequence = numerical_sequence(code)
    dir_seq = dir_sequence(dir_sequence(num_sequence))
    directional_sequences.append(dir_seq)

    complexity += len(dir_seq) * int(code.rstrip('A'))

print(f'Sequences: \n{directional_sequences} \n Complexity: {complexity}')


