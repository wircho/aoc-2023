# INPUT
# =====

INPUT_PATH = 'inputs/12.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import itertools

# SOLUTION
# ========

output = 0

class Line:
    def __init__(self, record, counts, hint_no_points, hint_no_number_signs):
        self.record = record
        self.counts = counts
        self.hint_no_points = hint_no_points
        self.hint_no_number_signs = hint_no_number_signs

    def __hash__(self) -> int:
        return hash((self.record, self.counts))
    
    def __eq__(self, o: object) -> bool:
        return self.record == o.record and self.counts == o.counts
    

def _factorial(n):
    from math import factorial
    return factorial(n)

factorial_dict = {}
def factorial(n):
    if n not in factorial_dict:
        factorial_dict[n] = _factorial(n)
    return factorial_dict[n]


def _num_arrangements(line):
    if len(line.record) == 0: return int(len(line.counts) == 0)
    if len(line.counts) == 0: return int('#' not in line.record)
    sum_counts = sum(line.counts)
    if sum_counts + len(line.counts) - 1 > len(line.record): return 0
    first_point = -1 if line.hint_no_points else line.record.find('.')
    if first_point == -1:
        first_number_sign = -1 if line.hint_no_number_signs else line.record.find('#')
        if first_number_sign == -1:
            # Assuming records is a series of '?'
            # Assuming counts is a series of positive integers with sum + len <= len(record)
            # - We have a total of len(counts) + 1 gaps
            # - The first and last gap can be 0
            # - The other gaps are >= 1
            # - This is the same as len(counts) + 1 gaps that add up to
            #   len(record) - sum(counts) - (len(counts) - 1)
            item_count = len(line.counts) + 1
            item_sum = len(line.record) - sum_counts - (len(line.counts) - 1)
            # - This is the same as having item_count - 1 bars and item_sum balls
            num_bars = item_count - 1
            num_balls = item_sum
            return factorial(num_bars + num_balls) // (factorial(num_bars) * factorial(num_balls))
        else:
            lhs = line.record[:first_number_sign]
            rhs = line.record[first_number_sign + 1:]
            r_num_number_signs = rhs.count('#')
            l_len_counts = -1
            r_len_counts = len(line.counts)
            l_sum_counts = -line.counts[-1]
            r_sum_counts = sum_counts
            result = 0
            for i in range(len(line.counts)):
                l_len_counts += 1
                r_len_counts -= 1
                l_sum_counts += line.counts[i - 1]
                r_sum_counts -= line.counts[i]
                if r_sum_counts + line.counts[i] - 1 < r_num_number_signs: break
                if l_sum_counts + l_len_counts - 1 > len(lhs) - 1: break
                if r_sum_counts + r_len_counts - 1 > len(rhs) - 1: continue
                for j in range(max(line.counts[i] - len(rhs) - 1, 0), min(len(lhs) + 1, line.counts[i])):
                    # j to the left, and line.counts[i] - 1 - j to the right
                    if line.counts[i] - 1 - j <= len(rhs) - 1 and rhs[line.counts[i] - 1 - j] == '#': continue
                    l_line = Line(lhs[:-j - 1], line.counts[:i], True, True)
                    r_line = Line(rhs[line.counts[i] - j:], line.counts[i + 1:], True, False)
                    result += num_arrangements(l_line) * num_arrangements(r_line)
            return result
    else:
        lhs = line.record[:first_point]
        rhs = line.record[first_point + 1:]
        l_num_number_signs = lhs.count('#')
        r_num_number_signs = rhs.count('#')
        l_len_counts = -1
        r_len_counts = len(line.counts) + 1
        l_sum_counts = -line.counts[-1]
        r_sum_counts = sum_counts + line.counts[-1]
        result = 0
        for i in range(len(line.counts) + 1):
            l_len_counts += 1
            r_len_counts -= 1
            l_sum_counts += line.counts[i - 1]
            r_sum_counts -= line.counts[i - 1]
            if l_sum_counts < l_num_number_signs: continue
            if r_sum_counts < r_num_number_signs: break
            if l_sum_counts + l_len_counts - 1 > len(lhs): break
            if r_sum_counts + r_len_counts - 1 > len(rhs): continue
            l_line = Line(lhs, line.counts[:i], True, False)
            r_line = Line(rhs, line.counts[i:], False, False)
            result += num_arrangements(l_line) * num_arrangements(r_line)
        return result

num_arrangements_dict = {}
def num_arrangements(line):
    if line not in num_arrangements_dict:
        num_arrangements_dict[line] = _num_arrangements(line)
    return num_arrangements_dict[line]

output = 0
multiply_times_5 = True
for line in input.splitlines():
    record, counts = line.split(' ')
    counts = tuple([int(i) for i in counts.split(',')]) if counts else tuple()
    if multiply_times_5:
        record = '?'.join([record] * 5)
        counts = tuple(list(counts) * 5)
    line = Line(record, counts, False, False)
    output += num_arrangements(line)
            
# PRINT
# =====
print(output)
