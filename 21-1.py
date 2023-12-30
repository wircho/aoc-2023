# INPUT
# =====

INPUT_PATH = 'inputs/21.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

from itertools import product

# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]

start_i, start_j = next((i, j) for i, j in product(range(len(input)), range(len(input[0]))) if input[i][j] == 'S')

positions = set([(start_i, start_j)])

steps = 1005 # 64
for step in range(steps):
    new_positions = set()
    for i, j in positions:
        for a, b in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if i + a < 0 or i + a >= len(input): continue
            if j + b < 0 or j + b >= len(input[0]): continue
            if input[i + a][j + b] == '#': continue
            new_positions.add((i + a, j + b))
    positions = new_positions

output = len(positions)

# PRINT
# =====
print(output)

