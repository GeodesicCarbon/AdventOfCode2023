import numpy as np

const = [15871, 19637, 12643, 14257, 21251, 19099]
loop = [31742, 39274, 25286, 28514, 42502, 38198]
# loop2 = [31742, -39274, 0, 0, 0, 0, 0]
# sum_matrix = np.vstack(np.array([-1, -1, -1, -1, -1, -1]))

# a1 = np.array([loop2])
# print(a1)
# a2 = np.concatenate((np.diag(loop), sum_matrix), axis=1)
# print(a2)
# a = np.concatenate((a1, a2), axis = 0)
a = np.array(const)
b = np.array(loop)
print(np.lcm.reduce(a))
loop2 = b-a
print(loop2)
# b = np.vstack(np.array(const) * -1)
print(a)
print(b)
# TTA dist : 15871 dest: KHZ
# KJA dist : 19637 dest: KRZ
# BGA dist : 12643 dest: HSZ
# AAA dist : 14257 dest: ZZZ
# LTA dist : 21251 dest: DXZ
# NJA dist : 19099 dest: HRZ
# KHZ dist : 31742 dest: KHZ
# KRZ dist : 39274 dest: KRZ
# HSZ dist : 25286 dest: HSZ
# ZZZ dist : 28514 dest: ZZZ
# DXZ dist : 42502 dest: DXZ
# HRZ dist : 38198 dest: HRZ
# x = np.linalg.solve(a, b)
# print(x)

# while not test_loop(cycles):
#     cycles += 1
# print(cycles)
