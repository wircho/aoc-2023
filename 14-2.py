# INPUT
# =====

INPUT_PATH = 'inputs/14.txt'
with open(INPUT_PATH) as file: input = file.read()

# SOLUTION
# ========

class Matrix:
    def __init__(self, input):
        self.data = tuple(tuple(line) for line in input.splitlines())

    def column_view(self):
        columns = [''.join([self.data[j][i] for j in range(len(self.data))]) for i in range(len(self.data[0]))]
        columns = [[(len(r), r.count("O")) for r in c.split('#')] for c in columns]
        return columns

    def tilt_north(self):
        columns = self.column_view()
        output = 0
        tilted_columns = []
        for column in columns:
            tilted_column = []
            first_chunk = True
            for chunk in column:
                length, count = chunk
                if not first_chunk: tilted_column.append("#")
                tilted_column.extend(["O"] * count + ["."] * (length - count))
                first_chunk = False
            tilted_columns.append(tilted_column)
        self.data = tuple(tuple(tilted_columns[j][i] for j in range(len(tilted_columns))) for i in range(len(tilted_columns[0])))

    def north_load(self):
        load = 0
        for i, line in enumerate(self.data):
            for char in line:
                if char == 'O':
                    load += len(self.data) - i
        return load

    def rotate_cw(self):
        self.data = tuple(tuple(reversed(line)) for line in zip(*self.data))

    def cycle(self):
        self.tilt_north()
        self.rotate_cw()
        self.tilt_north()
        self.rotate_cw()
        self.tilt_north()
        self.rotate_cw()
        self.tilt_north()
        self.rotate_cw()
        
matrix = Matrix(input)
datas = {matrix.data: 0}
north_loads = {0: matrix.north_load()}
i = 0
h = None
while True:
    i += 1
    matrix.cycle()
    if matrix.data in datas:
        h = datas[matrix.data]
        break
    datas[matrix.data] = i
    north_loads[i] = matrix.north_load()

num_cycles = 1000000000
equivalent_cycle_index = h + ((num_cycles - h) % (i - h))
output = north_loads[equivalent_cycle_index]

# PRINT
# =====
print(output)

