class Node:

    def __init__(self, value: str):
        self.value: str = value
        self.left: Node | None = None
        self.right: Node | None = None


def build_tree(
    list_of_nodes_pre_order: list[str],
    list_of_nodes_in_order:  list[str],
    depth: int
) -> Node | None:
    '''
    Reconstruct a binary tree from traversals pre order and in order.
    '''

    indent = "  " * depth

    if not list_of_nodes_pre_order:
        print(f"{indent}List of nodes pre order is empty.")
        return None

    value_of_root_node = list_of_nodes_pre_order[0]
    print(f"{indent}The root is the first element visited pre order, {value_of_root_node}.")

    print(f"{indent}We split the list of nodes in order at the root to find nodes to the left of the root visited before the root and nodes to the right of the root visited after the root.")
    root_index = list_of_nodes_in_order.index(value_of_root_node)
    list_of_left_nodes_in_order  = list_of_nodes_in_order[:root_index]
    list_of_right_nodes_in_order = list_of_nodes_in_order[root_index + 1:]
    print(f"{indent}List of left nodes in order: {list_of_left_nodes_in_order}")
    print(f"{indent}List of right nodes in order: {list_of_right_nodes_in_order}")

    print(f"{indent}We find the number of elements to the left of the root.")
    number_of_nodes_to_left_of_root = len(list_of_left_nodes_in_order)
    print(f"{indent}Number of elements to left of root: {number_of_nodes_to_left_of_root}")

    print(f"{indent}We find the first {number_of_nodes_to_left_of_root} children of the root pre order.")
    sublist_of_first_children_of_root_pre_order  = list_of_nodes_pre_order[1 : 1 + number_of_nodes_to_left_of_root]
    sublist_of_remaining_children_of_root_pre_order = list_of_nodes_pre_order[1 + number_of_nodes_to_left_of_root :]
    print(f"{indent}List of first {number_of_nodes_to_left_of_root} children of the root pre order: {sublist_of_first_children_of_root_pre_order}")
    print(f"{indent}List of remaining children of the root pre order: {sublist_of_remaining_children_of_root_pre_order}")

    print(f"{indent}We create a tree with root {value_of_root_node}.")
    root = Node(value_of_root_node)

    print(f"{indent}We assign the left child of the root to be the output of building a tree for the list of the first {number_of_nodes_to_left_of_root} children of the root pre order and the list of the left nodes of the root in order.")
    root.left  = build_tree(sublist_of_first_children_of_root_pre_order, list_of_left_nodes_in_order, depth + 1)

    print(f"{indent}We assign the right child of the root to be the output of building a tree for the list of the remaining children of the root pre order and the list of the right nodes of the root in order.")
    root.right = build_tree(sublist_of_remaining_children_of_root_pre_order, list_of_right_nodes_in_order, depth + 1)

    return root


def print_tree(node: Node | None,
               prefix: str = "",
               is_left: bool = True) -> None:
    """Pretty-print the tree sideways."""
    if node is None:
        return

    if node.right:
        print_tree(node.right,
                   prefix + ("│   " if is_left else "    "),
                   False)

    connector = "└── " if is_left else "┌── "
    print(prefix + connector + node.value)

    if node.left:
        print_tree(node.left,
                   prefix + ("    " if is_left else "│   "),
                   True)


# --------------------------------------------------------------------------
# Example
# --------------------------------------------------------------------------

preorder = ['G', 'B', 'A', 'D', 'C', 'E', 'F', 'I', 'H', 'K']
inorder  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K']

print("=== Narrated reconstruction ===")
root = build_tree(preorder, inorder, 0)

print("\n=== ASCII sketch of the rebuilt tree ===")
print_tree(root)