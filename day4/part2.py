#!/bin/python3
import re

file_input = open("input.txt", "r")
# file_input = open("example.txt", "r")
# wins_start = 8
# wins_end = 22
wins_start = 10
wins_end = 39

card_copies = [1] * 999
your_num_start = wins_end + 3

def get_wins(win_str: str):
    return list(map(int, win_str.split()))

def get_your_num(your_num: str):
    return list(map(int, your_num.split()))

card_sum = 0
card_idx = 0
for line in file_input:
    game_win_idx = 1
    for win_num in get_wins(line[wins_start:wins_end]):
        if win_num in get_your_num(line[your_num_start:-1]):
            card_copies[card_idx+game_win_idx] += card_copies[card_idx]
            game_win_idx += 1
    card_idx += 1
    card_sum += card_copies[card_idx]

print(card_sum)
file_input.close()
