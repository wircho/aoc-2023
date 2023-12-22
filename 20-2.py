# INPUT
# =====

INPUT_PATH = 'inputs/20.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import re
from itertools import product
import time
import inspect
from math import lcm

# SOLUTION
# ========

def process_module(line):
    first = re.search('[a-z]+', line).group()
    line = re.sub(r'([a-z]+)', r'\1_', line)
    line = line.replace(' -> ', f'(pulse): Outs({first}_, ')
    line += ',)'
    if line.startswith('%'):
        line = line[1:] + '.flip_flop(pulse)'
    elif line.startswith('&'):
        line = line[1:] + '.conjunction(pulse)'
    else:
        assert line.startswith('broadcaster')
        line += '.broadcast(pulse)'
    line = 'def ' + line
    return line

modules = [process_module(line) for line in input.splitlines()]
modules_code = '\n'.join(modules)

info = {'mock': False, 'queue': [], True: 0, False: 0, 'history': {}}
mock_called = set()
class Outs:
    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def flip_flop(self, pulse):
        if info['mock']:
            if self.function.__name__ in mock_called:
                pass
            else:
                mock_called.add(self.function.__name__)
                self.function.kind = 'flip_flop'
                self.function.state = False
                for arg in self.args: arg(pulse)
        else:
            _, pulse = pulse
            if pulse: return
            self.function.state = not self.function.state
            info['queue'].extend([(self.function, self.function.state, arg) for arg in self.args])

    def conjunction(self, pulse):
        if info['mock']:
            if self.function.__name__ in mock_called:
                pass
            else:
                mock_called.add(self.function.__name__)
                self.function.kind = 'conjunction'
                self.function.state = {}
                for arg in self.args: arg(pulse)
            stack = inspect.stack()
            caller_function_name = stack[3][3]
            self.function.state[caller_function_name] = False
        else:
            caller, pulse = pulse
            stack = inspect.stack()
            self.function.state[caller.__name__] = pulse
            if all(self.function.state.values()):
                info['queue'].extend([(self.function, False, arg) for arg in self.args])
            else:
                info['queue'].extend([(self.function, True, arg) for arg in self.args])

    def broadcast(self, pulse):
        if info['mock']:
            if self.function.__name__ in mock_called:
                pass
            else:
                mock_called.add(self.function.__name__)
                self.function.kind = 'broadcast'
                for arg in self.args: arg(pulse)
        else:
            _, pulse = pulse
            info['queue'].extend([(self.function, pulse, arg) for arg in self.args])

def press_button(broadcaster_, button_press_number):
    info['queue'] = [(None, False, broadcaster_)]
    while len(info['queue']) > 0:
        queue = info['queue']
        info['queue'] = []
        for caller, pulse, f in queue:
            info[pulse] += 1
            # print(f"{caller.__name__ if caller else None} -{pulse}-> {f.__name__}")
            info['history'].setdefault(f.__name__, {}).setdefault(button_press_number, []).append((caller.__name__ if caller else 'None', pulse))
            f((caller, pulse))


g = {'Outs': Outs, 'info': info, 'press_button': press_button}

code = """
info['mock'] = True
def rx_(pulse): pass # This is the output
def output_(pulse): pass  # This is the output
""" + modules_code + """
broadcaster_(None)
info['mock'] = False
for i in range(10000):
    press_button(broadcaster_, i)
"""

exec(code, g)

# Not proud, but I did this manually. After 10000 steps, I look at the history of x_'s upstream (ns_):

# > set(item[0] for i in range(10000) for item in info['history']['ns_'][i])  # list upstreams
upstreams = ['dc_', 'vp_', 'cq_', 'rv_']

# > any_true = [any(x[1] for x in info['history']['ns_'][i]) for i in range(10000)]
# > any_true_index = [i for i in range(10000) if any_true(i)]
any_true_index = [3796, 3846, 3876, 4050, 7593, 7693, 7753, 8101]

# I noticed that these upstreams get a high (True) pulse at regular intervals given by the first
# numbers above (we need to add 1 because the first button press is 0):
output = lcm(*(x + 1 for x in any_true_index[:4]))

# PRINT
# =====
print(output)

