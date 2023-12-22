# INPUT
# =====

INPUT_PATH = 'inputs/01.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re

# SOLUTION
# ========

pattern = re.compile(r'(\d|\n)')
output, line = 0, []
for match in pattern.finditer(input + '\n'):
    if match.group(0) == '\n': output, line = output + 10 * line[0] + line[-1], []
    else: line = line[:1] + [int(match.group(0))]

# PRINT
# =====

print(output)
