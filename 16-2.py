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

def get_energy(i, j, di, dj):
    current_positions = set([(i, j, di, dj)])
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
    return len(energized_positions)

output = 0
for i in range(len(input)):
    output = max(output, get_energy(i, -1, 0, 1), get_energy(i, len(input[i]), 0, -1))
for j in range(len(input[0])):
    output = max(output, get_energy(-1, j, 1, 0), get_energy(len(input), j, -1, 0))
    

# PRINT
# =====

print(output)
