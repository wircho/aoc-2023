# INPUT
# =====

INPUT_PATH = 'inputs/03.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re

# SOLUTION
# ========

all_numbers = re.findall(r'\d+', input)
sum_of_all_numbers = sum(int(n) for n in all_numbers)
marked_input = [list(line) for line in input.splitlines()]
input = [list(line) for line in input.splitlines()]
for i in range(len(input)):
    for j in range(len(input[i])):
        if input[i][j].isdigit() or input[i][j] == '.': continue
        for a in range(max(0, i - 1), min(len(input), i + 2)):
            for b in range(max(0, j - 1), min(len(input[a]), j + 2)):
                if input[a][b].isdigit():
                    marked_input[a][b] = 'A'
all_possibly_marked_numbers = re.findall(r'[\dA]+', '\n'.join(''.join(line) for line in marked_input))
all_unmarked_numbers = [n for n in all_possibly_marked_numbers if 'A' not in n]
sum_of_unmarked_numbers = sum(int(n) for n in all_unmarked_numbers)
output = sum_of_all_numbers - sum_of_unmarked_numbers
    

# PRINT
# =====

print(output)
