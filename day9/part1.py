#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress, tee
import math

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

def difference(measurement_values: List[int]):
    x, y = tee(measurement_values)
    next(y, None)
    diff = [b-a for a,b in zip(x,y)]
    return diff

values = []

for line in file_input:
    values.append(list(map(lambda x: int(x), line.split(" "))))

values_sum = 0
for value in values:
    differences = [value]
    series_diff = value
    while series_diff.count(0) != len(series_diff):
        series_diff = difference(series_diff)
        # print("iter: " + str(series_diff) )
        differences.append(series_diff)
    trend = 0
    for idx in range(1, len(differences)):
        trend = differences[-idx-1][-1] + trend
        # print("trend " + str(trend))
    values_sum += trend
print("sum: " + str(values_sum))

file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
