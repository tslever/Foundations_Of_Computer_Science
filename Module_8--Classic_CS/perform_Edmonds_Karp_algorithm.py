from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


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


dictionary_of_nodes_and_positions = {
    "s": (30, -142),
    "1": (192, -29),
    "2": (192, -273),
    "3": (401, -29),
    "4": (401, -273),
    "t": (549, -142)
}


list_of_directed_edges_with_capacities = [
    ("s", "u", 10),
    #("s", "v", 10),
    ("s", "a", 10),

    ("a", "b", 10),

    ("b", "v", 10),

    #("u", "t", 10),
    ("u", "c", 10),

    ("c", "d", 10),

    ("d", "t", 10),

    ("u", "v", 1),

    ("v", "t", 10)
]


dictionary_of_nodes_and_positions = {
    "a": (0, -3),
    "b": (1, -4),
    "c": (3, 0),
    "d": (4, -1),
    "s": (1, -2),
    "t": (3, -2),
    "u": (2, -1),
    "v": (2, -3)
}


def make_initial_network():
    print("We define a directed graph.")
    graph = nx.DiGraph()
    for u, v, capacity in list_of_directed_edges_with_capacities:
        graph.add_edge(u, v, capacity = capacity, flow = 0)
    return graph


def draw_flow_network(graph, title, ax):
    dictionary_of_edges_flows_and_capacities = {
        (u, v): f"{data['flow']} / {data['capacity']}"
        for u, v, data in graph.edges(data = True)
    }
    nx.draw_networkx_nodes(
        graph,
        dictionary_of_nodes_and_positions,
        node_color = "lightgrey",
        ax = ax
    )
    nx.draw_networkx_labels(
        graph,
        dictionary_of_nodes_and_positions,
        ax = ax
    )
    nx.draw_networkx_edges(
        graph,
        dictionary_of_nodes_and_positions,
        arrowstyle = "->",
        arrowsize = 15,
        ax = ax
    )
    nx.draw_networkx_edge_labels(
        graph,
        dictionary_of_nodes_and_positions,
        edge_labels = dictionary_of_edges_flows_and_capacities,
        ax = ax
    )
    ax.set_title(title)
    ax.axis("off")


def build_residual_network(graph):
    residual_network = nx.DiGraph()
    for u, v, data in graph.edges(data = True):
        capacity = data["capacity"]
        flow = data["flow"]
        residual_capacity = capacity - flow
        if residual_capacity > 0:
            residual_network.add_edge(u, v, capacity = residual_capacity, forward = True)
        if flow > 0:
            residual_network.add_edge(v, u, capacity = flow, forward = False)
    return residual_network


def draw_residual_network(residual_network, title, ax, augmentation_path = None):
    list_of_forward_edges = [
        (u, v) for u, v, data in residual_network.edges(data = True) if data["forward"]
    ]
    list_of_backward_edges = [
        (u, v) for u, v, data in residual_network.edges(data = True) if not data["forward"]
    ]
    nx.draw_networkx_nodes(
        residual_network,
        dictionary_of_nodes_and_positions,
        node_color = "lightgrey",
        ax = ax
    )
    nx.draw_networkx_labels(
        residual_network,
        dictionary_of_nodes_and_positions,
        ax = ax
    )
    nx.draw_networkx_edges(
        residual_network,
        dictionary_of_nodes_and_positions,
        edgelist = list_of_forward_edges,
        edge_color = "green",
        arrowstyle = "->",
        arrowsize = 15,
        width = 2,
        connectionstyle = "arc3,rad=0.0",
        ax = ax
    )
    nx.draw_networkx_edges(
        residual_network,
        dictionary_of_nodes_and_positions,
        edgelist = list_of_backward_edges,
        edge_color = "blue",
        arrowstyle = "->",
        arrowsize = 15,
        width = 2,
        connectionstyle = "arc3,rad=0.17",
        ax = ax
    )
    if augmentation_path:
        nx.draw_networkx_edges(
            residual_network,
            dictionary_of_nodes_and_positions,
            edgelist = augmentation_path,
            edge_color = "purple",
            width = 2,
            arrowstyle = "->",
            arrowsize = 15,
            ax = ax,
            connectionstyle = "arc3,rad=0.2"
        )
    dictionary_of_forward_edges_and_capacities = {
        edge: f"{residual_network.edges[edge]["capacity"]}" for edge in list_of_forward_edges
    }
    dictionary_of_backward_edges_and_capacities = {
        edge: f"{residual_network.edges[edge]["capacity"]}" for edge in list_of_backward_edges
    }
    nx.draw_networkx_edge_labels(
        residual_network,
        dictionary_of_nodes_and_positions,
        edge_labels = dictionary_of_forward_edges_and_capacities,
        label_pos = 0.7,
        font_color = "green",
        ax = ax
    )
    nx.draw_networkx_edge_labels(
        residual_network,
        dictionary_of_nodes_and_positions,
        edge_labels = dictionary_of_backward_edges_and_capacities,
        label_pos = 0.7,
        font_color = "blue",
        ax = ax
    )
    ax.set_title(title)
    ax.axis("off")


def draw_side_by_side(graph, residual_network, title_of_flow_network, title_of_residual_network, augmentation_path = None):
    _, (ax_left, ax_right) = plt.subplots(1, 2, figsize = (12, 4))
    draw_flow_network(
        graph,
        title_of_flow_network,
        ax_left
    )
    draw_residual_network(
        residual_network,
        title_of_residual_network,
        ax_right,
        augmentation_path
    )
    plt.tight_layout()
    plt.show()


def perform_Breadth_First_Search(residual_network, s, t):
    dictionary_of_nodes_and_parents = {s: None}
    queue = deque([s])
    while queue and t not in dictionary_of_nodes_and_parents:
        u = queue.popleft()
        for v in residual_network.successors(u):
            if v not in dictionary_of_nodes_and_parents and residual_network[u][v]["capacity"] > 0:
                dictionary_of_nodes_and_parents[v] = u
                queue.append(v)
    if t not in dictionary_of_nodes_and_parents:
        return None, 0
    path = []
    capacity_of_bottleneck = float("inf")
    v = t
    while v != s:
        u = dictionary_of_nodes_and_parents[v]
        path.append((u, v))
        capacity_of_bottleneck = min(capacity_of_bottleneck, residual_network[u][v]["capacity"])
        v = u
    path.reverse()
    return path, capacity_of_bottleneck


def perform_Depth_First_Search(residual_network, s, t):
    path_so_far = []
    stack = [(s, path_so_far)]
    set_of_visited_nodes = set()
    while stack:
        u, path_so_far = stack.pop()
        if u == t:
            capacity_of_bottleneck = min(residual_network[edge[0]][edge[1]]["capacity"] for edge in path_so_far)
            return path_so_far, capacity_of_bottleneck
        if u in set_of_visited_nodes:
            continue
        set_of_visited_nodes.add(u)
        for v in residual_network.successors(u):
            if v not in set_of_visited_nodes and residual_network[u][v]["capacity"] > 0:
                stack.append((v, path_so_far + [(u, v)]))
    return None, 0


def find_max_flow(graph, s, t, name_of_algorithm, we_should_visualize):
    iteration  = 0
    max_flow = 0
    while True:
        print(f"We begin iteration {iteration} of {name_of_algorithm} with current max flow {max_flow}.")
        print("We build a residual network.")
        residual_network = build_residual_network(graph)
        if we_should_visualize:
            print("We visualize the main network and the residual network.\n")
            draw_side_by_side(
                graph,
                residual_network,
                f"Flow Network At Beginning Of Iteration {iteration} Of\n{name_of_algorithm}",
                f"Residual Network At Beginning Of Iteration {iteration} Of\n{name_of_algorithm}"
            )
        if name_of_algorithm == "Edmonds-Karp Algorithm":
            print("We perform Breadth First Search to find an augmentation path in the residual network.")
            augmentation_path, capacity_of_bottleneck = perform_Breadth_First_Search(residual_network, s, t)
        elif name_of_algorithm == "Ford-Fulkerson Algorithm":
            print("We perform Depth First Search to find an augmentation path in the residual network.")
            augmentation_path, capacity_of_bottleneck = perform_Depth_First_Search(residual_network, s, t)
        else:
            raise Exception(f"{name_of_algorithm} is unsupported.")
        if augmentation_path:
            list_of_nodes = [edge[0] for edge in augmentation_path]
            list_of_nodes.append(augmentation_path[len(augmentation_path) - 1][1])
            print(f"The augmentation path is [{', '.join(list_of_nodes)}].")
            print(f"The capacity of the bottleneck is {capacity_of_bottleneck}.")
        else:
            print("No augmentation path exists.")
            break
        for u, v in augmentation_path:
            if graph.has_edge(u, v):
                print(f"We add the capacity of the bottleneck of our augmentation path to edge ({u}, {v}) in our main network.")
                graph[u][v]["flow"] += capacity_of_bottleneck
            elif graph.has_edge(v, u):
                print(f"We subtract the capacity of the bottleneck of our augmentation path from edge ({v}, {u}) in our main network.")
                graph[v][u]["flow"] -= capacity_of_bottleneck
            else:
                raise Exception(f"Both edges (u, v) and (v, u) do not exist.")
        max_flow += capacity_of_bottleneck
        print(f"We increase max flow to {max_flow}.")
        if we_should_visualize:
            print("We visualize the main network and the residual network.\n")
            draw_side_by_side(
                graph,
                residual_network,
                f"Flow Network At End Of Iteration {iteration} Of\n{name_of_algorithm}",
                f"Residual Network At End Of Iteration {iteration} Of\n{name_of_algorithm}",
                augmentation_path
            )
        iteration += 1
    print(f"The maximum flow from s to t / over the graph per the {name_of_algorithm} is {max_flow}.\n")
    return max_flow

print("We perform the Edmonds Karp algorithm.")
maximum_flow_from_s_to_t = find_max_flow(make_initial_network(), "s", "t", "Edmonds-Karp Algorithm", we_should_visualize = True)
maximum_flow_from_s_to_t = find_max_flow(make_initial_network(), "s", "t", "Ford-Fulkerson Algorithm", we_should_visualize = True)