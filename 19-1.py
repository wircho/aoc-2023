# INPUT
# =====

INPUT_PATH = 'inputs/19.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re
from unittest.mock import Mock

# SOLUTION
# ========

workflows, ratings = input.split('\n\n')
workflows = workflows.splitlines()
ratings = ratings.splitlines()

def process_workflow(workflow):
    return re.sub(r'([a-z]+)\{(.*)\}', lambda m: 'def ' + m.group(1) + '_(y): return ' + process_body(m.group(2)), workflow)

def process_body(body):
    return ' or '.join(map(process_rule, body.split(',')))

def process_rule(rule):
    rule = rule.replace(':', ' and ')
    rule = re.sub(r'([xmas](?:<|>))', r'y.\1', rule)
    rule += "_(y)"
    return rule

def process_rating(rating):
    return re.sub(r'\{(.*)\}', r'output += in_(Mock(\1))', rating)

for i in range(len(workflows)):
    workflows[i] = process_workflow(workflows[i])

for i in range(len(ratings)):
    ratings[i] = process_rating(ratings[i])

g = {"Mock": Mock}

code = """
output = 0
def A_(y): return y.x + y.m + y.a + y.s + 1
def R_(y): return 1
""" + "\n".join(workflows) + """
""" + "\n".join(ratings)

exec(code, g)
output = g["output"] - len(ratings)

# PRINT
# =====
print(output)

