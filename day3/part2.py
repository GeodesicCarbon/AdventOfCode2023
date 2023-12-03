#!/bin/python3
import re
import functools

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

symbols_pos = []
gears_adjacent = []
gears_adjacent_count = {}

def find_part(pos: (int, int), number_len: (int)):
    num_x, num_y = pos
    # print("x: " + str(num_x) + " y: " + str(num_y))
    possible_symbol_locations = [(num_x-1, num_y), (num_x-1, num_y - 1), (num_x-1, num_y + 1)]
    for i in range(num_x, num_x + number_len):
        possible_symbol_locations.append((i, num_y + 1))
        possible_symbol_locations.append((i, num_y - 1))
    possible_symbol_locations = possible_symbol_locations + [(num_x + number_len, num_y), (num_x + number_len, num_y - 1), (num_x + number_len, num_y + 1)]
    # print(possible_symbol_locations)
    return list(set(possible_symbol_locations) & set(symbols_pos))

def parse_symbol_pos(line: str, row: int):
    symbol_x = 0
    symbol_y = row
    for char in line:
        if (char == '*'):
            symbols_pos.append((symbol_x, symbol_y))
        symbol_x += 1

part_sum = 0
line_num = 0
for line in file_input:
    parse_symbol_pos(line.strip(), line_num)
    line_num += 1

file_input.seek(0)

part_sum = 0
line_num = 0
for line in file_input:
    numbers = {r.start(0):int(r.group(0)) for r in re.finditer("\d+", line)}
    for number in numbers:
        # print(numbers[number])
        gear_coords = find_part((number, line_num), len(str(numbers[number])))
        for gear_coord in gear_coords:
            gears_adjacent.append((gear_coord, numbers[number]))
    line_num += 1
gear_locations = set(list(map(lambda a : a[0], gears_adjacent)))
for gear_loc in gear_locations:
    # print(list(map(lambda a : a[0], gears_adjacent))[0] == gear_loc)
    if len(list(filter(lambda x: (x[0] == gear_loc[0] and x[1] == gear_loc[1]), list(map(lambda a : a[0], gears_adjacent))))) == 2:
        part1, part2 = list(filter(lambda y : (y[0][0] == gear_loc[0] and y[0][1] == gear_loc[1]), gears_adjacent))
        part_sum += part1[1] * part2[1]
print(part_sum)
file_input.close()
