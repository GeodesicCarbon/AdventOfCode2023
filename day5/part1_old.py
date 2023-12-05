#!/usr/bin/python3
import re
from collections import defaultdict

class AlmanacMap(defaultdict):
    def __missing__(self, key):
        return self.default_factory(key)


file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

seeds = []



seed_to_soil_map = AlmanacMap(lambda key: key)
soil_to_fertilizer_map = AlmanacMap(lambda key: key)
fertilizer_to_water_map = AlmanacMap(lambda key: key)
water_to_light_map = AlmanacMap(lambda key: key)
light_to_temperature_map = AlmanacMap(lambda key: key)
temperature_to_humidity_map = AlmanacMap(lambda key: key)
humidity_to_location_map = AlmanacMap(lambda key: key)

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
    for i in range(map_range):
        almanac_map[src + i] = dest + i

seeds = list(map(int, file_input.readline().strip().split(": ")[1].split(" ")))

for almanac_map in almanac_maps:

    file_input.readlines(2) # skip non-data

    for line in file_input:
        if line == "\n":
            break;
        map_string_line(line, almanac_map)
    print(almanac_map[0])
    seeds = [almanac_map[seed] for seed in seeds]

# print(file_input.readline())
seeds.sort()
print(seeds[0])
file_input.close()
