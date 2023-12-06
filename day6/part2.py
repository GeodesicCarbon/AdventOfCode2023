#!/usr/bin/python3
import re
from typing import List
from itertools import cycle, compress
import math



file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

line = file_input.readline().strip()
race_time = int("".join(re.findall("\d+",line)))


line = file_input.readline().strip()
record_dist = int("".join(re.findall("\d+",line)))

print("race_dist: " + str(race_time))
print("record_dist: " + str(record_dist))

def get_winning_range(time: int, dist: int):
    # a = -1, b = time c = -dist
    top_val = (-time + math.sqrt(time**2 - 4*dist))/ -2
    bot_val = (-time - math.sqrt(time**2 - 4*dist))/ -2
    return (math.ceil(bot_val) - math.ceil(top_val))

get_winning_range(race_time, record_dist)


wins = get_winning_range(race_time, record_dist)
print("wins: " + str(wins))




# print(file_input.readline())
file_input.close()
