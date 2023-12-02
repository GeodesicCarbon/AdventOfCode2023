#!/bin/python3
calib_in = open("fixed2.txt", "r")
# calib_in = open("example.txt", "r")
numwords = {
    "1":"one",
    "2":"two",
    "3":"three",
    "4":"four",
    "5":"five",
    "6":"six",
    "7":"seven",
    "8":"eight",
    "9":"nine"
}
calib_sum = 0
debug = 0;
for line in calib_in:
    old_line = line
    r_replace = ("", 0)
    l_replace = ("", 99999)
    for k,v in numwords.items():
        r_idx = line.rfind(v)
        l_idx = line.find(v)
        if (r_idx != -1 and r_idx > r_replace[1]):
            r_replace = (k, r_idx)
        if (l_idx != -1 and l_idx < l_replace[1]):
            l_replace = (k, l_idx)
    if r_replace[0] != "":
        num_len = len(numwords[r_replace[0]])
        line = line[:r_replace[1] +num_len] + r_replace[0] + line[r_replace[1] + num_len:]
        # line = line[:r_replace[1]] + r_replace[0] + line[r_replace[1] + len(numwords[r_replace[0]]):]
    if l_replace[0] != "":
        line = line[:l_replace[1]] + l_replace[0] + line[l_replace[1]:]
        # line = line[:l_replace[1]] + l_replace[0] + line[r_replace[1] + len(numwords[r_replace[0]]):]
    digits = filter(str.isdigit, line)
    first_digit = next(digits)
    last_digit = first_digit
    for d in digits:
        last_digit = d
    if debug < 25:
        print(old_line.strip() + " // " + line.strip() + ": " + first_digit + last_digit)
        debug += 1;
    calib_sum += int(first_digit + last_digit)
print(calib_sum)
calib_in.close()
