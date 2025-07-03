'''
Explain how you would detect a cycle in an undirected graph.

A graph contains a cycle if I can get from a vertex back to the vertex by following unique edges.
We can indicate that a cycle exists
when we visit vertices and find that a node q that we just arrived at
is connected to a node n that we already visited
that is not the node p that we just came from.

Consider a graph consisting of:
node 0 connected to nodes 1 and 3
node 1 connected to nodes 0 and 2
node 2 connected to nodes 1 and 3
node 3 connected to nodes 2 and 0

0--1--2
|     |
3     |
-------

We visit root node 0.
We visit node 1.
We visit node 2.
We visit node 3.
We observe that node 3 that we just arrived at
is connected to node 0 that we already visited
that is not node 2 that we just came from.
We have a cycle.

We can indicate that a cycle exists using Depth First Search by starting at a root node N with no parent, noting that N is visited, and, for each neighbor M of N, if M is unvisited, recursively visiting M with parent N, or, if M is visited and M is not N, indicating that a cycle exists.

Consider a graph consisting of:
node 0 connected to nodes 1 and 3
node 1 connected to nodes 0 and 2
node 2 connected to nodes 1 and 3
node 3 connected to nodes 2 and 0

Let's start with node 0.
Let node 0's parent be node -1.
We note that node 0 is visited.
node 0's neighbors 1 and 3 are unvisited.

Let's start with node 1.
node 1's parent is node 0.
We note that node 1 is visited.
node 1's neighbors are 0 and 2.
node 0 is visited and node 0 is node 0.
node 2 is unvisited.

Let's start with node 2.
node 2's parent is node 1.
WE node that node 2 is visited.
node 2's neighbors are 1 and 3.
node 1 is visited and node 1 is node 1.
node 3 is unvisited.

Let's start with node 3.
node 3's parent is node 2.
We note that node 3 is visited.
node 3's neighbors are nodes 2 and 0.
node 2 is visited and node 2 is node 2.
node 0 is visited and node 0 is not node 2.
We have a cycle.

Detecting a cycle in an undirected graph involves maintaining a set of IDs of visited nodes.
Let a bad ID be an ID that doesn't reference a node in the graph. Detecting a cycle starts Depth First Search from node N0 with a bad ID, then if node N1 is not visited starts Depth First Search from node N1 with a bad ID, then if node N2 is not visited starts Depth First Search from node N2 with a bad ID, ..., then if node Nn is not visited starts Depth First Search from node Nn with a bad ID. Depth First Search ultimately indicates whether there is a cycle.

DFS starts at a node N with an ID. DFS adds the ID to the set of IDs of visited nodes. DFS considers each neighbor M of N. If M hasn't been visited, Depth First Search returns the result of recursively calling DFS starting at M with the ID of N. Otherwise, if M is not the parent of N, Depth First Search indicates a cycle.
'''


def has_cycle(graph: dict[int, list[int]]) -> bool:
    '''
    Detects a cycle in an undirected graph using depth-first search.

    Parameters
    ----------
    graph: dict[int, list[int]]
        graph is an adjacency-list representation of a graph.
        Keys are node IDs.
        values are lists of neighbouring node IDs.

    Returns
    -------
    bool
        True if the graph contains at least one cycle, False otherwise.
    '''
    visited = set()

    def dfs(v: int, parent: int) -> bool:
        visited.add(v)
        for neigh in graph[v]:
            if neigh not in visited:
                return dfs(neigh, v)
            elif neigh != parent:
                return True
        return False

    # Handle disconnected graphs.
    for start in graph:
        if start not in visited:
            return dfs(start, parent = -1)
    return False


if __name__ == "__main__":
    '''
    There is a path from node with ID 0 to node with ID 1 to node with ID 2.
    There is a path from node with ID 2 to node with ID 3 to node with ID 0.
    Thus, there is a path from node with ID 0 to node with ID 0 and a cycle.
    '''
    g = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 3],
        3: [2, 0],
        4: [] # The graph contains an isolated vertex.
    }
    assert has_cycle(g) == True