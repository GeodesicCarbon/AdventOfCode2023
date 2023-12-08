#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress
import math

file_input = open("input.txt", "r")
# file_input = open("example3.txt", "r")

directions = list(map(lambda x: 0 if x == "L" else 1, ([*file_input.readline().strip()])))
file_input.readline()
# print(directions)


direction_count = len(directions)
graph = {}

for line in file_input:
    graph[line[:3]] = (line[7:10], line[12:15])

starts = list(filter(lambda x: x[2] == "A", graph.keys()))
ends = list(filter(lambda x: x[2] == "Z", graph.keys()))
print(list(filter(lambda x: x[2] == "Z", graph.keys())))
midpoints = []
steps = 0
for start in starts:
    steps = 0
    current = start
    while current[2] != "Z":
        # print(directions[steps%direction_count])
        current = graph[current][directions[steps%direction_count]]
        steps+= 1
        if steps%100000 == 0:
            print("steps: " + str(steps) + " " + str(current))
    print(start+ " dist : " +str(steps) + " dest: " + current)
    midpoints.append((current, steps))

for midpoint in midpoints:
    steps = midpoint[1]
    current = graph[midpoint[0]][directions[steps%direction_count]]
    steps += 1
    while current[2] != "Z":
        # print(directions[steps%direction_count])
        current = graph[current][directions[steps%direction_count]]
        steps+= 1
        if steps%1000000 == 0:
            print("steps: " + str(steps) + " " + str(current))
    print(midpoint[0]+ " dist : " +str(steps) + " dest: " + current)

# print (steps)
file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
