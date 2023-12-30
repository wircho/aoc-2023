# INPUT
# =====

INPUT_PATH = 'inputs/25.txt'
with open(INPUT_PATH) as file: input = file.read()

# IMPORTS
# =======

import networkx as nx
import matplotlib.pyplot as plt

# SOLUTION
# ========

nodes = set()
edges = set()
lines = input.splitlines()

for line in lines:
    node0, nodes1 = line.split(': ')
    nodes1 = nodes1.split()
    nodes.add(node0)
    for node in nodes1: nodes.add(node)
    for node in nodes1: edges.add(tuple(sorted([node0, node])))

# print(f"Number of nodes: {len(nodes)}")
# print(f"Number of edges: {len(edges)}")
# # VISUALIZATION
# G = nx.Graph()
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)
# nx.draw(G, with_labels=True)
# plt.show()
    
# The visualization above gives us the answer:
lhs = ['frl', 'ccp', 'llm']
rhs = ['fvm', 'thx', 'lhg']
connecting_edges = [tuple(sorted([lhs[i], rhs[j]])) for i in range(len(lhs)) for j in range(len(rhs))]
connecting_edges = set(connecting_edges).intersection(edges)
print(connecting_edges)
assert len(connecting_edges) == 3

# Remove edges
edges = edges.difference(connecting_edges)

# Finding connected component of lhs[0]:
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
lhs0_component = nx.node_connected_component(G, lhs[0])
size_of_lhs0_component = len(lhs0_component)

# Same for rhs:
rhs0_component = nx.node_connected_component(G, rhs[0])
size_of_rhs0_component = len(rhs0_component)

output = size_of_lhs0_component * size_of_rhs0_component


# PRINT
# =====
print(output)

