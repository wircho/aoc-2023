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
pipes_inv = {tuple(sorted(v)): k for k, v in pipes.items()}

S = next((i, j) for i in range(len(input)) for j in range(len(input[0])) if input[i][j] == 'S')

def find_connection(p, dir_name):
    global input
    i = p[0] + directions[dir_name][0]
    j = p[1] + directions[dir_name][1]
    if not(0 <= i < len(input) and 0 <= j < len(input[0])): return None
    next_dir = [dir for dir in pipes.get(input[i][j], []) if dir != opposites[dir_name]]
    if len(next_dir) != 1: return None
    return ((i, j), next_dir[0])

connections_to_S_dict = {dir_name: find_connection(S, dir_name) for dir_name in ['n', 'e', 's', 'w']}
connections_to_S_dict = {k: v for k, v in connections_to_S_dict.items() if v}
assert len(connections_to_S_dict) == 2

connections_to_S, S_pipe = list(connections_to_S_dict.values()), pipes_inv[tuple(sorted(connections_to_S_dict.keys()))]

input[S[0]][S[1]] = S_pipe

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
    
loop_set = set(loop)

output = 0

inside_dict = {"F": 1, "J": 1, "7": -1, "L": -1, "|": 2, "-": 0}

for i in range(len(input)):
    inside = 0
    for j in range(len(input[0])):
        if (i, j) in loop_set:
            inside += inside_dict[input[i][j]]
        else:
            if inside % 4 == 2:
                output += 1
        


# PRINT
# =====
print(output)

