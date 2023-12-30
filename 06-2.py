# INPUT
# =====

INPUT_PATH = 'inputs/06.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

from math import sqrt, ceil, floor

# SOLUTION
# ========

lines = input.splitlines()
time = int(''.join(lines[0].split()[1:]))
distance = int(''.join(lines[1].split()[1:]))

discriminant = time * time - 4 * distance
sqrt_discriminant = sqrt(discriminant)
assert discriminant >= 0
sol0 = (time - sqrt_discriminant) / 2
sol1 = (time + sqrt_discriminant) / 2
output = floor(sol1) - ceil(sol0) + 1

# PRINT
# =====

print(output)

