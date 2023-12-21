#!/usr/bin/python3
import regex as re
from typing import List, Tuple
from itertools import cycle, compress, tee, groupby
from functools import reduce
import math
import sys
import numpy as np
from copy import deepcopy

class Coord:
    def __init__(self, x, y, shape='', charmap=None):
        self.x = x
        self.y = y
        if charmap is not None:
            # print("charmap: " + str(charmap[0]))
            self.charmap = charmap
        else:
            self.charmap = None
        if not shape:
            self.shape = self.charmap[y][x]
        else:
            self.shape = shape
    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + ": " + str(self.shape) +")"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        elif self.y == other.y and self.x < other.x:
            return True
        else:
            return False
    def __hash__(self):
        return self.x + self.y*1000000


class Coords:
    def __init__(self, width, height, charmap):
        self.width = width
        self.height = height
        self.charmap = charmap
        self.area = width * height
        # print("-- coord w, h: " + str(width) +  " " + str(height))

    def make_coord(self, pos: Tuple[int, int], shape='', charmap=None):
        # print("    " + str(pos[0]) + ":" + str(pos[1]) + "max: " + str(self.width) + " " + str(self.height))
        if charmap is None:
            charmap = self.charmap
        if pos[0] < 0 or pos[0] >= self.width:
            # print("    " + str(pos[0]) + " too wide")
            return
        elif pos[1] < 0 or pos[1] >= self.height:
            # print("    " + str(pos[1]) + " too tall")
            return
        else:
            return Coord(pos[0], pos[1], shape, charmap)

    def get_cardinal_neighbours(self, origin: Coord, filterNone=False):
        coord_list = [
            self.make_coord((origin.x - 1, origin.y), charmap=self.charmap),
            self.make_coord((origin.x + 1, origin.y), charmap=self.charmap),
            self.make_coord((origin.x, origin.y - 1), charmap=self.charmap),
            self.make_coord((origin.x, origin.y + 1), charmap=self.charmap)
        ]
        if filterNone:
            return list(filter(lambda x: x, coord_list))
        else:
            return coord_list

    def get_all_neightbours(self, origin: Coord, filterNone=True):
        coord_list = [
            self.make_coord((origin.x - 1, origin.y), charmap=flood_map),
            self.make_coord((origin.x - 1, origin.y-1), charmap=flood_map),
            self.make_coord((origin.x - 1, origin.y+1), charmap=flood_map),
            self.make_coord((origin.x + 1, origin.y), charmap=flood_map),
            self.make_coord((origin.x + 1, origin.y-1), charmap=flood_map),
            self.make_coord((origin.x + 1, origin.y+1), charmap=flood_map),
            self.make_coord((origin.x, origin.y - 1), charmap=flood_map),
            self.make_coord((origin.x, origin.y + 1), charmap=flood_map)
        ]
        if filterNone:
            return list(filter(lambda x: x, coord_list))
        else:
            return coord_list

def print_charmap(charmap):
    for line in charmap:
        print("".join(line))

def pause_and_print():
    # print("--")
    # beam_charmap = [[*line] for line in mirror_charmap]
    # for key in beam_hashmap.keys():
    #     beam_charmap[key[1]][key[0]] = key[2]
    # print_charmap(beam_charmap)
    # input()
    return

def move_right(coord:Coord):
    if not coord:
        return
    dirshape = ">"
    # if (coord.x, coord.y, dirshape) in beam_hashmap:
    #     print("loop detected: " + str(next_coord))
    #     return
    current_x = coord.x
    current_y = coord.y
    next_coord = mirror_coords.make_coord((current_x, current_y))
    while next_coord:
    # while next_coord := mirror_coords.make_coord((current_x + 1, current_y)):
        if (next_coord.x, next_coord.y, dirshape) in beam_hashmap:
            # print("loop detected: " + str(next_coord))
            return
        elif next_coord.shape == ".":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "/":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_up(mirror_coords.make_coord((current_x, current_y - 1)))
            return
        elif next_coord.shape == "\\":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_down(mirror_coords.make_coord((current_x, current_y + 1)))
            return
        elif next_coord.shape == "|":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            for dir in map_connected_tiles(next_coord):
                if dir.y > current_y:
                    move_down(dir)
                elif dir.y < current_y:
                    move_up(dir)
            return
        elif next_coord.shape == "-":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        current_x = next_coord.x +1
        next_coord = mirror_coords.make_coord((current_x, current_y))
    return


def move_left(coord:Coord):
    if not coord:
        return
    dirshape = "<"
    # if (coord.x, coord.y, dirshape) in beam_hashmap:
    #     print("loop detected: " + str(next_coord))
    #     return
    current_x = coord.x
    current_y = coord.y
    next_coord = mirror_coords.make_coord((current_x, current_y))
    while next_coord:
    # while next_coord := mirror_coords.make_coord((current_x - 1, current_y)):
        if (next_coord.x, next_coord.y, dirshape) in beam_hashmap:
            # print("loop detected: " + str(next_coord))
            return
        elif next_coord.shape == ".":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "/":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_down(mirror_coords.make_coord((current_x, current_y + 1)))
            return
        elif next_coord.shape == "\\":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_up(mirror_coords.make_coord((current_x, current_y - 1)))
            return
        elif next_coord.shape == "|":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            for dir in map_connected_tiles(next_coord):
                if dir.y > current_y:
                    move_down(dir)
                elif dir.y < current_y:
                    move_up(dir)
            return
        elif next_coord.shape == "-":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        current_x = next_coord.x - 1
        next_coord = mirror_coords.make_coord((current_x, current_y))
    return

def move_up(coord:Coord):
    if not coord:
        return
    dirshape = "^"
    # if (coord.x, coord.y, dirshape) in beam_hashmap:
    #     print("loop detected: " + str(next_coord))
    #     return
    current_x = coord.x
    current_y = coord.y
    next_coord = mirror_coords.make_coord((current_x, current_y))
    while next_coord:
    # while next_coord := mirror_coords.make_coord((current_x, current_y - 1)):
        if (next_coord.x, next_coord.y, dirshape) in beam_hashmap:
            # print("loop detected: ^ " + str(next_coord))
            return
        elif next_coord.shape == ".":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "/":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_right(mirror_coords.make_coord((current_x + 1, current_y)))
            return
        elif next_coord.shape == "\\":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_left(mirror_coords.make_coord((current_x - 1, current_y)))
            return
        elif next_coord.shape == "|":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "-":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            for dir in map_connected_tiles(next_coord):
                if dir.x > current_x:
                    move_right(dir)
                elif dir.x < current_x:
                    move_left(dir)
            return
        current_y = next_coord.y - 1
        next_coord = mirror_coords.make_coord((current_x, current_y))
    return

def move_down(coord:Coord):
    if not coord:
        return
    dirshape = "v"
    # if (coord.x, coord.y, dirshape) in beam_hashmap:
    #     print("loop detected: " + str(next_coord))
    #     return
    current_x = coord.x
    current_y = coord.y
    next_coord = mirror_coords.make_coord((current_x, current_y))
    while next_coord:
    # while next_coord := mirror_coords.make_coord((current_x, current_y + 1)):
        if (next_coord.x, next_coord.y, dirshape) in beam_hashmap:
            # print("loop detected: " + str(next_coord))
            return
        elif next_coord.shape == ".":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "/":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_left(mirror_coords.make_coord((current_x - 1, current_y)))
            return
        elif next_coord.shape == "\\":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            move_right(mirror_coords.make_coord((current_x + 1, current_y)))
            return
        elif next_coord.shape == "|":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
        elif next_coord.shape == "-":
            beam_hashmap[next_coord.x, next_coord.y, dirshape] = 1
            pause_and_print()
            for dir in map_connected_tiles(next_coord):
                if dir.x > current_x:
                    move_right(dir)
                elif dir.x < current_x:
                    move_left(dir)
            return
        current_y = next_coord.y + 1
        next_coord = mirror_coords.make_coord((current_x, current_y))
    return

def map_connected_tiles(tile: Coord) -> List[Coord]:
    if tile.shape == "|":
        return mirror_coords.get_cardinal_neighbours(tile, True)[-2:]
    elif tile.shape == "-":
        return mirror_coords.get_cardinal_neighbours(tile, True)[:2]
    # elif tile.shape == "L":
    #     # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1:3]))))
    #     return mirror_coords.get_cardinal_neighbours(tile)[1:3]
    # elif tile.shape == "J":
    #     # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[0::2]))))
    #     return mirror_coords.get_cardinal_neighbours(tile)[0::2]
    # elif tile.shape == "7":
    #     return mirror_coords.get_cardinal_neighbours(tile)[0::3]
    # elif tile.shape == "F":
    #     # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1::2]))))
    #     return mirror_coords.get_cardinal_neighbours(tile)[1::2]
    return []

mirror_charmap =[]
energized_tiles_list = []
file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")

for line in file_input:
    mirror_charmap.append([*line.strip()])

mirror_coords = Coords(len(mirror_charmap[0]), len(mirror_charmap),  mirror_charmap)
for x_start in range(mirror_coords.width):
    beam_hashmap = {}
    start_tile = mirror_coords.make_coord((x_start,0))
    move_down(start_tile)

    # print(beam_hashmap)
    energized_tiles_list.append(len(set(map(lambda x: (x[0], x[1]), beam_hashmap.keys()))))

    beam_hashmap = {}
    start_tile = mirror_coords.make_coord((x_start,mirror_coords.height - 1))
    move_up(start_tile)

    # print(beam_hashmap)
    energized_tiles_list.append(len(set(map(lambda x: (x[0], x[1]), beam_hashmap.keys()))))

for y_start in range(mirror_coords.height):
    beam_hashmap = {}
    start_tile = mirror_coords.make_coord((0,y_start))
    move_right(start_tile)

    # print(beam_hashmap)
    energized_tiles_list.append(len(set(map(lambda x: (x[0], x[1]), beam_hashmap.keys()))))

    beam_hashmap = {}
    start_tile = mirror_coords.make_coord((mirror_coords.width - 1, y_start))
    move_left(start_tile)

    # print(beam_hashmap)
    energized_tiles_list.append(len(set(map(lambda x: (x[0], x[1]), beam_hashmap.keys()))))

# beam_charmap = [[*line] for line in mirror_charmap]
# for key in beam_hashmap.keys():
#     # if key[1] == 0:
#     #     print(str(key[0]) + " " + str(key[2]))
#     beam_charmap[key[1]][key[0]] = key[2]

# print_charmap(beam_charmap)
# print("28, 0, > " + str(beam_hashmap.get((28, 0, ">"))))
# print("28, 0, < " + str(beam_hashmap.get((28, 0, "<"))))
# print("28, 0, ^ " + str(beam_hashmap.get((28, 0, "^"))))
# print("28, 0, v " + str(beam_hashmap.get((28, 0, "v"))))

print("energized tiles: " + str(max(energized_tiles_list)))
# [(r.start(0), row) for r in re.finditer("\#", line)]

file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()

# def find_submatches(match_string: str, broken_springs: List[str]) -> int:
#     subsum = 0
#     if len(broken_springs) == 0:
#         return 1
#     search_string = make_search_string(broken_springs)
#     # print("search string " + search_string)
#     submatches = re.findall(search_string, match_string, overlapped=True)
#     print(match_string + ": " + str(submatches))
#     # submatches = list(set(submatches))
#     # print(match_string + ": " + str(submatches))
#     # print("len of submatches " + str(len(submatches)) + " springs " + str(broken_springs))
#     for submatch in submatches:
#         # print("submatch " + submatch)
#         submatch = "." + submatch + "."
#         subsum += find_submatches(submatch[int(broken_springs[0])+2:], broken_springs[1:])
#     return subsum

# def make_search_string(broken_springs: List[str]) -> str:
#     # search_string = r'(?='
#     # search_string = ""
#     search_string = "[^#]+("
#     for broken_num in broken_springs:
#         search_string += "[#?]{" + broken_num + "}[.?]+"
#     search_string = search_string[:-5]
#     search_string += ")[^#]+"
#     return search_string


# def find_y_mirror(x_rocks: List[List[int]], width: int, ignore_idx:int=-1) -> int:
#     x_list = []
#     for row in x_rocks:
#         x_list.append(list(map(lambda x: x[0],row)))
#     for idx in range(1,width):
#         if idx == ignore_idx:
#             continue
#         row_sum = 0
#         slice_width = min(idx, width - idx)
#         # x_vals = sum(list(map(lambda x: x[0] - idx, x_list[idx-slice_width/2:idx+slice_width/2]))
#         # print("slicing: [" + str(idx -slice_width) + " , " + str(idx + slice_width -1) + "]")
#         for row in x_list:
#             # print("row :" + str(row))
#             # print(list(zip([x for x in row if x in range(idx-slice_width, idx)], negative_mult)))

#             negative_x_vals = list(map(lambda x: x - idx, [x for x in row if x in range(idx-slice_width, idx)]))
#             positive_x_vals = list(map(lambda x: x - idx + 1, [x for x in row if x in range(idx, idx+slice_width)]))
#             # print("split row : " + str(negative_x_vals) +  str(positive_x_vals))
#             # print("testing row: " + str(negative_x_vals + positive_x_vals))
#             row_sum += abs(sum((negative_x_vals + positive_x_vals)))
#         # print("idx " + str(idx) + " row_sum: " + str(row_sum)  + " : ")
#         if row_sum == 0:
#             return idx
#     return 0

# def find_x_mirror(y_rocks: List[List[int]], height: int, ignore_idx:int=-1) -> int:
#     # print("height " + str(height))
#     y_list = []
#     for col in y_rocks:
#         y_list.append(list(map(lambda x: x[1],col)))

#     # print(y_list)
#     for idx in range(1,height):
#         if idx == ignore_idx:
#             continue
#         col_sum = 0
#         slice_width = min(idx, height - idx)
#         # x_vals = sum(list(map(lambda x: x[0] - idx, x_list[idx-slice_width/2:idx+slice_width/2]))
#         # print("slicing: [" + str(idx -slice_width) + " , " + str(idx + slice_width -1) + "]")
#         for col in y_list:
#             # print("row :" + str(row))
#             # print(list(zip([x for x in row if x in range(idx-slice_width, idx)], negative_mult)))

#             negative_y_vals = list(map(lambda y: y - idx, [x for x in col if x in range(idx-slice_width, idx)]))
#             positive_y_vals = list(map(lambda y: y - idx + 1, [x for x in col if x in range(idx, idx+slice_width)]))
#             # print("split row : " + str(negative_x_vals) +  str(positive_x_vals))
#             # print("testing col: " + str(negative_y_vals + positive_y_vals))
#             col_sum += abs(sum((negative_y_vals + positive_y_vals)))
#         # print("idx " + str(idx) + " col_sum: " + str(col_sum)  + " : ")
#         if col_sum == 0:
#             return idx*100
#     return 0

# def smudge(rock_list, position, pattern):
#     width = len(pattern[0])
#     height = len(pattern)
#     if position%100 == 0:
#         idx = position/100
#         slice_range = min(idx, height - idx)
#         possible_smudges = [(x, y) for y in range(height) for x in range(width)]
#         # print(possible_smudges)
#         for smudge in possible_smudges:
#             if smudge in rock_list:
#                 smudged_rock_list = [ x for x in rock_list if x != smudge]
#             else:
#                 smudged_rock_list = rock_list + [smudge]
#             rock_x_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[1], x[0]]), lambda x: x[1])))
#             # print(rock_x_list)
#             # rock_y_list = list(map(lambda x: list(x[1]), rock_list))
#             pattern_sum_x =  find_y_mirror(rock_x_list, len(pattern[0]))
#             if pattern_sum_x:
#                 # print("--- --- --- smudged y_mirror found: " + str(pattern_sum_x))
#                 return pattern_sum_x
#             rock_y_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[0], x[1]]), lambda x: x[0])))
#             pattern_sum_y = find_x_mirror(rock_y_list, len(pattern), idx)
#             if pattern_sum_y == position:
#                 print("!!! SAME MIRROR !!!")
#             if pattern_sum_y:
#                 # print("--- --- ---- smudged x_mirror found: " + str(pattern_sum_y))
#                 return pattern_sum_y
#     else:
#         idx = position
#         slice_range = min(idx, width - idx)
#         possible_smudges = [(x, y) for x in range(width) for y in range(height)]
#         # print(possible_smudges)
#         for smudge in possible_smudges:
#             if smudge in rock_list:
#                 smudged_rock_list = [ x for x in rock_list if x != smudge]
#             else:
#                 smudged_rock_list = rock_list + [smudge]
#             # print(len(smudged_rock_list))
#             rock_x_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[1], x[0]]), lambda x: x[1])))
#             # print(rock_x_list)
#             # rock_y_list = list(map(lambda x: list(x[1]), rock_list))
#             pattern_sum_x =  find_y_mirror(rock_x_list, len(pattern[0]), idx)
#             if pattern_sum_x == position:
#                 print("!!! SAME MIRROR !!!")
#             if pattern_sum_x:
#                 # print("--- --- --- smudged y_mirror found: " + str(pattern_sum_x))
#                 return pattern_sum_x
#             rock_y_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[0], x[1]]), lambda x: x[0])))
#             pattern_sum_y = find_x_mirror(rock_y_list, len(pattern))
#             if pattern_sum_y:
#                 # print("--- --- --- smudged x_mirror found: " + str(pattern_sum_y))
#                 return pattern_sum_y
