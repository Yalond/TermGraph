import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import termgraph

def linspace(low, high, amount):
    return [low + (high - low) * (i/amount) for i in range(amount)]

x = linspace(-10, 10, 200)
y1 = [xi ** 2 for xi in x]
y2 = [xi ** 3 for xi in x]

termgraph.plot([x, y1], (5, 2))
termgraph.plot([x, y1], (20, 5))
termgraph.plot([x, y1], (30, 10))

termgraph.plot([x, y1, x, y2], (30, 5))

