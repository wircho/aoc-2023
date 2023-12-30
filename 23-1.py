# INPUT
# =====

INPUT_PATH = 'inputs/23.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import sys

# SOLUTION
# ========

sys.setrecursionlimit(10000)

input = [list(line) for line in input.splitlines()]

start_j = next(j for j in range(len(input)) if input[0][j] == '.')
end_j = next(j for j in range(len(input)) if input[-1][j] == '.')

start = (0, start_j)
end = (len(input) - 1, end_j)
false_end = (len(input), end_j)

def _all_paths_to(p, excluded_point):
    if p == start: return [[p]]
    i, j = p
    valid_neighbors = []
    if i > 0 and input[i - 1][j] not in '#^><' and (i - 1, j) != excluded_point:
        valid_neighbors.append((i - 1, j))
    if i < len(input) - 1 and input[i + 1][j] not in '#v><' and (i + 1, j) != excluded_point:
        valid_neighbors.append((i + 1, j))
    if j > 0 and input[i][j - 1] not in '#<^v' and (i, j - 1) != excluded_point:
        valid_neighbors.append((i, j - 1))
    if j < len(input[0]) - 1 and input[i][j + 1] not in '#>^v' and (i, j + 1) != excluded_point:
        valid_neighbors.append((i, j + 1))
    if len(valid_neighbors) == 0:
        return None
    paths_to_neighbors = [all_paths_to(n, p) for n in valid_neighbors]
    paths_to_neighbors = [l for l in paths_to_neighbors if l is not None]
    paths_to_neighbors = [path + [p] for l in paths_to_neighbors for path in l] #  if p not in path]
    if len(paths_to_neighbors) == 0: return None
    return paths_to_neighbors

all_paths_to_dict = {}
def all_paths_to(p, excluded_point):
    if (p, excluded_point) not in all_paths_to_dict:
        all_paths_to_dict[(p, excluded_point)] = _all_paths_to(p, excluded_point)
    return all_paths_to_dict[(p, excluded_point)]

all_paths_to_end = all_paths_to(end, false_end)

output = max(map(len, all_paths_to_end)) - 1

# PRINT
# =====
print(output)

