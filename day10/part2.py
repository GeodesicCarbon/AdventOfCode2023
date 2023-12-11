#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress, tee
import math
import sys

sys.setrecursionlimit(100000)


file_input = open("input.txt", "r")
# file_input = open("example", "r")
pipe_map = []
cycle_map = {}

# @functools.total_ordering
class Coord:
    def __init__(self, x, y, shape='', charmap=None):
        self.x = x
        self.y = y
        if charmap is not None:
            # print("charmap: " + str(charmap[0]))
            self.charmap = charmap
        else:
            self.charmap = pipe_map
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
            return true
        elif self.y > other.y:
            return false
        elif self.y == other.y and self.x < other.x:
            return true
        else:
            return false
    def __hash__(self):
        return self.x + self.y*1000000


class Coords:
    def __init__(self, width, height, charmap):
        self.width = width
        self.height = height
        self.charmap = charmap
        self.area = width * height
        # print("-- coord w, h: " + str(width) +  " " + str(height))

    def make_coord(self, pos: Tuple[int, int], shape='', charmap=pipe_map):
        # print("    " + str(pos[0]) + ":" + str(pos[1]) + "max: " + str(self.width) + " " + str(self.height))
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

def map_connected_pipes(pipe: Coord) -> List[Coord]:
    if pipe.shape == "|":
        return pipe_coords.get_cardinal_neighbours(pipe)[-2:]
    elif pipe.shape == "-":
        return pipe_coords.get_cardinal_neighbours(pipe)[:2]
    elif pipe.shape == "L":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1:3]))))
        return pipe_coords.get_cardinal_neighbours(pipe)[1:3]
    elif pipe.shape == "J":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[0::2]))))
        return pipe_coords.get_cardinal_neighbours(pipe)[0::2]
    elif pipe.shape == "7":
        return pipe_coords.get_cardinal_neighbours(pipe)[0::3]
    elif pipe.shape == "F":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1::2]))))
        return pipe_coords.get_cardinal_neighbours(pipe)[1::2]
    return []

def expand_connected_pipes(pipe_conn: Coord) -> List[Coord]:
    flood_pipe = flood_coords.make_coord((1 + pipe_conn.x*3, 1 + pipe_conn.y*3), charmap=flood_map)
    if pipe_conn.shape == "|":
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[-2:]:
            flood_map[pipe.y][pipe.x] = "*"
    elif pipe_conn.shape == "-":
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[:2]:
            flood_map[pipe.y][pipe.x] = "*"
    elif pipe_conn.shape == "L":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1:3]))))
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[1:3]:
            flood_map[pipe.y][pipe.x] = "*"
    elif pipe_conn.shape == "J":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[0::2]))))
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[0::2]:
            flood_map[pipe.y][pipe.x] = "*"
    elif pipe_conn.shape == "7":
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[0::3]:
            flood_map[pipe.y][pipe.x] = "*"
    elif pipe_conn.shape == "F":
        # print(str(list(map(str, pipe_coords.get_cardinal_neighbours(pipe)[1::2]))))
        for pipe in flood_coords.get_cardinal_neighbours(flood_pipe)[1::2]:
            flood_map[pipe.y][pipe.x] = "*"
    return []

def fix_start(start_coord):
    for pipe in cycle_map[start_coord]:
        x_diff = pipe.x - start_coord.x
        y_diff = pipe.y - start_coord.y
        print("start_fix_diff: " + str(x_diff) + " " + str(y_diff))
        flood_map[start_coord.y*3 + y_diff + 1][start_coord.x*3 + x_diff + 1] = "*"

def filter_connected_to_start(start: Coord, cands: List[Coord]):
    connected_pipes = []

    for cand in cands:
        if list(filter(lambda x: x == start, map_connected_pipes(cand))):
            connected_pipes.append(cand)
    return connected_pipes

def get_next_pipe(prev_pipe: Coord, current_pipe: Coord) -> Coord:
    cands = map_connected_pipes(current_pipe)
    # print("  cands : " + str(list(map(str, cands))))
    # print("  filtered: " + str(list(filter(lambda x: x != prev_pipe, cands))))
    return list(filter(lambda x: x != prev_pipe, cands))[0]

def print_map(map):
    for row in map:
        print("".join(row))

def flood_neighbour(origin: Coord, target_map):
    if target_map[origin.y][origin.x] == "*":
        return
    target_map[origin.y][origin.x] = "O"
    # print("len: " + str(pipe_coords.get_all_neightbours(origin)))
    for dest_coord in flood_coords.get_all_neightbours(origin):
        if target_map[dest_coord.y][dest_coord.x] != "O" and target_map[dest_coord.y][dest_coord.x] != "*":
            flood_neighbour(dest_coord, target_map)

line_num = 0
start_pos = ()
for line in file_input:
    pipe_map.append(line.strip())
    if line.find("S") != -1:
        start_pos =(line.find("S"), line_num)
    line_num += 1


# print(pipe_map)

# for row in pipe_map:
#     for space in row:

pipe_coords = Coords(len(pipe_map[0]), len(pipe_map), pipe_map)
start_coord = pipe_coords.make_coord(start_pos, "S")
print(start_coord)
# print(list(map(str,filter_connected_to_start(start_coord, pipe_coords.get_cardinal_neighbours(start_coord)))))
cycle_map[start_coord] = filter_connected_to_start(start_coord, pipe_coords.get_cardinal_neighbours(start_coord, True))
cycle_fwd = [start_coord, cycle_map[start_coord][0]]
cycle_bck = [start_coord, cycle_map[start_coord][1]]
# print(cycle_fwd)
# print(cycle_bck)
cycle_map[cycle_map[start_coord][0]] = map_connected_pipes(cycle_map[start_coord][0])
cycle_map[cycle_map[start_coord][1]] = map_connected_pipes(cycle_map[start_coord][1])
idx = 2
while get_next_pipe(cycle_fwd[-2], cycle_fwd[-1]) not in cycle_bck:
    # print(idx)
    if idx % 100000 == 0:
        print(idx)
    # print(str(cycle_fwd[-2]) + " " + str(cycle_fwd[-1]))
    # print("next_fwd")
    next_fwd = get_next_pipe(cycle_fwd[-2], cycle_fwd[-1])
    # print(str(cycle_bck[-2]) + " " + str(cycle_bck[-1]))
    # print("next_bck")
    next_bck = get_next_pipe(cycle_bck[-2], cycle_bck[-1])
    cycle_map[next_fwd] = map_connected_pipes(next_fwd)
    cycle_map[next_bck] = map_connected_pipes(next_bck)
    cycle_fwd.append(next_fwd)
    cycle_bck.append(next_bck)
    idx += 1
# print("Loop len: " + str(idx-1))
# print(str(get_next_pipe(start_coord, cycle_map[start_coord][0])))

flood_map = []
for row in pipe_map:
    flood_map += [['.'] * len(pipe_map[0])*3]
    flood_row = []
    for col in [*row]:
        flood_row += ['.', '.', '.']
    flood_map.append(flood_row)
    flood_map += [['.'] * len(row)*3]
flood_coords = Coords(len(flood_map[0]), len(flood_map), charmap=flood_map)
print_map(flood_map)
print(str(len(flood_map[0])) +" " + str(len(flood_map)))

for loop_coords in cycle_map.keys():
    expand_connected_pipes(loop_coords)
    # print("x, y: " + str(loop_coords.x) + " " + str(loop_coords.y))
    flood_map[loop_coords.y*3 +1][loop_coords.x*3 +1] = "*"

print(start_coord)
fix_start(start_coord)

print_map(flood_map)
flood_map[0] = ["O"] * len(flood_map[0])
flood_map[-1] = ["O"] * len(flood_map[0])
for row in range(1, len(flood_map)-1):
    flood_map[row][0] = "O" if flood_map[row][0] != "*" else flood_map[row][0]
    flood_map[row][-1] = "O" if flood_map[row][-1] != "*" else flood_map[row][-1]
print("-----")
print_map(flood_map)

for row in range(len(flood_map)):
    for col in range(len(flood_map[0])):
        if flood_map[row][col] == "*":
            continue
        test_coord = flood_coords.make_coord((col, row), charmap=flood_map)
        # print(test_coord)
        if flood_map[test_coord.y][test_coord.x] == "O":
            flood_neighbour(test_coord, flood_map)
print("-----")
print_map(flood_map)

reduced_flood_map = []
reduced_flood_map_pic = []
for row in flood_map[1::3]:
    reduced_flood_map += (row[1::3])
    reduced_flood_map_pic.append(row[1::3])

print("-----")
print_map(reduced_flood_map_pic)
print("Nest size: " + str(reduced_flood_map.count(".")))

# print("----")
# print_map(flood_map)

file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
