# INPUT
# =====

INPUT_PATH = 'inputs/10.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]

directions = {'n': (-1, 0), 'e': (0, 1), 's': (1, 0), 'w': (0, -1)}
opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
pipes = {'F': ['e', 's'], 'L': ['n', 'e'], 'J': ['n', 'w'], '7': ['w', 's'], '|': ['n', 's'], '-': ['e', 'w']}

S = next((i, j) for i in range(len(input)) for j in range(len(input[0])) if input[i][j] == 'S')

def find_connection(p, dir_name):
    global input
    i = p[0] + directions[dir_name][0]
    j = p[1] + directions[dir_name][1]
    if not(0 <= i < len(input) and 0 <= j < len(input[0])): return None
    next_dir = [dir for dir in pipes.get(input[i][j], []) if dir != opposites[dir_name]]
    if len(next_dir) != 1: return None
    return ((i, j), next_dir[0])

connections_to_S = [find_connection(S, dir_name) for dir_name in ['n', 'e', 's', 'w']]
connections_to_S = [c for c in connections_to_S if c]
assert len(connections_to_S) == 2

loop = [connections_to_S[0][0], S, connections_to_S[1][0]]
loop_dir_names = [connections_to_S[0][1], None, connections_to_S[1][1]]

farthest_count = 1
while True:
    farthest_count += 1
    first_p, first_dir_name = find_connection(loop[0], loop_dir_names[0])
    last_p, last_dir_name = find_connection(loop[-1], loop_dir_names[-1])
    if first_p == last_p or first_p == loop[-1] or last_p == loop[0]:
        break
    loop.insert(0, first_p)
    loop_dir_names.insert(0, first_dir_name)
    loop.append(last_p)
    loop_dir_names.append(last_dir_name)
    

output = farthest_count


# PRINT
# =====
print(output)

