import re
import time

def day03_first(input):
    with open(input, "r") as file:
        pattern = r"mul\(\d{1,3},\s*\d{1,3}\)"
        mults = re.findall(pattern, file.read())

        result = 0
        for mult in mults:
            numbers = list(map(int, re.findall(r"\d+", mult)))
            result += numbers[0] * numbers[1]

        return result


def day03_second(input):
    file = open(input, "r")
    # get relevant strings to check
    instructions = ""
    for instr in file.read().split("do()"):
        instructions += instr.split("don't()")[0]

    # find mult patterns
    pattern = r"mul\(\d{1,3},\s*\d{1,3}\)"
    mults = re.findall(pattern, instructions)

    result = 0
    for mult in mults:
        numbers = list(map(int, re.findall(r"\d+", mult)))
        result += numbers[0] * numbers[1]

    return result


start_time = time.perf_counter()  # Record the start time

print(day03_second("day03.txt"))

end_time = time.perf_counter()  # Record the end time
runtime = end_time - start_time
print(f"Runtime: {runtime:.4f} seconds")



