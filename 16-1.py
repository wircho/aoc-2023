# INPUT
# =====

INPUT_PATH = 'inputs/16.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]
def get(input, i, j):
    if i < 0 or i >= len(input) or j < 0 or j >= len(input[i]): return None
    return input[i][j]
current_positions = set([(0, -1, 0, 1)])
all_positions = current_positions.copy()
energized_positions = set()
while True:
    new_positions = set()
    for pos in current_positions:
        i, j, di, dj = pos
        ci, cj = i + di, j + dj
        p = get(input, ci, cj)
        if p is None: continue
        elif p == '-':
            if di == 0: new_positions = new_positions.union(set([(ci, cj, di, dj)]) - all_positions)
            else: new_positions = new_positions.union(set([(ci, cj, 0, -1), (ci, cj, 0, 1)]) - all_positions)
        elif p == '|':
            if dj == 0: new_positions = new_positions.union(set([(ci, cj, di, dj)]) - all_positions)
            else: new_positions = new_positions.union(set([(ci, cj, -1, 0), (ci, cj, 1, 0)]) - all_positions)
        elif p == '/':
            new_positions = new_positions.union(set([(ci, cj, -dj, -di)]) - all_positions)
        elif p == '\\':
            new_positions = new_positions.union(set([(ci, cj, dj, di)]) - all_positions)
        elif p == '.':
            new_positions = new_positions.union(set([(ci, cj, di, dj)]) - all_positions)
        else: assert False
        energized_positions.add((ci, cj))
    if len(new_positions) == 0: break
    current_positions = new_positions
    all_positions = all_positions.union(new_positions)

output = len(energized_positions)
    

# PRINT
# =====

print(output)
