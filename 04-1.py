# INPUT
# =====

INPUT_PATH = 'inputs/04.txt'
with open(INPUT_PATH) as file: input = file.readlines()

# SOLUTION
# ========

output = 0
for line in input:
    win, mine = map(lambda x: x.strip().split(), line.split(':')[1].split('|'))
    output += int(2 ** (len([m for m in mine if m in win]) - 1))
    

# PRINT
# =====

print(output)
