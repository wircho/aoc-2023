# INPUT
# =====

INPUT_PATH = 'inputs/12.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import itertools

# SOLUTION
# ========

output = 0

for line in input.splitlines():
    record, counts = line.split(' ')
    counts = [int(i) for i in counts.split(',')] + [0]
    num_gaps = len(counts)
    gaps_total = len(record) - sum(counts)
    if gaps_total < num_gaps - 2: continue
    for combination in itertools.combinations(range(gaps_total + 1), num_gaps - 1):
        combination = [0] + list(combination) + [gaps_total]
        gaps = [combination[i + 1] - combination[i] for i in range(num_gaps)]
        potential_record = ''.join(g * '.' + c * '#' for g, c in zip(gaps, counts))
        if any(x[0] != '?' and x[0] != x[1] for x in zip(record, potential_record)): continue
        output += 1


# PRINT
# =====
print(output)

