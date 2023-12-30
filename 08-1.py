# INPUT
# =====

INPUT_PATH = 'inputs/08.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import sys

# SOLUTION
# ========

sys.setrecursionlimit(100000)

def process_line(line):
    line = ('def ' + line
        .replace(', ', '---')
        .replace('(', '')
        .replace(')', '(x, i + 1)')
        .replace(' = ', '(x, i): return ')
        .replace('---', r'(x, i + 1) if x[i % len(x)] == "L" else '))\
        .replace('def ZZZ', 'def ZZZ(x, i): return i  # ')

    return line

chain, functions = input.split('\n\n')
function_lines = functions.splitlines()
function_lines = [process_line(line) for line in function_lines]
functions = '\n'.join(function_lines) + "\noutput = AAA(chain, 0)\n"

g = {'chain': chain}
exec(functions, g)
output = g['output']

# PRINT
# =====

print(output)

