#!/usr/bin/python3
import re
from typing import List, Tuple
from itertools import cycle, compress
import math

# file_input = open("input.txt", "r")
file_input = open("example.txt", "r")

card_str=["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

winnings = 0

def compare_hands(hand1: Tuple[int, str, int], hand2: Tuple[int, str, int]) -> int:
    if hand1[0] == hand2[0]:
        for idx in range(0,5):
            if card_str.index(hand1[1][idx]) > card_str.index(hand1[1][idx]):
                return 1
            elif card_str.index(hand1[1][idx]) < card_str.index(hand1[1][idx]):
                return 1
        return 0
    elif hand1[0] > hand2[0]:
        return 1
    else:
        return -1


hands = []
for line in file_input:
    hand, bid = line.strip().split(" ")
    cards_count = list({chara:hand.count(chara) for chara in set(hand)}.values())
    cards_count.sort()
    cards_count.reverse()
    hand_type = 0
    if cards_count[0] == 5: # 5 kind
        hand_type = 0
    elif cards_count[0] == 4: # 4 kind
        hand_type = 1
    elif cards_count[0] == 3 and len(cards_count) > 1 and cards_count[1] == 2:
        hand_type = 2
    elif cards_count[0] == 3:
        hand_type = 3
    elif cards_count[0] == 2 and len(cards_count) > 1 and cards_count[1] == 2:
        hand_type = 4
    elif cards_count[0] == 2:
        hand_type = 5
    elif cards_count[0] == 1:
        hand_type = 6
    hand_conv_str = int("0x" + "".join(list(map(lambda x: f'{card_str.index(x):x}', hand))), 16)
    hands.append((hand_type, hand_conv_str, int(bid), hand))

# print(hands)
hands.sort(key= lambda h: (h[0],h[1]),reverse=True)
print(hands)

for rank in range(1,len(hands)+1):
    winnings += rank * hands[rank-1][2]

print (winnings)
# print(file_input.readline())
file_input.close()
