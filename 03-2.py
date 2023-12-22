# INPUT
# =====

INPUT_PATH = 'inputs/03.txt'
with open(INPUT_PATH) as file: input = file.readlines()

# SOLUTION
# ========

def update_digit_set(text, i, j, digit_set, range_set):
    if not text[i][j].isdigit() or (i, j) in digit_set: return None
    digit_set.add((i, j))
    r0, r1 = j, j + 1
    while r0 > 0 and text[i][r0 - 1].isdigit():
        r0 -= 1
        digit_set.add((i, r0))
    while r1 < len(text[i]) and text[i][r1].isdigit():
        digit_set.add((i, r1))
        r1 += 1
    range_set.append((i, (r0, r1)))

output = 0
for i in range(len(input)):
    for j in range(len(input[i])):
        if input[i][j] != '*': continue
        digit_set, range_set = set(), []
        for a in range(max(0, i - 1), min(len(input), i + 2)):
            for b in range(max(0, j - 1), min(len(input[a]), j + 2)):
                update_digit_set(input, a, b, digit_set, range_set)
                if len(range_set) > 2: break
        if len(range_set) != 2: continue
        output += int(input[range_set[0][0]][range_set[0][1][0]:range_set[0][1][1]]) \
            * int(input[range_set[1][0]][range_set[1][1][0]:range_set[1][1][1]])
    

# PRINT
# =====

print(output)
