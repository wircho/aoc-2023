# INPUT
# =====

INPUT_PATH = 'inputs/04.txt'
with open(INPUT_PATH) as file: input = file.readlines()

# SOLUTION
# ========

output = 0
counts = {}
for i, line in enumerate(input):
    win, mine = map(lambda x: x.strip().split(), line.split(':')[1].split('|'))
    score = len([m for m in mine if m in win])
    count = counts.get(i, 1)
    output += count
    for j in range(i + 1, min(i + score + 1, len(input))):
        counts[j] = counts.get(j, 1) + count

# PRINT
# =====

print(output)
