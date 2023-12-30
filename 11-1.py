# INPUT
# =====

INPUT_PATH = 'inputs/11.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======


# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]

def insert_voids():
    global input
    i = 0
    while True:
        if '#' not in input[i]:
            input.insert(i, ['.'] * len(input[0]))
            i += 1
        i += 1
        if i == len(input): break
    

def transpose():
    global input
    input = list(map(list, zip(*input)))

def sum_of_all_pairwise_differences(numbers):
    return sum(abs(numbers[i] - numbers[j]) for i in range(len(numbers)) for j in range(i + 1, len(numbers)))


insert_voids()
transpose()
insert_voids()
transpose()

galaxy_is = []
galaxy_js = []

for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] == '#':
            galaxy_is.append(i)
            galaxy_js.append(j)

galaxy_is.sort()
galaxy_js.sort()

output = sum_of_all_pairwise_differences(galaxy_is) + sum_of_all_pairwise_differences(galaxy_js)

# PRINT
# =====
print(output)

