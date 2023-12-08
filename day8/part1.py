#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress
import math

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

directions = list(map(lambda x: 0 if x == "L" else 1, ([*file_input.readline().strip()])))
file_input.readline()
# print(directions)

direction_count = len(directions)
graph = {}

for line in file_input:
    graph[line[:3]] = (line[7:10], line[12:15])

steps = 0
current = "AAA"
while current != "ZZZ":
    # print(graph[current])
    # print(directions[steps%direction_count])
    current = graph[current][directions[steps%direction_count]]
    steps+= 1

print (steps)
file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
