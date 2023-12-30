# INPUT
# =====

INPUT_PATH = 'inputs/09.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

input = [list(map(int, line.split(' '))) for line in input.splitlines()]

output = 0

def diffs(seq):
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]

def is_all_zero(seq):
    return all(d == 0 for d in seq)

for line in input:
    seqs = [line]
    while True:
        if is_all_zero(seqs[-1]): break
        seqs.append(diffs(seqs[-1]))
    seqs[-1].append(0)
    for j in range(len(seqs) - 2, -1, -1):
        seqs[j].insert(0, seqs[j][0] - seqs[j + 1][0])
    output += seqs[0][0]
        

# SOLUTION
# ========



# PRINT
# =====
print(output)

