# INPUT
# =====

INPUT_PATH = 'inputs/19.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re
from itertools import product
import time

# SOLUTION
# ========

workflows, _ = input.split('\n\n')
workflows = workflows.splitlines()

def process_workflow(workflow):
    return re.sub(r'([a-z]+)\{(.*)\}', lambda m: 'def ' + m.group(1) + '_(y): return ' + process_body(m.group(2)), workflow)

def process_body(body):
    return ','.join(map(process_rule, body.split(','))) + ')' * body.count(':')

def process_rule(rule):
    rule = rule.replace(':', '.branch(')
    rule = re.sub(r'([xmas](?:<|>))', r'y.\1', rule)
    rule += "_(y)"
    rule = re.sub(r'([^ ]+(?:<|>)[0-9]+)', r'(\1)', rule)
    return rule

def process_rating(rating):
    return re.sub(r'\{(.*)\}', r'output += in_(Mock(\1))', rating)

for i in range(len(workflows)):
    workflows[i] = process_workflow(workflows[i])

class ConditionSet:
    def __init__(self, conditions_list):
        self.conditions_list = conditions_list

    def __or__(self, other):
        if isinstance(other, ConditionSet):
            return ConditionSet(self.conditions_list + other.conditions_list)
        elif isinstance(other, Conditions):
            return ConditionSet(self.conditions_list + [other])
        else:
            assert False

class Conditions:
    def __init__(self, prop_names, ops, values):
        self.prop_names = prop_names
        self.ops = ops
        self.values = values
    
    def negate(self):
        assert len(self.prop_names) == 1
        assert self.ops[0] in ['<', '>']
        if self.ops[0] == '<':
            return Conditions(self.prop_names, ['>'], [self.values[0] - 1])
        elif self.ops[0] == '>':
            return Conditions(self.prop_names, ['<'], [self.values[0] + 1])
    
    def branch(self, if_true, if_false):
        return (self & if_true) | (self.negate() & if_false)

    def __and__(self, other):
        if isinstance(other, Conditions):
            return Conditions(self.prop_names + other.prop_names, self.ops + other.ops, self.values + other.values)
        elif isinstance(other, ConditionSet):
            return ConditionSet([self & a for a in other.conditions_list])
        else:
            assert False

    def __or__(self, other):
        if isinstance(other, Conditions):
            return ConditionSet([self, other])
        elif isinstance(other, ConditionSet):
            return ConditionSet([self] + other.conditions_list)
        else:
            assert False

class Prop:
    def __init__(self, name):
        self.name = name

    def __lt__(self, number):
        return Conditions([self.name], ['<'], [number])

    def __gt__(self, number):
        return Conditions([self.name], ['>'], [number])

class Rating:
    @property
    def x(self): return Prop("x")

    @property
    def m(self): return Prop("m")

    @property
    def a(self): return Prop("a")

    @property
    def s(self): return Prop("s")

    @property
    def accept(self): return Conditions(["accept"], ["="], [None])

    @property
    def reject(self): return Conditions(["reject"], ["="], [None])

g = {"Rating": Rating}

code = """
def A_(y): return y.accept
def R_(y): return y.reject
y = Rating()
""" + "\n".join(workflows) + """
result = in_(y)
"""

exec(code, g)

result = g["result"]

assert isinstance(result, ConditionSet)

accept_conditions = [conditions for conditions in result.conditions_list if conditions.prop_names[-1] == 'accept']

output = 0

for conditions in accept_conditions:
    lower_bounds = {'x': 0, 'm': 0, 'a': 0, 's': 0}
    upper_bounds = {'x': 4001, 'm': 4001, 'a': 4001, 's': 4001}
    for i in range(len(conditions.prop_names) - 1):
        prop_name = conditions.prop_names[i]
        op = conditions.ops[i]
        value = conditions.values[i]
        if op == '<':
            upper_bounds[prop_name] = min(upper_bounds[prop_name], value)
        elif op == '>':
            lower_bounds[prop_name] = max(lower_bounds[prop_name], value)
        else:
            assert False
    output += max(upper_bounds['x'] - lower_bounds['x'] - 1, 0) * max(upper_bounds['m'] - lower_bounds['m'] - 1, 0) * max(upper_bounds['a'] - lower_bounds['a'] -1, 0) * max(upper_bounds['s'] - lower_bounds['s'] - 1, 0)

# PRINT
# =====
print(output)

