import matplotlib.pyplot as plt
import networkx as nx


list_of_directed_edges_with_capacities = [
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
graph.add_weighted_edges_from(list_of_directed_edges_with_capacities, weight = "capacity")

maximum_flow_from_s_to_t, dictionary_of_edges_and_flows = nx.maximum_flow(
    graph,
    "s",
    "t",
    flow_func = nx.algorithms.flow.edmonds_karp
)
dictionary_of_edges_and_flows = {(u, v): dictionary_of_edges_and_flows[u].get(v, 0) for u, v, _ in list_of_directed_edges_with_capacities}
dictionary_of_edges_flows_and_capacities = {
    (u, v):  f"{dictionary_of_edges_and_flows[(u, v)]}/{capacity}"
    for u, v, capacity in list_of_directed_edges_with_capacities
}

print("The dictionary of edges, flows, and capacities corresponding to the maximum flow from s to t / over the graph is")
print(dictionary_of_edges_flows_and_capacities)
print(f"The maximum flow from s to t / over the graph is {maximum_flow_from_s_to_t}.")
print(
    "For every node v that is not source or sink, the flow-conservation constraint applies.\n" +
    "The sum along all edges ending with v of all inflows to v is equal to " +
    "the sum along all edges starting with v of all outflows from v.\n" +
    "The net flow of v is the difference between the inflow and the outflow.\n" +
    "Since the inflow and outflow of v are equal, the net flow of v is 0."
)

nx.draw_networkx_nodes(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_labels(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_edges(graph, dictionary_of_nodes_and_positions)
nx.draw_networkx_edge_labels(graph, dictionary_of_nodes_and_positions, dictionary_of_edges_flows_and_capacities)
plt.show()