#!/usr/bin/python3
import re
from typing import List
from itertools import cycle, compress



file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

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

# def map_string_line(line: str, almanac_map):
#     dest, src, map_range = list(map(int, (line.split(" "))))
#     almanac_map.append(((src, src + map_range), (dest)))

def map_string_line(line: str, almanac_map):
    dest, src, map_range = list(map(int, (line.split(" "))))
    almanac_map.append(((src, map_range), dest))


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

def map_candiate(candidate: int, almanac_map):
    for ranges in almanac_map:
        source_range, dest = ranges
        src_min, map_range = source_range
        if candidate >= dest and candidate < dest + map_range:
            # print ("cand : " + str(candidate) + " dest: " + str(dest))
            diff = candidate - dest
            # print ("found map, diff: " + str(diff) + str(almanac_map))
            return src_min + diff
    return candidate

def test_is_seed(canditdate:int, seeds):
    for ranges in seeds:
        if canditdate >= ranges[0] and canditdate < ranges[0] + ranges[1]:
            return True
    return False

def get_seeds(seed_range_list: List[int]):
    pairs = list(map(list, zip(compress(seed_range_list, cycle([1, 0])), compress(seed_range_list, cycle([0, 1])))))
    seed_list = []
    for seed_range in pairs:
        # print([*range(seed_range[0], seed_range[0] + seed_range[1])])
        # seed_list += [*range(seed_range[0], seed_range[0] + seed_range[1])]
        seed_list.append(seed_range)
    return seed_list

seeds = get_seeds(list(map(int, file_input.readline().strip().split(": ")[1].split(" "))))
print("seed ranges loaded")

for almanac_map in almanac_maps:

    file_input.readlines(2) # skip non-data

    for line in file_input:
        if line == "\n":
            break;
        map_string_line(line, almanac_map)
    # print(almanac_map)
    # seeds = map_seeds(seeds, almanac_map)
    # print(seeds)
    print("Map done")

print("Starting inverse search")
almanac_maps.reverse()

for candidate in range(0, 84470623):
    if candidate % 100000 == 0:
        print("testing candidate : " +  str(candidate))
    candidate_temp = candidate
    candidate_temp_list = [candidate]
    for almanac_map in almanac_maps:
        # if candidate == 46:
        #     print("cand_temp: " + str(candidate_temp))
        candidate_temp = map_candiate(candidate_temp, almanac_map)
        candidate_temp_list.append(candidate_temp)
    if test_is_seed(candidate_temp, seeds):
        print(candidate_temp_list)
        print(candidate)
        break


# print(file_input.readline())
file_input.close()
