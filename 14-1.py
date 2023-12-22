# INPUT
# =====

INPUT_PATH = 'inputs/14.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

matrix = [list(line) for line in input.splitlines()]
columns = [''.join([matrix[j][i] for j in range(len(matrix))]) for i in range(len(matrix[0]))]
columns = [[(len(r), r.count("O")) for r in c.split('#')] for c in columns]
output = 0
for column in columns:
    distance = 0
    for chunk in column:
        count = chunk[1]
        space = len(matrix) - distance - count + 1
        output += space * count + count * (count - 1) // 2
        distance += chunk[0] + 1
        

# PRINT
# =====

print(output)
