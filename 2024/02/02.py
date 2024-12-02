def parseList(input):
    reports = []
    with open(input, "r") as file:
        for line in file.readlines():
            reports.append(list(map(int, line.split())))
    return reports


def checkReport(report):
    increasing = False
    decreasing = False
    unsafe = False
    for i in range(len(report) - 1):
        if abs(report[i] - report[i + 1]) > 3 or report[i] == report[i + 1]:
            unsafe = True
        elif report[i] > report[i + 1]:
            increasing = True
        else:
            decreasing = True
    return not unsafe and (increasing != decreasing)


def day2_first(input):
    reports = parseList(input)
    safeReports = 0
    for report in reports:
        if checkReport(report):
            safeReports += 1
    return safeReports


def day2_second(input):
    reports = parseList(input)
    safeReports = 0
    for report in reports:
        if checkReport(report):
            safeReports += 1
        else:
            for i in range(len(report)):
                smallReport = report[:]
                smallReport.pop(i)
                if checkReport(smallReport):
                    safeReports += 1
                    break
    return safeReports


print(day2_second('day02.txt'))
