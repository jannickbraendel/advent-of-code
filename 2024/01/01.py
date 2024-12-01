
def parseLists(input):
    list1 = []
    list2 = []
    with open(input, "r") as file:
        for line in file.readlines():
            line = line.split()
            list1.append(int(line[0]))
            list2.append(int(line[1]))
    return list1, list2

def day1_first(input):
    list1, list2 = parseLists(input)
    list1.sort()
    list2.sort()
    result = 0
    for x, y in zip(list1, list2):
        result += abs(x-y)

    return result

def day1_second(input):
    list1, list2 = parseLists(input)
    similarity_score = 0
    for x in list1:
        similarity_score += x * list2.count(x)
    return similarity_score


print('Puzzle 1: ' + str(day1_first('input.txt')))
print('Puzzle 2: ' + str(day1_second('input.txt')))
