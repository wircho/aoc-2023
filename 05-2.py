

# INPUT
# =====

INPUT_PATH = 'inputs/05.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

# SOLUTION
# ========

class Range:
    def __init__(self, start, end, locked):
        self.start = start
        self.end = end
        self.is_empty = start > end
        self.locked = locked

    @staticmethod
    def range_and_offset_from_parameters(destination, source, length):
        return Range.from_start_and_length(source, length), destination - source
    
    @staticmethod
    def from_start_and_length(start, length):
        return Range(start, start + length - 1, False)

    @staticmethod
    def list_from_starts_and_lengths(seeds):
        return [Range.from_start_and_length(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    
    @staticmethod
    def apply_to_many(ranges, other, offset):
        applied_ranges = [s for r in ranges for s in r.apply(other, offset)]
        result = Range.simplify_list(applied_ranges)
        return result
    
    @staticmethod
    def simplify_list(ranges):
        final_result = []
        for locked in [False, True]:
            result = []
            specific_ranges = [r for r in ranges if r.locked == locked]
            specific_ranges = sorted(specific_ranges, key=lambda r: r.start)
            for range in specific_ranges:
                if range.is_empty: continue
                if result and range.start <= result[-1].end:
                    result[-1] = Range(result[-1].start, max(result[-1].end, range.end), locked)
                else:
                    result.append(range)
            final_result = final_result + result
        return final_result
    
    @staticmethod
    def unlock_list(ranges):
        return [r.unlock() for r in ranges]

    def shift(self, offset):
        return Range(self.start + offset, self.end + offset, self.locked)
    
    def unlock(self):
        return Range(self.start, self.end, False)
    
    def apply(self, other, offset):
        if self.is_empty: return []
        if self.locked: return [self]
        lhs = Range(self.start, min(other.start - 1, self.end), False)
        rhs = Range(max(other.end + 1, self.start), self.end, False)
        intersection = Range(max(self.start, other.start), min(self.end, other.end), True).shift(offset)
        result = []
        if not lhs.is_empty: result.append(lhs)
        if not rhs.is_empty: result.append(rhs)
        if not intersection.is_empty: result.append(intersection)
        return result
    
    def __repr__(self):
        return f'Range({self.start}, {self.end}, {self.locked})'
        

current_name = None
def process_line(line):
    global current_name
    if not line.strip():
        if current_name:
            return f'  x = Range.unlock_list(x)\n  return x\n\nranges = {current_name}(ranges)\n'
        else:
            return ''
    elif 'seeds:' in line:
        seeds = list(map(int, line.split()[1:]))
        return f'ranges = Range.simplify_list(Range.list_from_starts_and_lengths({seeds}))'
    elif 'map:' in line:
        name = line.split()[0].replace('-', '_')
        current_name = name
        return f'def {name}(x):'
    elif line:
        destination, source, length = line.split()
        return f'  x = Range.apply_to_many(x, *Range.range_and_offset_from_parameters({destination}, {source}, {length}))'

lines = list(map(process_line, (input + '\n\n').splitlines()))
code = '\n'.join(lines)

g = {'Range': Range}
exec(code, g)

output = min(range.start for range in g['ranges'] if not range.is_empty)

# PRINT
# =====

print(output)