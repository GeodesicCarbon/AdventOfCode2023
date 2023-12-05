#!/usr/bin/python3
import re
from typing import List



file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

seeds = []



seed_to_soil_map = []
soil_to_fertilizer_map = []
fertilizer_to_water_map = []
water_to_light_map = []
light_to_temperature_map = []
temperature_to_humidity_map = []
humidity_to_location_map = []

almanac_maps = [
    seed_to_soil_map,
    soil_to_fertilizer_map,
    fertilizer_to_water_map,
    water_to_light_map,
    light_to_temperature_map,
    temperature_to_humidity_map,
    humidity_to_location_map
]

def map_string_line(line: str, almanac_map):
    dest, src, map_range = list(map(int, (line.split(" "))))
    almanac_map.append(((src, src + map_range), (dest)))

def map_seeds(seeds: List[int], almanac_map):
    new_seeds = []
    for seed in seeds:
        new_seed_val = seed
        for ranges in almanac_map:
            source_range, dest = ranges
            src_min, src_max = source_range
            if seed >= src_min and seed < src_max:
                diff = seed - src_min
                new_seed_val = dest + diff
        new_seeds.append(new_seed_val)
    return new_seeds


seeds = list(map(int, file_input.readline().strip().split(": ")[1].split(" ")))

for almanac_map in almanac_maps:

    file_input.readlines(2) # skip non-data

    for line in file_input:
        if line == "\n":
            break;
        map_string_line(line, almanac_map)
    # print(almanac_map)
    seeds = map_seeds(seeds, almanac_map)
    # print(seeds)

# print(file_input.readline())
seeds.sort()
print(seeds[0])
file_input.close()
