'''
Given the network defined below and heuristic, use A* to find the best route from Node A to G

Node,Heuristic to G
A,97
B,71
C,46
D,80
E,41
F,66
G,0


I begin by placing the start node on the open list / priority queue ordered by priority f = cost so far g + heuristic h.
The open list currently contains: A (f = 97).

Step 0: I now expand node A. The cost so far is g = 0.0, the heuristic estimate is h = 97, so the evaluation value is f = g + h = 97.
  I examine edge A → B with cost 70. The provisional cost to B is g = 70.0.     This is the first recorded path to B. I therefore update a representation of B to (f = 141.0, g = 70.0, node = 'B', parent = 'A'), and place this represention on the open list.
  The open list currently contains: B (f = 141).
  I examine edge A → C with cost 54. The provisional cost to C is g = 54.0.     This is the first recorded path to C. I therefore update a representation of C to (f = 100.0, g = 54.0, node = 'C', parent = 'A'), and place this represention on the open list.
  The open list currently contains: C (f = 100), B (f = 141).
  I examine edge A → D with cost 27. The provisional cost to D is g = 27.0.     This is the first recorded path to D. I therefore update a representation of D to (f = 107.0, g = 27.0, node = 'D', parent = 'A'), and place this represention on the open list.
  The open list currently contains: C (f = 100), D (f = 107), B (f = 141).
  At the end of this expansion step, The open list currently contains: C (f = 100), D (f = 107), B (f = 141).

Step 1: I now expand node C. The cost so far is g = 54.0, the heuristic estimate is h = 46, so the evaluation value is f = g + h = 100.0.
  I consider the edge C → A whose cost is 54. The tentative cost to reach A would be g = 108.0. However, A has already been closed, so I can take no further action regarding this edge.
  I examine edge C → B with cost 35. The provisional cost would be g = 89.0, which is no better than the best cost already recorded for B (g = 70.0). Consequently, I leave B unchanged; it remains on the open list with its existing priority.
  I examine edge C → D with cost 53. The provisional cost would be g = 107.0, which is no better than the best cost already recorded for D (g = 27.0). Consequently, I leave D unchanged; it remains on the open list with its existing priority.
  I examine edge C → E with cost 47. The provisional cost to E is g = 101.0.     This is the first recorded path to E. I therefore update a representation of E to (f = 142.0, g = 101.0, node = 'E', parent = 'C'), and place this represention on the open list.
  The open list currently contains: D (f = 107), B (f = 141), E (f = 142).
  I examine edge C → G with cost 60. The provisional cost to G is g = 114.0.     This is the first recorded path to G. I therefore update a representation of G to (f = 114.0, g = 114.0, node = 'G', parent = 'C'), and place this represention on the open list.
  The open list currently contains: D (f = 107), G (f = 114), B (f = 141), E (f = 142).
  At the end of this expansion step, The open list currently contains: D (f = 107), G (f = 114), B (f = 141), E (f = 142).

Step 2: I now expand node D. The cost so far is g = 27.0, the heuristic estimate is h = 80, so the evaluation value is f = g + h = 107.0.
  I consider the edge D → A whose cost is 27. The tentative cost to reach A would be g = 54.0. However, A has already been closed, so I can take no further action regarding this edge.
  I consider the edge D → C whose cost is 53. The tentative cost to reach C would be g = 80.0. However, C has already been closed, so I can take no further action regarding this edge.
  I examine edge D → E with cost 93. The provisional cost would be g = 120.0, which is no better than the best cost already recorded for E (g = 101.0). Consequently, I leave E unchanged; it remains on the open list with its existing priority.
  At the end of this expansion step, The open list currently contains: G (f = 114), B (f = 141), E (f = 142).

Step 3: I now expand node G. The cost so far is g = 114.0, the heuristic estimate is h = 0, so the evaluation value is f = g + h = 114.0.
Since this is the goal node, the search halts here.

A* path from A to G: ['A', 'C', 'G']
Total path cost:      114.0
'''


import heapq
import matplotlib.pyplot as plt
import networkx as nx


# Define weighted edges
edges = [
    ('A', 'B', 70),
    ('A', 'C', 54),
    ('A', 'D', 27),
    ('B', 'C', 35),
    ('B', 'F', 45),
    ('C', 'D', 53),
    ('C', 'E', 47),
    ('C', 'G', 60),
    ('D', 'E', 93),
    ('E', 'G', 46),
    ('F', 'G', 70)
]

# Build the graph
G = nx.Graph()
for u, v, w in edges:
    G.add_edge(u, v, weight = w)

# Hand-tuned layout
pos = {
    'A': (0, 3),
    'B': (-1, 1.5),
    'C': (-0.5, 0.5),
    'D': (0.5, 2),
    'E': (0.5, -0.5),
    'F': (-2, -2),
    'G': (-0.5, -3)
}

# Heuristic (straight-line) estimates to goal G
heuristic = {
    'A': 97,
    'B': 71,
    'C': 46,
    'D': 80,
    'E': 41,
    'F': 66,
    'G': 0
}

# NetworkX expects a function: h(node, goal) -> estimated remaining cost
def h(u: str, v: str) -> float:
    return heuristic[u]


def astar_verbose(
    graph: nx.Graph,
    start: str,
    goal: str,
    heuristic_fn,
    weight_attr: str = "weight",
):
    """
    A* search narrated in full prose, with explicit commentary on
    queue contents, re-queuing, and closed-set effects.
    """
    # ── data structures ────────────────────────────────────────────
    open_heap: list[tuple[float, float, str, str | None]] = []
    heapq.heappush(open_heap, (heuristic_fn(start, goal), 0.0, start, None))

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
            f"is h = {heuristic_fn(u, goal)}, so the evaluation value is "
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
                f_cand = g_cand + heuristic_fn(v, goal)
                heapq.heappush(open_heap, (f_cand, g_cand, v, u))

                if old_g == float("inf"):
                    sentence = (
                        f"    This is the first recorded path to {v}. "
                        f"I therefore update a representation of {v} to (f = {f_cand}, g = {g_cand}, node = '{v}', parent = '{u}'), "
                        f"and place this represention on the open list."
                    )
                else:
                    old_f = old_g + heuristic_fn(v, goal)
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


# Run A* from A to G
start, goal = 'A', 'G'
astar_path, astar_cost = astar_verbose(G, start, goal, h)

print("A* path from A to G:", astar_path)
print("Total path cost:     ", astar_cost)

# Redraw & highlight the found path
edge_path = []
if astar_path is not None:
    edge_path = list(zip(astar_path[:-1], astar_path[1:]))

# draw the base graph
nx.draw(G, pos, with_labels=True, node_size=1200, font_weight='bold')
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=nx.get_edge_attributes(G, 'weight'),
    font_size=9
)

# overlay the solution edges in red & thicker width
nx.draw_networkx_edges(G, pos, edgelist=edge_path, width=4, edge_color='red')

plt.show()