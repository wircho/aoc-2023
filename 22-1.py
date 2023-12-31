# INPUT
# =====

INPUT_PATH = 'inputs/22.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======


# SOLUTION
# ========

class Brick:
    cube_map = {}

    def __init__(self, line):
        if '<-' in line:
            line, name = line.split('<-')
            self.name = name
        else:
            self.name = line
        ends = [tuple(map(int, end.split(','))) for end in line.split('~')]
        assert len(ends) == 2 and len(ends[0]) == 3 and len(ends[1]) == 3
        diffs = [i for i in range(3) if ends[0][i] != ends[1][i]]
        if diffs:
            assert len(diffs) == 1
            diff = diffs[0]
            if ends[0][diff] > ends[1][diff]: ends = [ends[1], ends[0]]
            self.cubes = [tuple(t if j == diff else ends[0][j] for j in range(3)) for t in range(ends[0][diff], ends[1][diff] + 1)]
        else:
            self.cubes = [ends[0]]
        for cube in self.cubes:
            Brick.cube_map[cube] = self
        self.supported_bricks = set()
        self.supported_by = set()

    def __hash__(self) -> int:
        return hash(tuple(self.cubes))
    
    def __eq__(self, o: object) -> bool:
        return o and self.cubes == o.cubes

    @property
    def bottom(self):
        bottom_z = min(cube[2] for cube in self.cubes)
        return [cube for cube in self.cubes if cube[2] == bottom_z]
    
    @property
    def top(self):
        top_z = max(cube[2] for cube in self.cubes)
        return [cube for cube in self.cubes if cube[2] == top_z]

    def lower(self):
        cubes = []
        for cube in self.cubes:
            if cube[2] == 1: return False
            new_cube = tuple(cube[i] - 1 if i == 2 else cube[i] for i in range(3))
            brick = Brick.cube_map.get(new_cube)
            if brick and brick != self: return False
            cubes.append(new_cube)
        for cube in self.cubes: Brick.cube_map.pop(cube)
        for cube in cubes: Brick.cube_map[cube] = self
        self.cubes = cubes
        return True

    def drop(self):
        any_lower = False
        while True:
            if not self.lower(): return any_lower
            any_lower = True

    def update_supports(self):
        for cube in self.top:
            brick = Brick.cube_map.get((cube[0], cube[1], cube[2] + 1))
            assert brick != self
            if not brick: continue
            self.supported_bricks.add(brick)
            brick.supported_by.add(self)

    def __repr__(self) -> str:
        return f"{self.name} {self.cubes}"

bricks = sorted([Brick(line) for line in input.splitlines()], key=lambda brick: brick.bottom[0][2])

while True:
    any_drop = False
    for brick in bricks:
         dropped = brick.drop()
         any_drop = any_drop or dropped
    if not any_drop: break

for brick in bricks:
    brick.update_supports()

useless_bricks = []
for brick in bricks:
    if any(len(supported_brick.supported_by) <= 1 for supported_brick in brick.supported_bricks): continue
    useless_bricks.append(brick)

output = len(useless_bricks)

# PRINT
# =====
print(output)

