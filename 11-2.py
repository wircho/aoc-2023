# INPUT
# =====

INPUT_PATH = 'inputs/11.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======


# SOLUTION
# ========

input = [list(line) for line in input.splitlines()]

def compute_voids():
    global input
    return [i for i in range(len(input)) if '#' not in input[i]]
    

def transpose():
    global input
    input = list(map(list, zip(*input)))

def sum_of_all_pairwise_differences(numbers, voids):
    EXTRA_LENGTH = 999999
    extra_lengths = [len([v for v in voids if v < n]) * EXTRA_LENGTH for (i, n) in enumerate(numbers)]
    return sum(abs(numbers[i] + extra_lengths[i] - numbers[j] - extra_lengths[j]) for i in range(len(numbers)) for j in range(i + 1, len(numbers)))


void_is = compute_voids()
transpose()
void_js = compute_voids()
transpose()

galaxy_is = []
galaxy_js = []

for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] == '#':
            galaxy_is.append(i)
            galaxy_js.append(j)

void_is.sort()
void_js.sort()
galaxy_is.sort()
galaxy_js.sort()

output = sum_of_all_pairwise_differences(galaxy_is, void_is) + sum_of_all_pairwise_differences(galaxy_js, void_js)

# PRINT
# =====
print(output)

