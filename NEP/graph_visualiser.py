import rdflib
import networkx as nx
import matplotlib.pyplot as plt

# Load RDF data from a Turtle file
g = rdflib.Graph()
g.parse("output.ttl", format="turtle")

# Create a NetworkX graph from the RDF data
nx_graph = nx.DiGraph()

for s, p, o in g:
    nx_graph.add_node(s)
    nx_graph.add_node(o)
    nx_graph.add_edge(s, o, label=p)

# Visualize the graph
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(nx_graph)
nx.draw(nx_graph, pos, with_labels=True, node_size=3000, font_size=10, node_color="skyblue", edge_color="gray", arrowsize=20)
nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels={(u, v): d['label'] for u, v, d in nx_graph.edges(data=True)})
plt.show()
