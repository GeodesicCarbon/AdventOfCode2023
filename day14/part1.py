#!/usr/bin/python3
import regex as re
from typing import List, Tuple
from itertools import cycle, compress, tee, groupby
import math
import sys
import numpy as np
from copy import deepcopy



file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")



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


platform_charmap = []
load_total = 0

for line in file_input:
    platform_charmap.append(line.strip())

print_charmap(platform_charmap)
print("---")
platform_charmap_transposed = list(zip(*platform_charmap))
print_charmap(platform_charmap_transposed)
print("--- Rolling ---")

platform_transposed_width = len(platform_charmap_transposed[0])
platform_transposed_height = len(platform_charmap)
for col in platform_charmap_transposed:
    rock_idx = []
    current_free_idx = -1
    for idx in range(platform_transposed_width):
        if col[idx] == "O" and current_free_idx < 0:
            rock_idx.append(idx)
        elif col[idx] == "O":
            rock_idx.append(current_free_idx)
            current_free_idx += 1
        if col[idx] == "." and current_free_idx < 0:
            current_free_idx = idx
        if col[idx] == "#":
            current_free_idx = -1
    # print("-- rock indexes :" + str(rock_idx))
    loads = list(map(lambda x: platform_transposed_width - x, rock_idx))
    # print("-- loads :" + str(loads) + " total: " + str(sum(loads)))
    load_total += sum(loads)

print(load_total)

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


def find_y_mirror(x_rocks: List[List[int]], width: int, ignore_idx:int=-1) -> int:
    x_list = []
    for row in x_rocks:
        x_list.append(list(map(lambda x: x[0],row)))
    for idx in range(1,width):
        if idx == ignore_idx:
            continue
        row_sum = 0
        slice_width = min(idx, width - idx)
        # x_vals = sum(list(map(lambda x: x[0] - idx, x_list[idx-slice_width/2:idx+slice_width/2]))
        # print("slicing: [" + str(idx -slice_width) + " , " + str(idx + slice_width -1) + "]")
        for row in x_list:
            # print("row :" + str(row))
            # print(list(zip([x for x in row if x in range(idx-slice_width, idx)], negative_mult)))

            negative_x_vals = list(map(lambda x: x - idx, [x for x in row if x in range(idx-slice_width, idx)]))
            positive_x_vals = list(map(lambda x: x - idx + 1, [x for x in row if x in range(idx, idx+slice_width)]))
            # print("split row : " + str(negative_x_vals) +  str(positive_x_vals))
            # print("testing row: " + str(negative_x_vals + positive_x_vals))
            row_sum += abs(sum((negative_x_vals + positive_x_vals)))
        # print("idx " + str(idx) + " row_sum: " + str(row_sum)  + " : ")
        if row_sum == 0:
            return idx
    return 0

def find_x_mirror(y_rocks: List[List[int]], height: int, ignore_idx:int=-1) -> int:
    # print("height " + str(height))
    y_list = []
    for col in y_rocks:
        y_list.append(list(map(lambda x: x[1],col)))

    # print(y_list)
    for idx in range(1,height):
        if idx == ignore_idx:
            continue
        col_sum = 0
        slice_width = min(idx, height - idx)
        # x_vals = sum(list(map(lambda x: x[0] - idx, x_list[idx-slice_width/2:idx+slice_width/2]))
        # print("slicing: [" + str(idx -slice_width) + " , " + str(idx + slice_width -1) + "]")
        for col in y_list:
            # print("row :" + str(row))
            # print(list(zip([x for x in row if x in range(idx-slice_width, idx)], negative_mult)))

            negative_y_vals = list(map(lambda y: y - idx, [x for x in col if x in range(idx-slice_width, idx)]))
            positive_y_vals = list(map(lambda y: y - idx + 1, [x for x in col if x in range(idx, idx+slice_width)]))
            # print("split row : " + str(negative_x_vals) +  str(positive_x_vals))
            # print("testing col: " + str(negative_y_vals + positive_y_vals))
            col_sum += abs(sum((negative_y_vals + positive_y_vals)))
        # print("idx " + str(idx) + " col_sum: " + str(col_sum)  + " : ")
        if col_sum == 0:
            return idx*100
    return 0

def smudge(rock_list, position, pattern):
    width = len(pattern[0])
    height = len(pattern)
    if position%100 == 0:
        idx = position/100
        slice_range = min(idx, height - idx)
        possible_smudges = [(x, y) for y in range(height) for x in range(width)]
        # print(possible_smudges)
        for smudge in possible_smudges:
            if smudge in rock_list:
                smudged_rock_list = [ x for x in rock_list if x != smudge]
            else:
                smudged_rock_list = rock_list + [smudge]
            rock_x_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[1], x[0]]), lambda x: x[1])))
            # print(rock_x_list)
            # rock_y_list = list(map(lambda x: list(x[1]), rock_list))
            pattern_sum_x =  find_y_mirror(rock_x_list, len(pattern[0]))
            if pattern_sum_x:
                # print("--- --- --- smudged y_mirror found: " + str(pattern_sum_x))
                return pattern_sum_x
            rock_y_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[0], x[1]]), lambda x: x[0])))
            pattern_sum_y = find_x_mirror(rock_y_list, len(pattern), idx)
            if pattern_sum_y == position:
                print("!!! SAME MIRROR !!!")
            if pattern_sum_y:
                # print("--- --- ---- smudged x_mirror found: " + str(pattern_sum_y))
                return pattern_sum_y
    else:
        idx = position
        slice_range = min(idx, width - idx)
        possible_smudges = [(x, y) for x in range(width) for y in range(height)]
        # print(possible_smudges)
        for smudge in possible_smudges:
            if smudge in rock_list:
                smudged_rock_list = [ x for x in rock_list if x != smudge]
            else:
                smudged_rock_list = rock_list + [smudge]
            # print(len(smudged_rock_list))
            rock_x_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[1], x[0]]), lambda x: x[1])))
            # print(rock_x_list)
            # rock_y_list = list(map(lambda x: list(x[1]), rock_list))
            pattern_sum_x =  find_y_mirror(rock_x_list, len(pattern[0]), idx)
            if pattern_sum_x == position:
                print("!!! SAME MIRROR !!!")
            if pattern_sum_x:
                # print("--- --- --- smudged y_mirror found: " + str(pattern_sum_x))
                return pattern_sum_x
            rock_y_list = list(map(lambda x: list(x[1]), groupby(sorted(smudged_rock_list, key=lambda x : [x[0], x[1]]), lambda x: x[0])))
            pattern_sum_y = find_x_mirror(rock_y_list, len(pattern))
            if pattern_sum_y:
                # print("--- --- --- smudged x_mirror found: " + str(pattern_sum_y))
                return pattern_sum_y
