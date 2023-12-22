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
    _, __, hex = line.split()
    hex = hex.strip().lstrip('(').lstrip('#').rstrip(')')
    length = int(hex[0:5], 16)
    dir = dirs['RDLU'[int(hex[5])]]
    length = int(length)
    pos = (pos[0] + dir[0] * length, pos[1] + dir[1] * length)
    edge.append(pos)
    min_i, max_i = min(min_i, pos[0]), max(max_i, pos[0])
    min_j, max_j = min(min_j, pos[1]), max(max_j, pos[1])

def pop_corner(edge, i, new_corner):
    print(f"- Found a corner with points {edge[i]}, {edge[i + 1]}, {edge[i + 2]}")
    points = [edge[i], edge[i + 1], edge[i + 2]]
    bounds_0 = (min(p[0] for p in points), max(p[0] for p in points))
    bounds_1 = (min(p[1] for p in points), max(p[1] for p in points))
    other_edges = [edge[j] for j in range(len(edge)) if j not in [i, i + 1, i + 2]]
    for p in other_edges:
        if p[0] >= bounds_0[0] and p[0] <= bounds_0[1] and p[1] >= bounds_1[0] and p[1] <= bounds_1[1]:
            print(f"  Other edge {p} is inside the bounds, not popping")
            return 0
    edge[i + 1] = new_corner
    area_increment = (bounds_0[1] - bounds_0[0]) * (bounds_1[1] - bounds_1[0])
    print(f"  Vertex updated to {edge[i + 1]}")
    print(f"  Area increment: {area_increment}")
    return area_increment

area = 0
while True:
    if len(edge) <= 4: break
    i = 0
    current_area = area
    while i < len(edge) - 2:
        # POP CORNERS

        # right down
        if edge[i][0] == edge[i + 1][0] and edge[i + 1][1] == edge[i + 2][1] \
            and edge[i][1] < edge[i + 1][1] and edge[i + 1][0] < edge[i + 2][0]:
            area += pop_corner(edge, i, (edge[i + 2][0], edge[i][1]))
        
        # down left
        elif edge[i][1] == edge[i + 1][1] and edge[i + 1][0] == edge[i + 2][0] \
            and edge[i][0] < edge[i + 1][0] and edge[i + 1][1] > edge[i + 2][1]:
            area += pop_corner(edge, i, (edge[i][0], edge[i + 2][1]))

        # left up
        elif edge[i][0] == edge[i + 1][0] and edge[i + 1][1] == edge[i + 2][1] \
            and edge[i][1] > edge[i + 1][1] and edge[i + 1][0] > edge[i + 2][0]:
            area += pop_corner(edge, i, (edge[i + 2][0], edge[i][1]))

        # up right
        elif edge[i][1] == edge[i + 1][1] and edge[i + 1][0] == edge[i + 2][0] \
            and edge[i][0] > edge[i + 1][0] and edge[i + 1][1] < edge[i + 2][1]:
            area += pop_corner(edge, i, (edge[i][0], edge[i + 2][1]))
        
        # COLINEAR (all assumed to be disjoint and going out - seems safe!)

        # Colinear horizontal with middle one in between
        if edge[i][0] == edge[i + 1][0] == edge[i + 2][0] \
            and (edge[i][1] <= edge[i + 1][1] <= edge[i + 2][1]
            or edge[i][1] >= edge[i + 1][1] >= edge[i + 2][1]):
                edge.pop(i + 1)
        
        # Colinear vertical with middle one in between
        elif edge[i][1] == edge[i + 1][1] == edge[i + 2][1] \
            and (edge[i][0] <= edge[i + 1][0] <= edge[i + 2][0]
            or edge[i][0] >= edge[i + 1][0] >= edge[i + 2][0]):
                edge.pop(i + 1)

        # Colinear horizontal with middle one not in between
        elif edge[i][0] == edge[i + 1][0] == edge[i + 2][0]:
            area += min(abs(edge[i + 1][1] - edge[i][1]), abs(edge[i + 1][1] - edge[i + 2][1]))
            edge.pop(i + 1)

        # Colinear vertical with middle one not in between
        elif edge[i][1] == edge[i + 1][1] == edge[i + 2][1]:
            area += min(abs(edge[i + 1][0] - edge[i][0]), abs(edge[i + 1][0] - edge[i + 2][0]))
            edge.pop(i + 1)

        i += 1
    if area == current_area:
        break

# Assert that only a square is left - why not!
assert len(edge) == 5 \
    and edge[0][0] == edge[1][0] \
    and edge[1][1] == edge[2][1] \
    and edge[2][0] == edge[3][0] \
    and edge[3][1] == edge[0][1] \
    and edge[0][1] < edge[1][1] \
    and edge[1][0] < edge[2][0] \
    and edge[2][1] > edge[3][1] \
    and edge[3][0] > edge[0][0] \
    and edge[0][0] == edge[4][0] \
    and edge[0][1] == edge[4][1]

area += (edge[1][1] - edge[0][1] + 1) * (edge[2][0] - edge[1][0] + 1)
output = area

# PRINT
# =====
print(output)

