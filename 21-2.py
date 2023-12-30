# INPUT
# =====

INPUT_PATH = 'inputs/21.txt'
with open(INPUT_PATH) as file: input = file.read()

steps = 26501365

# IMPORTS
# =======

from itertools import product

# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]

start_i, start_j = next((i, j) for i, j in product(range(len(input)), range(len(input[0]))) if input[i][j] == 'S')
S = (start_i, start_j)

# It turns out the input satisfies this, making the solution easier
assert all(input[start_i][j] == '.' for j in range(start_j + 1, len(input[0])))
assert all(input[i][start_j] == '.' for i in range(start_i + 1, len(input)))
assert len(input) % 2 == 1
assert len(input[0]) % 2 == 1

# Given the above, there are 8 points that are special:
_n = (0, start_j)
_e = (start_i, len(input[0]) - 1)
_s = (len(input) - 1, start_j)
_w = (start_i, 0)
_ne = (0, len(input[0]) - 1)
_se = (len(input) - 1, len(input[0]) - 1)
_sw = (len(input) - 1, 0)
_nw = (0, 0)

special_points = [_n, _e, _s, _w, _ne, _se, _sw, _nw]

special_points_and_S = special_points + [S]

# For each special point we compute the ending points within the input after any number of steps
special_point_box_reach = {}       # special_point -> distance -> set of points
special_point_box_reach_stop = {}  # special_point -> 0 or 1 -> set of points
distances_to_special_points = {}   # any point -> special_point -> distance
max_stop_distance = 0
for special_point in special_points_and_S:
    step = 0
    positions = {step: set([special_point])}
    distances_to_special_points.setdefault(special_point, {}).update({special_point: 0})
    while True:
        step += 1
        new_positions = set()
        for i, j in positions[step - 1]:
            for a, b in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if i + a < 0 or i + a >= len(input): continue
                if j + b < 0 or j + b >= len(input[0]): continue
                if input[i + a][j + b] == '#': continue
                new_positions.add((i + a, j + b))
                distances_to_special_points.setdefault((i + a, j + b), {}).update({special_point: min(step, distances_to_special_points.get((i + a, j + b), {}).get(special_point, float('inf')))})
        positions[step] = new_positions
        if step >= 3 and len(positions[step]) == len(positions[step - 2]) and len(positions[step - 1]) == len(positions[step - 3]):
            max_stop_distance = max(max_stop_distance, step)
            special_point_box_reach_stop[special_point] = {step % 2: positions[step], (step - 1) % 2: positions[step - 1]}
            break
    special_point_box_reach[special_point] = positions

side = len(input)
s_to_side = distances_to_special_points[S][_e]
s_to_corner = distances_to_special_points[S][_ne]

assert len(input[0]) == side

assert distances_to_special_points[S][_s] == s_to_side
assert distances_to_special_points[S][_w] == s_to_side
assert distances_to_special_points[S][_n] == s_to_side

assert distances_to_special_points[S][_se] == s_to_corner
assert distances_to_special_points[S][_sw] == s_to_corner
assert distances_to_special_points[S][_nw] == s_to_corner

assert 2 * s_to_side + 1 == side

assert s_to_side * 2 == s_to_corner

assert side % 2 == 1
assert s_to_side % 2 == 1
assert steps % 2 == 1

# Knowing the above, we know that the distance from S to any box (b_i, b_j) is:
# (b_i != 0) * (s_to_side + (abs(b_i) - 1) * side + 1) + (b_j != 0) * (s_to_side + (abs(b_j) - 1) * side + 1)

output = 0
output += len(special_point_box_reach_stop[S].get(steps, special_point_box_reach_stop[S][steps % 2]))


# For b_i = 0, b_j > 0, we have:
# Distance to the box is:
# s_to_side + (b_j - 1) * side + 1  # parity: b_j + 1, parity left: bj (starts odd)
# For all the boxes where s_to_side + (b_j - 1) * side + 1 + max_stop_distance <= steps, we assume they're all contained:
# Solving: s_to_side + (b_j - 1) * side + 1 + max_stop_distance <= steps
# (b_j - 1) * side <= steps - s_to_side - max_stop_distance - 1
# b_j <= (steps - s_to_side - max_stop_distance - 1) / side + 1
# b_j <= int((steps - s_to_side - max_stop_distance - 1) / side + 1)
num_straight_contained_boxes = max(0, int((steps - s_to_side - max_stop_distance - 1) / side + 1))
num_even = num_straight_contained_boxes // 2  # Starts odd
num_odd = num_straight_contained_boxes - num_even

for entry_point in [_w, _e, _n, _s]:
    output += num_even * len(special_point_box_reach_stop[entry_point][0]) + num_odd * len(special_point_box_reach_stop[entry_point][1])



# We need for sure that s_to_side + (b_j - 1) * side + 1 <= steps
# Solving: s_to_side + (b_j - 1) * side + 1 <= steps
# (b_j - 1) * side <= steps - s_to_side - 1
# b_j <= (steps - s_to_side - 1) / side + 1
# b_j <= int((steps - s_to_side - 1) / side + 1)
max_index_of_reachable_box = int((steps - s_to_side - 1) / side + 1)
num_non_trivial_boxes = 0
for b_j in range(num_straight_contained_boxes + 1, max_index_of_reachable_box + 1):
    distance_to_box = s_to_side + (b_j - 1) * side + 1
    left_over_steps = steps - distance_to_box
    if left_over_steps < 0: continue
    for entry_point in [_s, _n, _w, _e]:
        num_non_trivial_boxes += 1
        output += len(special_point_box_reach[entry_point].get(left_over_steps, special_point_box_reach_stop[entry_point][left_over_steps % 2]))



# For b_i > 0 and b_j > 0:
# Distance to the box is:
# 2 * s_to_side + 2 + (abs(b_i) + abs(b_j) - 2) * side
# side + (abs(b_i) + abs(b_j) - 2) * side + 1
# (abs(b_i) + abs(b_j) - 1) * side + 1  # parity: bi + bj, parity left: bi + bj - 1 (starts odd at corner)
# For all the boxes where (abs(b_i) + abs(b_j) - 1) * side + 1 + max_stop_distance <= steps, we assume they're all contained:
# Solving: (abs(b_i) + abs(b_j) - 1) * side + 1 + max_stop_distance <= steps
# abs(b_i) + abs(b_j) <= (steps - 1 - max_stop_distance) / side
# b_i + b_j <= int((steps - 1 - max_stop_distance) / side)
contained_triangle_height = max(0, int((steps - 1 - max_stop_distance) / side) - 1)
if contained_triangle_height % 2 == 0:
    half_contained_triangle_height = contained_triangle_height // 2
    # num_odd = 1 + 3 + ... + 2 * half_contained_triangle_height - 1
    # num_even = 2 + 4 + ... + 2 * half_contained_triangle_height
    num_odd = half_contained_triangle_height ** 2
    num_even = half_contained_triangle_height * (half_contained_triangle_height + 1)
else:
    half_contained_triangle_height = (contained_triangle_height - 1) // 2
    # num_odd = 1 + 3 + ... + 2 * half_contained_triangle_height + 1
    # num_even = 2 + 4 + ... + 2 * half_contained_triangle_height
    num_odd = (half_contained_triangle_height + 1) ** 2
    num_even = half_contained_triangle_height * (half_contained_triangle_height + 1)
for entry_point in [_nw, _se, _sw, _ne]:
    output += num_even * len(special_point_box_reach_stop[entry_point][0]) + num_odd * len(special_point_box_reach_stop[entry_point][1])


# We need for sure that 2 * s_to_side + 2 + (abs(b_i) + abs(b_j) - 2) * side <= steps
# Solving: 2 * s_to_side + 2 + (b_i + b_j - 2) * side <= steps
# (b_i + b_j - 2) * side <= steps - 2 * s_to_side - 2
# b_i + b_j <= (steps - 2 * s_to_side - 2) / side + 2
# b_i + b_j <= int((steps - 2 * s_to_side - 2) / side + 2)
max_reachable_triangle_height = max(0, int((steps - 2 * s_to_side - 2) / side + 2) - 1)

for height in range(contained_triangle_height + 1, max_reachable_triangle_height + 1):
    for b_i in range(1, height + 1):
        b_j = height + 1 - b_i
        distance_to_box = 2 * s_to_side + 2 + (b_i + b_j - 2) * side
        left_over_steps = steps - distance_to_box
        if left_over_steps < 0: continue
        for entry_point in [_nw, _se, _sw, _ne]:
            num_non_trivial_boxes += 1
            output += len(special_point_box_reach[entry_point].get(left_over_steps, special_point_box_reach_stop[entry_point][left_over_steps % 2]))


# PRINT
# =====
print(output)

