#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress, tee
import math
import sys



file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")
x_list = set()
y_list = set()
galaxy_list = []
galaxy_charmap = []
expansion_factor = 1000000

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
    for row in charmap:
        print("".join(row))

def shortest_path(galaxy1: Coord, galaxy2: Coord) -> int:
    dist = abs(galaxy1.x - galaxy2.x) + abs(galaxy1.y - galaxy2.y)
    # print("start: " + str(galaxy1) + " end: " + str(galaxy2) + " dist: " +str(dist))
    return abs(galaxy1.x - galaxy2.x) + abs(galaxy1.y - galaxy2.y)

row = 0
for line in file_input:
    galaxy_charmap.append(line)
    galaxies = [(r.start(0), row) for r in re.finditer("\#", line)]
    for galaxy in galaxies:
        y_list.add(row)
        x_list.add(galaxy[0])
        galaxy_list.append((galaxy[0], row))
    row += 1
print(x_list)

galaxy_coords = Coords(len(galaxy_charmap[0]), len(galaxy_charmap), charmap=galaxy_charmap)
galaxy_list = list(map(lambda x: galaxy_coords.make_coord((x[0], x[1]), ), galaxy_list))
expand_x_set = set(range(galaxy_coords.width)).difference(x_list)
expand_y_set = set(range(galaxy_coords.height)).difference(y_list)

print("Galaxies :" + str(list(map(str, galaxy_list))))
for expansion in reversed(sorted(list(expand_x_set))):
    for galaxy in filter(lambda x: x.x > expansion,galaxy_list):
        galaxy.x += expansion_factor - 1

for expansion in reversed(sorted(list(expand_y_set))):
    for galaxy in filter(lambda x: x.y > expansion,galaxy_list):
        galaxy.y += expansion_factor - 1

print("Galaxies :" + str(list(map(str, galaxy_list))))

path_sum = 0
for idx in range(len(galaxy_list)):
    start_galaxy = galaxy_list[idx]
    # print("dest_list = " + str(list(map(str, galaxy_list[idx + 1:len(galaxy_list)]))))
    for dest_galaxy in galaxy_list[idx + 1:len(galaxy_list)]:
        path_sum += shortest_path(start_galaxy, dest_galaxy)

print("sum: " + str(path_sum))

file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
