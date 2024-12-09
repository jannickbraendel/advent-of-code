import itertools
from itertools import combinations, repeat

from bitarray import bitarray
from bitarray.util import ba2int, int2ba


def parse_input(input):
    results = []
    numbers = []
    with open(input, "r") as file:
        for line in file.readlines():
            results.append(int(line.split(":")[0]))
            numbers.append(list(map(int, line.split(":")[1].rstrip("\n").split())))

    return results, numbers


def add_to_bitarray(ba, to_add):
    x = ba2int(ba)
    x += to_add
    return int2ba(x, length=len(ba))


# for 1st puzzle
def check_equation_1(result, numbers):
    n = len(numbers)
    # bitarray that checks which operators to use (0: +, 1: *)
    operators = bitarray(n-1)

    for _ in range(2 ** (n-1)):
        res = numbers[0]
        for i in range(1, n):
            if operators[i-1] == 0:
                res += numbers[i]
            else:
                res *= numbers[i]
        # print(f"numbers: {numbers}, wanted: {result}, calculated {res} with {operators}")
        if res == result:
            return result
        try:
            operators = add_to_bitarray(operators, 1)
        except OverflowError:
            return 0

    return 0


# for 2nd puzzle (with || operator)
def check_equation_2(result, numbers):
    n = len(numbers)
    # array of combinations of operators (0: +, 1: *, 2: ||)
    operator_combinations = list(itertools.product([0, 1, 2], repeat=n-1))

    for operators in operator_combinations:
        res = numbers[0]
        for i in range(1, n):
            if operators[i - 1] == 0:
                res += numbers[i]
            elif operators[i - 1] == 1:
                res *= numbers[i]
            else:
                s = str(res) + str(numbers[i])
                res = int(s)

        # print(f"numbers: {numbers}, wanted: {result}, calculated {res} with {operators}")
        if res == result:
            return result

    return 0


def check_equations(input):
    results, numbers = parse_input(input)
    res = 0
    for result, nums in zip(results, numbers):
        res += check_equation_2(result, nums)

    return res


print(check_equations("day07.txt"))
