'''
Response to ICA 4

│       ┌── 957
│   ┌── 869
│   │   │   ┌── 806
│   │   └── 791
└── 776
    │   ┌── 700
    │   │   └── 450
    └── 435
        └── 141
            │   ┌── 124
            └── 66
                └── 48
                    └── 42
Pre Order Traversal visit order: [776, 435, 141, 66, 48, 42, 124, 700, 450, 869, 791, 806, 957]
In Order Traversal visit order: [42, 48, 66, 124, 141, 435, 450, 700, 776, 791, 806, 869, 957]
Post Order Traversal visit order: [42, 48, 124, 66, 141, 450, 700, 435, 806, 791, 957, 869, 776]
BFS visit order to 450: [776, 435, 869, 141, 700, 791, 957, 66, 450]
DFS visit order to 450: [776, 435, 141, 66, 48, 42, 124, 700, 450]
'''


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
        '''
        Insert value while preserving BST order.
        Duplicate values go left.
        '''
        parent = None
        current = self.root
        while current:
            parent = current
            current = current.left if value <= current.value else current.right
        new_node = Node(value)
        if parent is None:
            self.root = new_node
        elif value <= parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
    

    def conduct_breadth_first_search(self, value):
        '''
        Breadth first search searches 1 level at a time.
        Breadth first search is useful for finding elements close to the root.
        Worst case time complexity in a Binary Search Tree is `O(n)` due to walking every node until node with value is found or all nodes are evaluated.
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
    

    def conduct_depth_first_search_in_order(self, value):
        '''
        Worst case time complexity in a Binary Search Tree is `O(n)` due to walking every node until node with value is found or all nodes are evaluated.
        '''
        visit_order = []

        def help_conduct_depth_first_search_in_order(node):
            if not node:
                return None
            found = help_conduct_depth_first_search_in_order(node.left)
            if found:
                return found
            visit_order.append(node.value)
            if node.value == value:
                return node
            return help_conduct_depth_first_search_in_order(node.right)

        found = help_conduct_depth_first_search_in_order(self.root)
        if found:
            print(f"DFS in order visit order to {value}: {visit_order}")
            return True
        else:
            print(f"DFS in order visit order to {value}: {visit_order} – value not found")
            return False


    def conduct_depth_first_search_post_order(self, value):
        '''
        Conduct depth first search post order to find value.
        Worst case time complexity in a Binary Search Tree is `O(n)` due to walking every node until node with value is found or all nodes are evaluated.
        '''
        visit_order = []

        def help_conduct_depth_first_search_post_order(node):
            if not node:
                return None
            found = help_conduct_depth_first_search_post_order(node.left)
            if found:
                return found
            found = help_conduct_depth_first_search_post_order(node.right)
            if found:
                return found
            visit_order.append(node.value)
            if node.value == value:
                return node
            return None

        found = help_conduct_depth_first_search_post_order(self.root)
        if found:
            print(f"DFS post order visit order to {value}: {visit_order}")
            return True
        else:
            print(f"DFS post order visit order to {value}: {visit_order} - value not found")
            return False


    def conduct_depth_first_search_pre_order(self, value):
        '''
        Depth first search is useful for finding elements far from the root.
        Worst case time complexity in a Binary Search Tree is `O(n)` due to walking every node until node with value is found or all nodes are evaluated.
        '''
        visit_order = []

        def help_conduct_depth_first_search_pre_order(node):
            '''
            Search pre order for a node with a value defined in the parent's scope.
            '''
            if not node:
                return None
            visit_order.append(node.value)
            if node.value == value:
                return node
            return help_conduct_depth_first_search_pre_order(node.left) or help_conduct_depth_first_search_pre_order(node.right)
        
        found = help_conduct_depth_first_search_pre_order(self.root)
        if found:
            print(f"DFS pre order visit order to {value}: {visit_order}")
            return True
        else:
            print(f"DFS pre order visit order to {value}: {visit_order} - value not found")
            return False


    def draw(self):
        if self.root is None:
            print("<empty tree>")
            return
        self.help_draw(self.root, "", True)
    

    def find(self, value: int) -> bool:
            '''
            Return True if and only if value is present in the tree.
            Worst case time complexity is `O(h)`, where `h` is the height of the tree, or
            `O[log(n)]` in a balanced tree and `O(n)` in an unbalanced tree of elements that were sorted in order.
            Stop as soon as one subtree that possibly contains value is known.
            '''
            current = self.root
            while current:
                if value == current.value:
                    return True
                current = current.left if value < current.value else current.right
            return False


    def help_draw(self, node: Node, prefix: str, node_is_left_child: bool):
        '''
        prefix: str -- prefix begins every line.
        '''
        if node.right:
            self.help_draw(node.right, prefix + ("│   " if node_is_left_child else "    "), False)
        print(prefix + ("└── " if node_is_left_child else "┌── ") + str(node.value))
        if node.left:
            self.help_draw(node.left, prefix + ("    " if node_is_left_child else "│   "), True)

    
    def traverse_in_order(self):
        '''
        Traversing a tree order in order is useful for
        traversing a Binary Search Tree so that nodes are visited in sorted order.
        '''
        visit_order = []
        def help_traverse_in_order(node):
            if node:
                help_traverse_in_order(node.left)
                visit_order.append(node.value)
                help_traverse_in_order(node.right)
        help_traverse_in_order(self.root)
        print(f"In Order Traversal visit order: {visit_order}")


    def traverse_post_order(self):
        '''
        Traversing a tree order post order is useful for deallocating a tree.
        '''
        visit_order = []
        def help_traverse_post_order(node):
            if node:
                help_traverse_post_order(node.left)
                help_traverse_post_order(node.right)
                visit_order.append(node.value)
        help_traverse_post_order(self.root)
        print(f"Post Order Traversal visit order: {visit_order}")
    

    def traverse_pre_order(self):
        '''
        Traversing a tree order pre order is useful for copying a tree.
        '''
        visit_order = []
        def help_traverse_pre_order(node):
            if node:
                visit_order.append(node.value)
                help_traverse_pre_order(node.left)
                help_traverse_pre_order(node.right)
        help_traverse_pre_order(self.root)
        print(f"Pre Order Traversal visit order: {visit_order}")


tree = BinarySearchTree()
#for value in (10, 5, 15, 3, 8, 7, 9, 17):
for value in (776, 435, 869, 141, 700, 791, 957, 66, 450, 806, 48, 124, 42):
    tree.add_node(value)

tree.draw()
tree.traverse_pre_order()
tree.traverse_in_order()
tree.traverse_post_order()
tree.conduct_breadth_first_search(450)
tree.conduct_depth_first_search_in_order(450)
tree.conduct_depth_first_search_post_order(450)
tree.conduct_depth_first_search_pre_order(450)