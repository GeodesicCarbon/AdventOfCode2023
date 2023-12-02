#!/bin/python3
from typing import Dict

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

max_cubes = {
    "red":12,
    "green": 13,
    "blue": 14
}

def cube_max_test(test: Dict[str, int]):
    for k,v in test.items():
        if max_cubes[k] < v:
            return False;
    return True

def lineparser(line: str):
    (pre_record, records) = line.split(sep=": ")
    game_num = int(pre_record[5:])
    record_arr = records.split(sep="; ")
    for record in record_arr:
        cubes = {}
        cube_record = record.split(sep=", ")
        for cube in cube_record:
            num, color = cube.strip().split(" ")
            cubes[color] = int(num)
        if not cube_max_test(cubes):
            return 0
    return game_num

game_sum = 0
for line in file_input:
    game_sum += lineparser(line)
print(game_sum)
