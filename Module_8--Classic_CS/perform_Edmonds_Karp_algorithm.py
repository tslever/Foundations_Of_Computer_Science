import matplotlib.pyplot as plt
import networkx as nx


list_of_directed_edges = [
    ("s", "1", 16),
    ("s", "2", 12),

    ("1", "3", 12),

    ("2", "1", 4),
    ("2", "4", 14),

    ("3", "2", 9),
    ("3", "t", 20),

    ("4", "3", 7),
    ("4", "t", 4)
]


# Lay out the undirected graph.
dictionary_of_nodes_and_positions = {
    "s": (30, -142),
    "1": (192, -29),
    "2": (192, -273),
    "3": (401, -29),
    "4": (401, -273),
    "t": (549, -142)
}


graph = nx.DiGraph()
graph.add_weighted_edges_from(list_of_directed_edges, weight = "capacity")

dictionary_of_edges_and_capacities = {(u, v): data["capacity"] for u, v, data in graph.edges(data = True)}
nx.draw_networkx_nodes(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_labels(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_edges(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_edge_labels(graph, dictionary_of_nodes_and_positions, dictionary_of_edges_and_capacities)
plt.show()