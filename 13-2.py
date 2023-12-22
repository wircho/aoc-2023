# INPUT
# =====

INPUT_PATH = 'inputs/13.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

inputs = input.split("\n\n")
inputs = [tuple(tuple(line) for line in box.splitlines()) for box in inputs]

def find_mirror(matrix):
    diff_d_is = []
    for i in range(1, len(matrix)):
        ds = range(1, min(i + 1, len(matrix) - i + 1))
        different_ds = []
        for d in ds:
            if matrix[i - d] != matrix[i + d - 1]:
                different_ds.append(d)
            if len(different_ds) > 1:
                break
        else:
            if len(different_ds) == 0:
                continue
            else:
                diff_d_is.append((i, different_ds[0]))
            
    for i, d in diff_d_is:
        if sum(matrix[i - d][j] != matrix[i + d - 1][j] for j in range(len(matrix[i]))) != 1:
            continue
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

