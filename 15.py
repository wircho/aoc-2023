# INPUT
# =====

INPUT_PATH = 'inputs/15.txt'
with open(INPUT_PATH) as file: input = file.read().strip()

# IMPORTS
# =======

from collections import OrderedDict

# SOLUTION
# ========

hashes = {}
def hash(s):
    if s in hashes: return hashes[s]
    h = 0
    for c in s:
        a = ord(c)
        h = ((h + a) * 17) % 256
    hashes[s] = h
    return h

input = input.split(',')
boxes = {}
for step in input:
    if step[-1] == '-':
        label = step[:-1]
        box_number = hash(label)
        boxes.setdefault(box_number, OrderedDict()).pop(label, None)
    else:
        label, f = step.split('=')
        box_number, focal_length = hash(label), int(f)
        boxes.setdefault(box_number, OrderedDict()).update({label: focal_length})

output = sum([(box_number + 1) * (slot_number + 1) * focal_length for box_number, box in boxes.items()
 for (slot_number, (label, focal_length)) in enumerate(box.items())])
        

# PRINT
# =====

print(output)
