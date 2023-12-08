const = [15871, 19637, 12643, 14257, 21251, 19099]
loop = [31742, 39274, 25286, 28514, 42502, 38198]
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

def test_loop (cycle):
    steps = list(map(lambda x : const[x] + cycle * loop[x], list(range(6))))
    if steps.count(steps[0]) != 6:
        return False
    return True
cycles = 0



while not test_loop(cycles):
    cycles += 1
print(cycles)
