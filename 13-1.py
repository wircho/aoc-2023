# INPUT
# =====

INPUT_PATH = 'inputs/13.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

inputs = input.split("\n\n")
inputs = [tuple(tuple(line) for line in box.splitlines()) for box in inputs]

def find_mirror(matrix):
    for i in range(1, len(matrix)):
        if any(matrix[i - d] != matrix[i + d - 1] for d in range(1, min(i + 1, len(matrix) - i + 1))): continue
        return i
    return 0

output = 0

for input in inputs:
    transpose = [[input[j][i] for j in range(len(input))] for i in range(len(input[0]))]
    horizontal_mirror = find_mirror(input)
    vertical_mirror = find_mirror(transpose)
    output += 100 * horizontal_mirror + vertical_mirror

# PRINT
# =====
print(output)

