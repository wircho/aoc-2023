# INPUT
# =====

INPUT_PATH = 'inputs/17.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

input = [list(map(int, line)) for line in input.splitlines()]
def exists(i, j):
    return i >= 0 and i < len(input) and j >= 0 and j < len(input[i])
# node: (i, j, di, dj, k)
#  i, j: position
#  di, dj: direction to get there
#  k: number of last steps equal to di, dj
# edge:
#  (i, j, di, dj, k) -> (ci, cj, cdi, cdj, ck)
starting_node = (0, 0, 0, 0, 0)
nodes = set([starting_node])
edges = {}
for i in range(len(input)):
    for j in range(len(input[i])):
        for di, dj in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            for k in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                # k = 0 only makes sense if they are all 0
                if (k == 0 or (di == 0 and dj == 0)) and (i != 0 or j != 0):
                    continue
                # if i == 0 and j == 0 and k == 0 and di == 0 and dj == 0:
                #     import pdb; pdb.set_trace()
                if not exists(i - k * di, j - k * dj): continue
                nodes.add((i, j, di, dj, k))
                for _di, _dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if _di == -di and _dj == -dj: continue
                    if not exists(i + _di, j + _dj): continue
                    if k == 10 and _di == di and _dj == dj: continue
                    if k < 4 and (di != 0 or dj != 0) and (_di != di or _dj != dj): continue
                    _k = k + 1 if _di == di and _dj == dj else 1
                    edges.setdefault((i, j, di, dj, k), {}).update({(i + _di, j + _dj, _di, _dj, _k): input[i + _di][j + _dj]})

ending_nodes = {node for node in nodes if node[0] == len(input) - 1 and node[1] == len(input[node[0]]) - 1}

# Dijkstra's!

shortest_paths = {node: (float('infinity'), []) for node in nodes}
shortest_paths[starting_node] = (0, [])

queue = [(0, starting_node)]

while queue:
    (dist, current_node) = queue.pop(min(range(len(queue)), key=lambda i: queue[i][0]))
    if dist > shortest_paths[current_node][0]: continue
    for neighbor, neighbor_dist in edges.get(current_node, {}).items():
        old_dist, old_path = shortest_paths[neighbor]
        new_dist = dist + neighbor_dist
        # If we've found a shorter path to this neighbor, update our shortest paths data
        if new_dist < old_dist:
            shortest_paths[neighbor] = (new_dist, old_path + [current_node])
            # Add the neighbor to the queue
            queue.append((new_dist, neighbor))

output = min(shortest_paths[node][0] for node in ending_nodes)

# PRINT
# =====
print(output)

