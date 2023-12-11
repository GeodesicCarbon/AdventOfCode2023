#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress, tee
import math


# file_input = open("input.txt", "r")
file_input = open("example", "r")
pipe_map = []
cycle_map = {}



# @functools.total_ordering
class Coord:
    def __init__(self, x, y, shape=''):
        self.x = x
        self.y = y
        if not shape:
            self.shape = pipe_map[y][x]
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
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # print("-- coord w, h: " + str(width) +  " " + str(height))

    def make_coord(self, pos: Tuple[int, int], shape=''):
        # print("    " + str(pos[0]) + ":" + str(pos[1]) + "max: " + str(self.width) + " " + str(self.height))
        if pos[0] < 0 or pos[0] >= self.width:
            # print("    " + str(pos[0]) + " too wide")
            return
        elif pos[1] < 0 or pos[1] >= self.height:
            # print("    " + str(pos[1]) + " too tall")
            return
        else:
            return Coord(pos[0], pos[1], shape)

    def get_cardinal_neighbours(self, origin: Coord, filterNone=False):
        coord_list = [
            self.make_coord((origin.x - 1, origin.y)),
            self.make_coord((origin.x + 1, origin.y)),
            self.make_coord((origin.x, origin.y - 1)),
            self.make_coord((origin.x, origin.y + 1))
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

pipe_coords = Coords(len(pipe_map[0]), len(pipe_map))
start_coord = pipe_coords.make_coord(start_pos, "S")
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
print("Loop len: " + str(idx-1))
# print(str(get_next_pipe(start_coord, cycle_map[start_coord][0])))
flood_map = []
for row in pipe_map:
    flood_map.append([*row])

for loop_coords in cycle_map.keys():
    flood_map[loop_coords.y][loop_coords.x] = "L"
print(flood_map)

file_input.close()
# file_output = open("sorted.txt", "w")
# for hand in hands:
#     file_output.write(str((hand[7], hand[6])) + "\n")
# file_output.close()
