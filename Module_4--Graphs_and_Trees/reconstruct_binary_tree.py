from typing import List, Optional


class Node:
    """Simple binary‐tree node."""
    def __init__(self, val: str):
        self.val: str = val
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


def build_tree(preorder: List[str], inorder: List[str]) -> Optional[Node]:
    """
    Reconstruct a binary tree from preorder and inorder traversals.
    preorder[0] is always the current subtree’s root.
    """
    if not preorder:                      # base case: empty subtree
        return None

    root_val = preorder[0]
    root = Node(root_val)

    # Split inorder list at the root to get left vs right subtrees
    root_index = inorder.index(root_val)
    in_left  = inorder[:root_index]
    in_right = inorder[root_index + 1:]

    # Number of nodes in the left subtree = len(in_left)
    pre_left  = preorder[1 : 1 + len(in_left)]
    pre_right = preorder[1 + len(in_left):]

    # Recursively build subtrees
    root.left  = build_tree(pre_left,  in_left)
    root.right = build_tree(pre_right, in_right)

    return root

def print_tree(node: Optional[Node], prefix: str = "", is_left: bool = True) -> None:
    """
    Pretty-print the tree sideways:
        right child
    root
        left child
    """
    if node is None:
        return

    if node.right:
        print_tree(node.right,
                   prefix + ("│   " if is_left else "    "),
                   False)

    # Current node
    connector = "└── " if is_left else "┌── "
    print(prefix + connector + node.val)

    if node.left:
        print_tree(node.left,
                   prefix + ("    " if is_left else "│   "),
                   True)

# --- Example --------------------------------------------------------------

preorder = ['G', 'B', 'A', 'D', 'C', 'E', 'F', 'I', 'H', 'K']
inorder  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K']

root = build_tree(preorder, inorder)
print_tree(root)