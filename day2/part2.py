#!/bin/python3
from typing import Dict

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

max_cubes = {
    "red": 0,
    "green": 0,
    "blue": 0
}

def cube_max_count(test: Dict[str, int], game_max_cubes: Dict[str, int]):
    for k,v in test.items():
        if game_max_cubes[k] < v:
            game_max_cubes[k] = v;
    return game_max_cubes

def lineparser(line: str):
    game_max_cubes = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    pre_record, records = line.split(sep=": ")
    game_num = int(pre_record[5:])
    record_arr = records.split(sep="; ")
    for record in record_arr:
        cubes = {}
        cube_record = record.split(sep=", ")
        for cube in cube_record:
            num, color = cube.strip().split(" ")
            cubes[color] = int(num)
        game_max_cubes = cube_max_count(cubes, game_max_cubes)
    return game_max_cubes["red"] * game_max_cubes["green"] * game_max_cubes["blue"]


power_sum = 0
for line in file_input:
    power_set = lineparser(line)
    # print(power_set)
    power_sum += power_set
print(power_sum)
