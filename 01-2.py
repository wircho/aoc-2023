# INPUT
# =====

INPUT_PATH = 'inputs/01.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re

# SOLUTION
# ========

mapping = {**{str(i): i for i in range(10)}, 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
           'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
lookahead_pattern = re.compile("(?=" + "|".join(mapping.keys()) + r"|\n)")
pattern = re.compile("(" + "|".join(mapping.keys()) + r"|\n)")
output, line = 0, []
input += '\n'
for match in lookahead_pattern.finditer(input):
    match = pattern.match(input[match.start():])
    value = mapping.get(match.group(0))
    if value: line = line[:1] + [mapping[match.group(0)]]
    else: output, line = output + 10 * line[0] + line[-1], []


# PRINT
# =====

print(output)
