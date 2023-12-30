# INPUT
# =====

INPUT_PATH = 'inputs/24.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import numpy as np
from sympy import symbols, solve

# SOLUTION
# ========

input = input.splitlines()

# 1. The Line class

class Line:
    def __init__(self, x, y, z, vx, vy, vz):
        self.p = np.array([x, y, z])  # Start
        self.v = np.array([vx, vy, vz])  # Direction

    
lines = []
for line in input:
    position, velocity = line.split('@')
    x, y, z = map(float, map(lambda p: p.strip(), position.split(',')))
    vx, vy, vz = map(float, map(lambda p: p.strip(), velocity.split(',')))
    lines.append(Line(x, y, z, vx, vy, vz))

# 2. Take symbolic "t's" for four lines

t = [symbols(f't{i}') for i in range(4)]

# 3. Compute the points on the four lines

qs = []
for i, line in enumerate(lines[:4]):
    q = line.p + t[i] * line.v
    qs.append(q)

# 4. The vectors from one of the points to the three others must be parallel

q0 = qs[0] - qs[3]
q1 = qs[1] - qs[3]
q2 = qs[2] - qs[3]

eqs = [
    q0[0] * q1[1] - q0[1] * q1[0],
    q0[0] * q2[1] - q0[1] * q2[0],
    q0[0] * q1[2] - q0[2] * q1[0],
    q0[0] * q2[2] - q0[2] * q2[0],
    q0[1] * q1[2] - q0[2] * q1[1],
    q0[1] * q2[2] - q0[2] * q2[1],
    q1[0] * q2[1] - q1[1] * q2[0],
    q1[0] * q2[2] - q1[2] * q2[0],
    q1[1] * q2[2] - q1[2] * q2[1]
]

# 5. Solve the equations

sol = solve(eqs)
sol = [s for s in sol if all(x > 0 for x in s.values())][0]

t0 = sol[t[0]]
t1 = sol[t[1]]

# 6. The first line is the one with the smallest t0

if t0 < t1:
    p0 = lines[0].p
    v0 = lines[0].v
    p1 = lines[1].p
    v1 = lines[1].v
else:
    _t0 = t0
    t0 = t1
    t1 = _t0
    p0 = lines[1].p
    v0 = lines[1].v
    p1 = lines[0].p
    v1 = lines[0].v

# 7. Compute the starting point

q0 = p0 + t0 * v0
q1 = p1 + t1 * v1
q = q0 - t0 * (q1 - q0) / (t1 - t0)

output = int(np.sum(q))

# PRINT
# =====

print(output)

