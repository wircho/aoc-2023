# INPUT
# =====

INPUT_PATH = 'inputs/08.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import sys
from math import lcm

# SOLUTION
# ========

sys.setrecursionlimit(100000)

def process_line(line):
    fname, defs = line.split(' = ')
    left, right = defs.lstrip('(').rstrip(')').split(', ')
    return f"""
def {fname}(x, i, p):
    q = p + [(i % len(x), "{fname}")]
    if (i % len(x), "{fname}") in p: return q
    if x[i % len(x)] == "L": return {left}(x, i + 1, q)
    else: return {right}(x, i + 1, q)
    """

chain, functions = input.split('\n\n')
function_lines = functions.splitlines()
function_lines = [process_line(line) for line in function_lines]
functions = '\n'.join(function_lines)

g = {'chain': chain}
exec(functions, g)

class Loop:
    def __init__(self, name, start_index, size, z_indexes):
        self.name = name
        self.start_index = start_index
        self.size = size
        self.z_indexes = z_indexes

    def __repr__(self) -> str:
        return f'Loop({self.name}, {self.start_index}, {self.size}, {self.z_indexes})'

loops = []
for fname, f in g.items():
    if not fname.endswith('A'): continue
    result = f(chain, 0, [])
    loop_start_index = result.index(result[-1])
    loop_size = len(result) - loop_start_index - 1
    z_indexes = [i for i, (_, name) in enumerate(result) if name.endswith('Z')]
    loop = Loop(fname, loop_start_index, loop_size, z_indexes)
    loops.append(loop)
    print(loop)

# Assumptions:
for loop in loops:
    assert loop.z_indexes == [loop.size]

output = lcm(*[loop.size for loop in loops])

# PRINT
# =====

print(output)

