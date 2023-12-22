# INPUT
# =====

INPUT_PATH = 'inputs/18.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

input = input.splitlines()
pos = (0, 0)
min_i, max_i, min_j, max_j = 0, 0, 0, 0
dirs = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}
edge = [pos]
for line in input:
    dir, length, _ = line.split()
    dir = dirs[dir]
    length = int(length)
    for _ in range(length):
        pos = (pos[0] + dir[0], pos[1] + dir[1])
        edge.append(pos)
        min_i, max_i = min(min_i, pos[0]), max(max_i, pos[0])
        min_j, max_j = min(min_j, pos[1]), max(max_j, pos[1])

edge = set(edge)
inside_point = (1, 1)  # I looked and saw that (1, 1) is inside
inside = set([inside_point])
current = set([inside_point])
while len(current) > 0:
    new = set()
    for pos in current:
        for dir in dirs.values():
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if new_pos in inside or new_pos in edge: continue
            inside.add(new_pos)
            new.add(new_pos)
    current = new

output = len(edge) + len(inside)

# PRINT
# =====
print(output)

