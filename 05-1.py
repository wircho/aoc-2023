# INPUT
# =====

INPUT_PATH = 'inputs/05.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

# SOLUTION
# ========

current_name = None
def process_line(line):
    global current_name
    if not line.strip():
        if current_name:
            return f'  return x\n\nseeds = list(map({current_name}, seeds))\n'
        else:
            return ''
    elif 'seeds:' in line:
        seeds = list(map(int, line.split()[1:]))
        return f'seeds = {seeds}'
    elif 'map:' in line:
        name = line.split()[0].replace('-', '_')
        current_name = name
        return f'def {name}(x):'
    elif line:
        destination, source, length = line.split()
        return f'  if {source} <= x < {source} + {length}: return {destination} + x - {source}'

lines = list(map(process_line, (input + '\n\n').splitlines()))
code = '\n'.join(lines)

g = {}
exec(code, g)

output = min(g['seeds'])

# PRINT
# =====

print(output)
