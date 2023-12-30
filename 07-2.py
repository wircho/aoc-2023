# INPUT
# =====

INPUT_PATH = 'inputs/07.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

# SOLUTION
# ========

coefs = [1, 15, 15 ** 2, 15 ** 3, 15 ** 4, 15 ** 5, 15 ** 6, 15 ** 7, 15 ** 8, 15 ** 9]

def single_card_value(card):
    return ({
        'T': 11,
        'J': 1,
        'Q': 13,
        'K': 14,
        'A': 15,
    }.get(card) or (int(card) + 1)) - 1

def hand_card_value(hand):
    reversed_hand = list(reversed(hand))
    return sum(single_card_value(reversed_hand[i]) * coefs[i] for i in range(len(reversed_hand)))

def hand_repetition_value(hand):
    num_js = hand.count('J')
    hand = hand.replace('J', '')
    reps = []
    while len(hand) > 0:
        card = hand[0]
        reps.append(hand.count(card))
        hand = hand.replace(card, '')
    reps = sorted(reps)
    if reps: reps[-1] += num_js
    else: reps = [num_js]
    while len(reps) < 5: reps.insert(0, 0)
    return sum(reps[i] * coefs[i + 5] for i in range(5))

def hand_value(hand):
    return hand_repetition_value(hand) + hand_card_value(hand)

inputs = [line.split(' ') for line in input.splitlines()]
inputs = [(hand_value(line[0]), int(line[1])) for line in inputs]
inputs = sorted(inputs, key=lambda x: x[0])
output = sum((i + 1) * n for i, (_, n) in enumerate(inputs))

# PRINT
# =====

print(output)

