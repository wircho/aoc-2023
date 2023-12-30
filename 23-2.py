# INPUT
# =====

INPUT_PATH = 'inputs/23.txt'
with open(INPUT_PATH) as file: input = file.read()

# input = """#.##
# #...
# #...
# ###."""

# input = """#.###
# #.###
# #...#
# #.#.#
# #...#
# ###.#
# """

# input = """#.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#"""

# IMPORTS
# =======

import sys
import copy

# SOLUTION
# ========

# It looks like the path is always of width 1, except at some points where there are some intersections

input = [list(map(lambda c: '#' if c == '#' else '.', line)) for line in input.splitlines()]

start_j = next(j for j in range(len(input)) if input[0][j] == '.')
end_j = next(j for j in range(len(input)) if input[-1][j] == '.')

start = (0, start_j)
end = (len(input) - 1, end_j)

nodes = [start, end]

edges = {}

def get_valid_neighbors(p):
    i, j = p
    valid_neighbors = []
    if i > 0 and input[i - 1][j] == '.':
        valid_neighbors.append((i - 1, j))
    if i < len(input) - 1 and input[i + 1][j] == '.':
        valid_neighbors.append((i + 1, j))
    if j > 0 and input[i][j - 1] == '.':
        valid_neighbors.append((i, j - 1))
    if j < len(input[0]) - 1 and input[i][j + 1] == '.':
        valid_neighbors.append((i, j + 1))
    return valid_neighbors

# Nodes
for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] == '.':
            valid_neighbors = get_valid_neighbors((i, j))
            if len(valid_neighbors) > 2:
                nodes.append((i, j))

# Edges
for node in nodes:
    valid_neighbors = get_valid_neighbors(node)
    for neighbor in valid_neighbors:
        current = neighbor
        previous = node
        length = 1
        while True:
            valid_neighbors = [p for p in get_valid_neighbors(current) if p != previous]
            if len(valid_neighbors) == 1:
                assert current not in nodes
                previous = current
                current = valid_neighbors[0]
                length += 1
            else:
                assert current in nodes
                assert length > 1
                edges.setdefault(node, {})[current] = length
                edges.setdefault(current, {})[node] = length
                break

# print(f"Nodes: {nodes}")
# print(f"Edges: {edges}")

# print(len(edges))

def all_paths_from_start_to(p, ending_section):
    if p == start: return [[start]]
    neighbors = [n for n in edges[p] if n not in ending_section]
    if len(neighbors) == 0: return None
    paths_to_neighbors = [all_paths_from_start_to(n, [p] + ending_section) for n in neighbors]
    paths_to_neighbors = [l for l in paths_to_neighbors if l is not None]
    paths_to_neighbors = [path + [p] for l in paths_to_neighbors for path in l]
    if len(paths_to_neighbors) == 0: return None
    return paths_to_neighbors

all_paths = all_paths_from_start_to(end, [])
path_lengths = []
for path in all_paths:
    path_length = 0
    for i in range(len(path) - 1):
        path_length += edges[path[i]][path[i + 1]]
    path_lengths.append(path_length)

output = max(path_lengths)

# PRINT
# =====
print(output)

