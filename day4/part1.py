#!/bin/python3
import re

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")
# wins_start = 8
wins_start = 10
# wins_end = 22
wins_end = 39
your_num_start = wins_end + 3

def get_wins(win_str: str):
    return list(map(int, win_str.split()))

def get_your_num(your_num: str):
    return list(map(int, your_num.split()))

win_sum = 0
for line in file_input:
    game_win = 0
    for win_num in get_wins(line[wins_start:wins_end]):
        if win_num in get_your_num(line[your_num_start:-1]):
            if game_win == 0:
                game_win = 1
            else:
                game_win = game_win * 2
    win_sum += game_win

print(win_sum)
file_input.close()
