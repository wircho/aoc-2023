# INPUT
# =====

INPUT_PATH = 'inputs/02.txt'
with open(INPUT_PATH) as file: input = file.readlines()

# IMPORTS
# =======

from functools import reduce

# SOLUTION
# ========

output = 0
for line in input:
    min_amounts = {'red': 0, 'green': 0, 'blue': 0}
    _, game = line.split(':')
    game_plays = [b.strip().split(' ') for a in game.split(';') for b in a.split(',')]
    for p in game_plays:
        min_amounts[p[1]] = max(int(p[0]), min_amounts[p[1]])
    output += reduce(lambda x, y: x * y, min_amounts.values(), 1)
    

# PRINT
# =====

print(output)
