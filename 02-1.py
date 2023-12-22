# INPUT
# =====

INPUT_PATH = 'inputs/02.txt'
with open(INPUT_PATH) as file: input = file.readlines()

# SOLUTION
# ========

max_amounts = {'red': 12, 'green': 13, 'blue': 14}
output = 0
for line in input:
    game_label, game = line.split(':')
    game_index = int(game_label.split(' ')[1])
    game_plays = [b.strip().split(' ') for a in game.split(';') for b in a.split(',')]
    if all(int(p[0]) <= max_amounts[p[1]] for p in game_plays): output += game_index

# PRINT
# =====

print(output)
