from collections import deque


class Node:
    '''
    Class Node is a template for a single vertex in a tree.
    '''
    def __init__(self, value):
        # For a binary tree
        self.left: Node | None = None
        self.right: Node | None = None
        # For a n-ary tree
        #self.children = []
        self.value = value
    
    def add_left(self, value):
        self.left = Node(value)
    
    def add_right(self, value):
        self.right = Node(value)


class BinarySearchTree:
    def __init__(self):
        self.root: Node | None = None
    
    def add_node(self, value):
        if self.root is None:
            self.root = Node(value)
            return
        current = self.root
        while True:
            if value <= current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right

    def help_draw(self, node: Node, prefix: str = "", is_left: bool = True):
        if node.right:
            self.help_draw(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
            self.help_draw(node.left, prefix + ("    " if is_left else "│   "), True)
    
    def draw(self):
        if not self.root:
            print("<empty tree>")
            return
        self.help_draw(self.root)
    
    def traverse_pre_order(self):
        '''
        Traversing a tree order pre order is useful for copying a tree.
        '''
        out = []
        def help_traverse_pre_order(node):
            if node:
                out.append(node.value)
                help_traverse_pre_order(node.left)
                help_traverse_pre_order(node.right)
        help_traverse_pre_order(self.root)
        print(f"Pre Order Traversal visit order: {out}")
    
    def traverse_in_order(self):
        '''
        Traversing a tree order in order is useful for ?.
        '''
        out = []
        def help_traverse_in_order(node):
            if node:
                help_traverse_in_order(node.left)
                out.append(node.value)
                help_traverse_in_order(node.right)
        help_traverse_in_order(self.root)
        print(f"In Order Traversal visit order: {out}")

    def traverse_post_order(self):
        '''
        Traversing a tree order post order is useful for deallocating a tree.
        '''
        out = []
        def help_traverse_post_order(node):
            if node:
                help_traverse_post_order(node.left)
                help_traverse_post_order(node.right)
                out.append(node.value)
        help_traverse_post_order(self.root)
        print(f"Post Order Traversal visit order: {out}")
    
    def conduct_breadth_first_search(self, value):
        '''
        Breadth first search searches 1 level at a time.
        Breadth first search is useful for finding elements close to the root.
        '''
        if not self.root:
            print("Tree is empty.")
            return False
        visit_order = []
        q = deque([self.root])
        while q:
            node = q.popleft()
            visit_order.append(node.value)
            if node.value == value:
                print(f"BFS visit order to {value}: {visit_order}")
                return True
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        print(f"BFS visit order to {value}: {visit_order} - value not found")
        return False
    
    def conduct_depth_first_search(self, value):
        '''
        Depth first search is useful for finding elements far from the root.
        '''
        visit_order = []
        def help_conduct_depth_first_search(node):
            if not node:
                return None
            visit_order.append(node.value)
            if node.value == value:
                return node
            return help_conduct_depth_first_search(node.left) or help_conduct_depth_first_search(node.right)
        found = help_conduct_depth_first_search(self.root)
        if found:
            print(f"DFS visit order to {value}: {visit_order}")
            return True
        else:
            print(f"DFS visit order to {value}: {visit_order} - value not found")
            return False

tree = BinarySearchTree()
#for value in (10, 5, 15, 3, 8, 7, 9, 17):
for value in (776, 435, 869, 141, 700, 791, 957, 66, 450, 806, 48, 124, 42):
    tree.add_node(value)

tree.draw()
tree.traverse_pre_order() # I expect "[10, 5, 3, 8, 7, 9, 15, 17]" to be printed.
tree.traverse_in_order() # I expect "[3, 5, 7, 8, 9, 10, 15, 17]" to be printed.
tree.traverse_post_order() # I expect "[3, 7, 9, 8, 5, 17, 15, 10]" to be printed.
tree.conduct_breadth_first_search(450)
tree.conduct_depth_first_search(450)