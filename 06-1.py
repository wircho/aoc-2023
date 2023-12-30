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
times = [int(t) for t in lines[0].split()[1:]]
distances = [int(d) for d in lines[1].split()[1:]]

output = 1
for i in range(len(times)):
    time = times[i]
    distance = distances[i]
    # Suppose button is held for held seconds
    # The boat runs for (time - held) seconds at speed held
    # Total distance = (time - held) * held
    # Eq: time * held - held^2 > distance
    #     held^2 - time * held + distance < 0
    discriminant = time * time - 4 * distance
    sqrt_discriminant = sqrt(discriminant)
    assert discriminant >= 0
    sol0 = (time - sqrt_discriminant) / 2
    sol1 = (time + sqrt_discriminant) / 2
    num_sols = floor(sol1) - ceil(sol0) + 1
    output *= num_sols

# PRINT
# =====

print(output)

