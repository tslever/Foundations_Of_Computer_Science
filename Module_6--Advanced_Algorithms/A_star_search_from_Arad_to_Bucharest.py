'''
Find the best route from Arad to Bucharest given the following graph and heuristic.
'''


import heapq
import matplotlib.pyplot as plt
import networkx as nx


# Define weighted undirected edges.
list_of_edges = [
    ('Arad', 'Sibiu', 140),
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


# Define a heuristic of straight line estimates to goal Bucharest.
heuristic = {
    'Arad': 366,
    'Bucharest': 0,
    'Craiova': 160,
    'Dobreta': 242,
    'Eforie': 161,
    'Fagaras': 178,
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


def perform_A_star_search(
    graph: nx.Graph,
    start: str,
    goal: str,
    heuristic,
    weight_attr: str = "weight",
):
    """
    A* search narrated in full prose, with explicit commentary on
    queue contents, re-queuing, and closed-set effects.
    """
    # ── data structures ────────────────────────────────────────────
    open_heap: list[tuple[float, float, str, str | None]] = []
    heapq.heappush(open_heap, (heuristic[start], 0.0, start, None))

    g_best:   dict[str, float] = {start: 0.0}   # cheapest g discovered so far
    came_from: dict[str, str] = {}              # child → parent
    closed:   set[str]        = set()           # nodes permanently expanded

    def queue_view() -> str:
        """Return a prose-friendly description of the open list."""
        items = sorted((f, n) for f, g, n, _ in open_heap)
        if not items:
            return "The open list is now empty."
        parts = [f"{node} (f = {f:.0f})" for f, node in items]
        return "The open list currently contains: " + ", ".join(parts) + "."

    # ── initial narration ──────────────────────────────────────────
    print("\nI begin by placing the start node on the open list / priority queue ordered by priority f = cost so far g + heuristic h.")
    print(queue_view())

    step = 0
    while open_heap:
        # Retrieve the node with the lowest f.  Discard stale duplicates.
        f_u, g_u, u, parent = heapq.heappop(open_heap)
        if u in closed:
            continue   # This entry is obsolete; a cheaper route has closed u.

        closed.add(u)
        if parent is not None:
            came_from.setdefault(u, parent)

        print(
            f"\nStep {step}: I now expand node {u}. "
            f"The cost so far is g = {g_u}, the heuristic estimate "
            f"is h = {heuristic[u]}, so the evaluation value is "
            f"f = g + h = {f_u}."
        )
        step += 1

        # ── goal test ───────────────────────────────────────────────
        if u == goal:
            print("Since this is the goal node, the search halts here.\n")
            # Reconstruct and return the path.
            path = [u]
            while u != start:
                u = came_from[u]
                path.append(u)
            return path[::-1], g_u

        # ── examine each neighbour in turn ─────────────────────────
        for v in graph.neighbors(u):
            w = graph[u][v][weight_attr]
            g_cand = g_u + w

            if v in closed:
                print(
                    f"  I consider the edge {u} → {v} whose cost is {w}. "
                    f"The tentative cost to reach {v} would be g = {g_cand}. "
                    f"However, {v} has already been closed, so I can take no "
                    f"further action regarding this edge."
                )
                continue

            old_g = g_best.get(v, float("inf"))
            if g_cand < old_g:
                # A better (or first) path has been found.
                g_best[v] = g_cand
                f_cand = g_cand + heuristic[v]
                heapq.heappush(open_heap, (f_cand, g_cand, v, u))

                if old_g == float("inf"):
                    sentence = (
                        f"    This is the first recorded path to {v}. "
                        f"I therefore update a representation of {v} to (f = {f_cand}, g = {g_cand}, node = '{v}', parent = '{u}'), "
                        f"and place this represention on the open list."
                    )
                else:
                    old_f = old_g + heuristic[v]
                    sentence = (
                        f"    This route is better than the previously known "
                        f"one (old f = {old_f:.0f}). I update {v} accordingly "
                        f"and re-queue it with the improved priority f = {f_cand:.0f}."
                    )
                print(
                    f"  I examine edge {u} → {v} with cost {w}. "
                    f"The provisional cost to {v} is g = {g_cand}. "
                    f"{sentence}"
                )
                print("  " + queue_view())
            else:
                print(
                    f"  I examine edge {u} → {v} with cost {w}. "
                    f"The provisional cost would be g = {g_cand}, which is "
                    f"no better than the best cost already recorded for {v} "
                    f"(g = {old_g}). Consequently, I leave {v} unchanged; "
                    f"it remains on the open list with its existing priority."
                )

        # Finish step with a fresh queue overview.
        print("  At the end of this expansion step, " + queue_view())

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