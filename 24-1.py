# INPUT
# =====

INPUT_PATH = 'inputs/24.txt'
with open(INPUT_PATH) as file: input = file.read()
cmin = 200000000000000
cmax = 400000000000000

# input = """19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3"""
# cmin = 7
# cmax = 27

# IMPORTS
# =======

# SOLUTION
# ========


angle_max = 4 * (cmax - cmin)
input = input.splitlines()

class Segment:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def intersection(self, other):
        # Calculate the determinant
        det = other.vy * self.vx - other.vx * self.vy
        if det == 0:
            return None  # Parallel lines

        # Calculate t and s
        dx = other.x - self.x
        dy = other.y - self.y
        t = (dx * other.vy - dy * other.vx) / det
        s = (dx * self.vy - dy * self.vx) / det

        return t, s



segments = {}
for line in input:
    position, velocity = line.split('@')
    x, y, z = map(float, map(lambda p: p.strip(), position.split(',')))
    vx, vy, vz = map(float, map(lambda p: p.strip(), velocity.split(',')))
    segment = Segment(x, y, vx, vy)
    segments[line] = segment

output = 0
keys = list(segments.keys())
for i in range(len(segments)):
    for j in range(i + 1, len(segments)):
        s_i = segments[keys[i]]
        s_j = segments[keys[j]]
        intersection = s_i.intersection(s_j)
        if not intersection: continue
        t, s = intersection
        if t < 0 or s < 0: continue
        intersection_point_x = s_i.x + t * s_i.vx
        intersection_point_y = s_i.y + t * s_i.vy
        if not (cmin <= intersection_point_x <= cmax and cmin <= intersection_point_y <= cmax): continue
        output += 1


# PRINT
# =====
print(output)

