'''
Find the best route from Arad to Bucharest given the following graph and heuristic.
'''


import heapq
import matplotlib.pyplot as plt
import networkx as nx


# Define weighted undirected edges.
list_of_edges = [
    ('Arad', 'Sibiu', 140), # kilometers
    ('Arad', 'Timisoara', 118),
    ('Arad', 'Zerind', 75),

    ('Bucharest', 'Fagaras', 211),
    ('Bucharest', 'Giurgiu', 90),
    ('Bucharest', 'Pitesti', 101),
    ('Bucharest', 'Urziceni', 85),

    ('Craiova', 'Dobreta', 120),
    ('Craiova', 'Pitesti', 138),
    ('Craiova', 'Rimnicu_Vilcea', 146),

    #('Dobreta', 'Craiova', 120),
    ('Dobreta', 'Mehadia', 75),

    ('Eforie', 'Hirsova', 86),

    #('Fagaras', 'Bucharest', 211),
    ('Fagaras', 'Sibiu', 99),
    
    #('Giurgiu', 'Bucharest', 90),

    #('Hirsova', 'Eforie', 86),
    ('Hirsova', 'Urziceni', 98),

    ('Iasi', 'Neamt', 87),
    ('Iasi', 'Vaslui', 92),

    ('Lugoj', 'Mehadia', 70),
    ('Lugoj', 'Timisoara', 111),

    #('Mehadia', 'Lugoj', 70),
    #('Mehadia', 'Dobreta', 75),

    #('Neamt', 'Iasi', 87),

    ('Oradea', 'Sibiu', 151),
    ('Oradea', 'Zerind', 71),

    #('Pitesti', 'Bucharest', 101),
    #('Pitesti', 'Craiova', 138),
    ('Pitesti', 'Rimnicu_Vilcea', 97),

    #('Rimnicu_Vilcea', 'Craiova', 146),
    #('Rimnicu_Vilcea', 'Pitesti', 97),
    ('Rimnicu_Vilcea', 'Sibiu', 80),

    #('Sibiu', 'Arad', 140),
    #('Sibiu', 'Fagaras', 99),
    #('Sibiu', 'Oradea', 151),
    #('Sibiu', 'Rimnicu_Vilcea', 80),

    #('Timisoara', 'Arad', 118),
    #('Timisoara', 'Lugoj', 111),

    #('Urziceni', 'Bucharest', 85),
    #('Urziceni', 'Hirsova', 98),
    ('Urziceni', 'Vaslui', 142),

    #('Vaslui', 'Iasi', 92),
    #('Vaslui', 'Urziceni', 142),

    #('Zerind', 'Arad', 75),
    #('Zerind', 'Oradea', 71)
]


# Build an undirected graph.
undirected_graph = nx.Graph()
for u, v, w in list_of_edges:
    undirected_graph.add_edge(u, v, weight = w)


# Lay out the undirected graph.
dictionary_of_cities_and_positions = {
    'Arad': (43, -92),
    'Bucharest': (465, -267),
    'Craiova': (264, -310),
    'Dobreta': (144, -297),
    'Eforie': (685, -304),
    'Fagaras': (337, -137),
    'Giurgiu': (430, -328),
    'Hirsova': (646, -243),
    'Iasi': (564, -76),
    'Lugoj': (144, -213),
    'Mehadia': (148, -255),
    'Neamt': (472, -44),
    'Oradea': (98, -7),
    'Pitesti': (356, -225),
    'Rimnicu_Vilcea': (237, -179),
    'Sibiu': (202, -128),
    'Timisoara': (48, -179),
    'Urziceni': (542, -243),
    'Vaslui': (613, -142),
    'Zerind': (67, -49)
}


# Define a heuristic of estimates of straight line distances to goal Bucharest.
heuristic = {
    'Arad': 366,
    'Bucharest': 0,
    'Craiova': 160,
    'Dobreta': 242,
    'Eforie': 161,
    'Fagaras': 176,
    'Giurgiu': 77,
    'Hirsova': 151,
    'Iasi': 226,
    'Lugoj': 244,
    'Mehadia': 241,
    'Neamt': 234,
    'Oradea': 380,
    'Pitesti': 98,
    'Rimnicu_Vilcea': 193,
    'Sibiu': 253,
    'Timisoara': 329,
    'Urziceni': 80,
    'Vaslui': 199,
    'Zerind': 374
}


def describe(min_heap) -> str:
    '''
    The min heap is a list satisfying requirements for a min heap.
    The first element of the min heap is the element in the heap with the minimal estimated total distance.
    However, while all of the elements of the heap satisfy the requirements for a min heap,
    the elements other than the first may not necessarily be sorted by estimated total distance. 
    '''
    items: list[tuple[float, float, str, str | None]] = sorted(min_heap)
    if not items:
        return "The min heap is empty."
    parts = [
        f"(f = {f:.0f}, g = {g:.0f}, location = {n}, preceding location = {p})"
        for f, g, n, p in items
    ]
    return "The min heap currently contains\n" + "\n".join(parts) + "."


def _hierarchy_pos(
    G: nx.DiGraph,
    root: str,
    *,
    x_center: float = 0.5,
    total_width: float = 1.0,
    vertical_gap: float = 1.0,
    vertical_loc: float = 0.0,
    _pos_cache: dict[str, tuple[float, float]] | None = None,
    _visited: set[str] | None = None
) -> dict[str, tuple[float, float]]:
    """
    Recursively compute (x, y) coordinates that lay a **tree** out top-down.

    The routine now includes *cycle protection*: if `root` (or any descendant)
    is encountered again while the recursion is still active, that branch is
    ignored so the call stack cannot grow indefinitely.

    Parameters
    ----------
    G
        A directed graph that is *supposed* to represent an exploration tree.
        If spurious back-edges have turned it into a DAG or a graph with
        cycles, those extra edges are safely ignored.
    root
        The node to treat as the root of the layout.
    x_center, total_width, vertical_gap, vertical_loc
        Usual layout parameters (unchanged).
    _pos_cache, _visited
        Internal parameters used to accumulate results and remember the nodes
        already placed.  **Do not supply manually.**

    Returns
    -------
    dict
        Mapping ``node → (x, y)`` suitable for `networkx.draw`.
    """
    # ------------------------------------------------------------------ setup
    if _pos_cache is None:
        _pos_cache = {}
    if _visited is None:
        _visited = set()

    # If we've already placed this node, bail out — prevents infinite recursion
    if root in _visited:
        return _pos_cache
    _visited.add(root)

    # ------------------------------------------------------------------ place
    _pos_cache[root] = (x_center, vertical_loc)

    children = list(G.successors(root))
    if not children:                # leaf ⇒ nothing more to lay out
        return _pos_cache

    # ---------------------------------------------------------------- recurse
    dx = total_width / len(children)              # width for each subtree
    next_x = x_center - total_width / 2 + dx / 2  # centre of leftmost child

    for child in children:
        if child in _visited:        # skip back-edge to an ancestor/older node
            continue
        _hierarchy_pos(
            G,
            child,
            x_center=next_x,
            total_width=dx,
            vertical_gap=vertical_gap,
            vertical_loc=vertical_loc - vertical_gap,
            _pos_cache=_pos_cache,
            _visited=_visited,
        )
        next_x += dx

    return _pos_cache


def draw_search_tree(search_tree: nx.DiGraph,
                     closed: set[str],
                     open_heap: list[tuple[float, float, str, str | None]],
                     *,
                     selected: str | None = None,
                     solution_path: set[str] = set()) -> None:
    """Visualise the exploration tree with a tidy, top-down layout."""

    # ---------- colour coding --------------------------------------------- #
    open_nodes = {n for _, _, n, _ in open_heap}
    colours = []
    for n in search_tree.nodes():
        if n in solution_path:                 # final solution path → red
            colours.append("firebrick")
        elif n == selected: # just chosen for expansion
            colours.append("gold")
        elif n in closed:                      # already expanded     → grey
            colours.append("lightgrey")
        elif n in open_nodes:                  # still in frontier    → orange
            colours.append("orange")
        else:
            colours.append("white")            # should not happen

    # ---------- layout ----------------------------------------------------- #
    # The root is the unique node with in-degree 0 (there is only one).
    try:
        root = next(n for n in search_tree.nodes() if search_tree.in_degree(n) == 0)
    except StopIteration:                      # defensive fallback
        root = next(iter(search_tree))

    pos = _hierarchy_pos(search_tree, root, vertical_gap = 1.5)

    # ---------- draw ------------------------------------------------------- #
    plt.figure(figsize=(9, 6))
    nx.draw(
        search_tree,
        pos,
        with_labels=True,
        node_color=colours,
        node_size=800,
        arrows=True,
        arrowsize=14,
        width=1.3,
    )
    plt.title("A* search tree (grey = closed, gold = selected, orange = open)")
    plt.show()


'''
A* search expands the node n in a min heap with the minimal estimated total distance f from start through n to goal.
A* search estimates a total distance as the sum of the distance g so far to reach n and the estimated distance h from n to goal.

In comparison to A* search, greedy search expands the node in a min heap with the minimal estimated distance h from n to goal.
Greedy search expands the node in a priority queue with the minimum heuristic.
Greedy search makes a locally optimal choice with the hope of finding a global optimum.
Greedy search does not generally produce a global optimum but may approximate a global optimum in reasonable time.
'''
def perform_A_star_search(
    graph: nx.Graph,
    start: str,
    goal: str,
    heuristic
):
    print("We begin by placing a node representing the start on a min heap ordered by estimated total distance.")
    initial_distance_so_far = 0
    initial_estimated_distance_from_node_to_goal = heuristic[start]
    initial_estimated_total_distance = initial_distance_so_far + initial_estimated_distance_from_node_to_goal
    initial_preceding_location = None
    node_representing_start = (initial_estimated_total_distance, initial_distance_so_far, start, initial_preceding_location)

    min_heap: list[tuple[float, float, str, str | None]] = []
    heapq.heappush(min_heap, node_representing_start)
    print(describe(min_heap))

    print(f"We place location {start} in a search tree.")
    search_tree = nx.DiGraph()
    search_tree.add_node(start)

    set_of_locations_corresponding_to_expanded_nodes: set[str] = set()
    dictionary_of_locations_and_preceding_locations: dict[str, str] = {}

    g_best: dict[str, float] = {start: 0.0} # cheapest g discovered so far

    step = 0
    while min_heap:

        # Select.
        estimated_total_distance, distance_so_far, location, preceding_location = heapq.heappop(min_heap)

        print(
            f"\nStep {step}\n" +
            "We select a node from the min heap. This node has minimal estimated total distance and is " +
            f"({estimated_total_distance}, {distance_so_far}, {location}, {preceding_location}).\n" +
            "We draw the search tree."
        )

        draw_search_tree(search_tree, set_of_locations_corresponding_to_expanded_nodes, min_heap, selected = location)

        if preceding_location is not None:
            dictionary_of_locations_and_preceding_locations.setdefault(location, preceding_location)

        if location == goal:
            print("Since this is the goal node, the search halts here.\n")
            path = [location]
            while location != start:
                location = dictionary_of_locations_and_preceding_locations[location]
                path.append(location)
            path.reverse()
            return path, distance_so_far

        print(
            f"We expand this node.\n"
            f"The distance so far g is {distance_so_far}. "
            f"The estimated distance from {location} to goal {goal} h is {heuristic[location]}. "
            f"The estimated total distance from start {start} through {location} to goal {goal} f is {estimated_total_distance}."
        )

        # Expand.
        set_of_locations_corresponding_to_expanded_nodes.add(location)

        for neighbor in graph.neighbors(location):
            weight = graph[location][neighbor]["weight"]
            tentative_distance = distance_so_far + weight

            search_tree.add_edge(location, neighbor)

            if neighbor in set_of_locations_corresponding_to_expanded_nodes:
                print(
                    f"I consider the edge ({location}, {neighbor}) whose distance is {weight}. "
                    f"The tentative distance to go from {location} to {neighbor} would be g = {tentative_distance}. "
                    f"However, {neighbor} has already been expanded, so I can take no further action regarding this edge."
                )
                continue

            old_g = g_best.get(neighbor, float("inf"))
            if tentative_distance < old_g:
                # A better (or first) path has been found.
                g_best[neighbor] = tentative_distance
                f_cand = tentative_distance + heuristic[neighbor]
                heapq.heappush(min_heap, (f_cand, tentative_distance, neighbor, location))

                #search_tree.add_edge(location, neighbor)

                if old_g == float("inf"):
                    sentence = (
                        f"    This is the first recorded path to {neighbor}. "
                        f"I therefore update a representation of {neighbor} to (f = {f_cand}, g = {tentative_distance}, node = '{neighbor}', parent = '{location}'), "
                        f"and place this represention on the open list."
                    )
                else:
                    old_f = old_g + heuristic[neighbor]
                    sentence = (
                        f"    This route is better than the previously known "
                        f"one (old f = {old_f:.0f}). I update {neighbor} accordingly "
                        f"and re-queue it with the improved priority f = {f_cand:.0f}."
                    )
                print(
                    f"  I examine edge {location} → {neighbor} with cost {weight}. "
                    f"The provisional cost to {neighbor} is g = {tentative_distance}. "
                    f"{sentence}"
                )
                print("  " + describe(min_heap))
            else:
                print(
                    f"  I examine edge {location} → {neighbor} with cost {weight}. "
                    f"The provisional cost would be g = {tentative_distance}, which is "
                    f"no better than the best cost already recorded for {neighbor} "
                    f"(g = {old_g}). Consequently, I leave {neighbor} unchanged; "
                    f"it remains on the open list with its existing priority."
                )

        # Finish step with a fresh queue overview.
        print("  At the end of this expansion step, " + describe(min_heap))

        step += 1

    # If we exit the loop, the open list is empty and the goal was not reached.
    return None, float("inf")


# Run A* start from Arad to Bucharest.
start = 'Arad'
goal = 'Bucharest'
list_of_nodes_from_start_to_goal, cost_of_traveling_from_start_to_goal = perform_A_star_search(undirected_graph, start, goal, heuristic)

print(f"Path from {start} to {goal}: {list_of_nodes_from_start_to_goal}")
print(f"Cost of traveling from {start} to {goal}: {cost_of_traveling_from_start_to_goal}")

list_of_edges_from_start_to_goal = []
if list_of_nodes_from_start_to_goal is not None:
    list_of_edges_from_start_to_goal = list(
        zip(list_of_nodes_from_start_to_goal[:-1], list_of_nodes_from_start_to_goal[1:])
    )

# Draw the undirected graph.
nx.draw(undirected_graph, dictionary_of_cities_and_positions, with_labels = True, node_size = 0)

# overlay the edges from start to goal to form a thick red path.
nx.draw_networkx_edges(
    undirected_graph,
    dictionary_of_cities_and_positions,
    edgelist = list_of_edges_from_start_to_goal,
    width = 3,
    edge_color = 'red'
)

plt.show()