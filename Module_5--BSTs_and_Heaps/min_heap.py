'''
Response to ICA 5

Initial heap:
│       ┌── 16
│   ┌── 15
│   │   └── 17
└── 5
    │   ┌── 11
    └── 7
        └── 8
            └── 9

Array view (values / parent indices):
Values :   5   7  15   8  11  17  16   9
Parents:  -1   0   0   1   1   2   2   3

delete() -> 5
│       ┌── 16
│   ┌── 15
│   │   └── 17
└── 7
    │   ┌── 11
    └── 8
        └── 9
Values :   7   8  15   9  11  17  16
Parents:  -1   0   0   1   1   2   2

delete() -> 7
│   ┌── 15
│   │   └── 17
└── 8
    │   ┌── 11
    └── 9
        └── 16
Values :   8   9  15  16  11  17
Parents:  -1   0   0   1   1   2

In-order traversal: [16, 9, 11, 8, 17, 15]

add(12)
│       ┌── 15
│   ┌── 12
│   │   └── 17
└── 8
    │   ┌── 11
    └── 9
        └── 16
Values :   8   9  12  16  11  17  15
Parents:  -1   0   0   1   1   2   2

add(18)
│       ┌── 15
│   ┌── 12
│   │   └── 17
└── 8
    │   ┌── 11
    └── 9
        └── 16
            └── 18
Values :   8   9  12  16  11  17  15  18
Parents:  -1   0   0   1   1   2   2   3

add(6)
│       ┌── 15
│   ┌── 12
│   │   └── 17
└── 6
    │   ┌── 11
    └── 8
        │   ┌── 16
        └── 9
            └── 18
Values :   6   8  12   9  11  17  15  18  16
Parents:  -1   0   0   1   1   2   2   3   3

Final heap:
│       ┌── 15
│   ┌── 12
│   │   └── 17
└── 6
    │   ┌── 11
    └── 8
        │   ┌── 16
        └── 9
            └── 18

Array view:
Values :   6   8  12   9  11  17  15  18  16
Parents:  -1   0   0   1   1   2   2   3   3

Final in-order traversal: [18, 9, 16, 8, 11, 6, 17, 12, 15]
'''


from typing import List, Optional


class Node:
    '''
    Class Node is a template for a node for drawing and traversing.
    '''
    def __init__(self, value: int):
        self.value: int = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None


class MinHeap:
    
    def __init__(self) -> None:
        self._data: List[int] = []


    def _sift_up(self, idx: int) -> None:
        while idx and self._data[idx] < self._data[(idx - 1) // 2]:
            parent = (idx - 1) // 2
            self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
            idx = parent


    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            l, r = 2 * idx + 1, 2 * idx + 2
            smallest = idx
            if l < n and self._data[l] < self._data[smallest]:
                smallest = l
            if r < n and self._data[r] < self._data[smallest]:
                smallest = r
            if smallest == idx:
                break
            self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
            idx = smallest


    def add(self, value: int) -> None:
        self._data.append(value)
        self._sift_up(len(self._data) - 1)


    def delete(self) -> Optional[int]:
        '''
        Remove and return minimum value / value of root.
        Return None if heap is empty.
        '''
        if not self._data:
            return None
        root_val = self._data[0]
        last_val = self._data.pop()
        if self._data:
            self._data[0] = last_val
            self._sift_down(0)
        return root_val


    def _build_pointer_tree(self) -> Optional[Node]:
        '''
        Return the root node of a heap of objects of type Node connected by pointers.
        '''
        if not self._data:
            return None
        nodes = [Node(x) for x in self._data]
        for i, node in enumerate(nodes):
            li, ri = 2 * i + 1, 2 * i + 2
            if li < len(nodes):
                node.left = nodes[li]
            if ri < len(nodes):
                node.right = nodes[ri]
        return nodes[0] # root


    def _help_draw(self, node: Node, prefix: str, is_left: bool) -> None:
        if node.right:
            self._help_draw(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
            self._help_draw(node.left, prefix + ("    " if is_left else "│   "), True)


    def draw(self) -> None:
        '''
        Pretty print the heap as a tree.
        '''
        root = self._build_pointer_tree()
        if not root:
            print("<empty heap>")
            return
        self._help_draw(root, "", True)


    def _traverse_in_order(self, node: Optional[Node], out: List[int]) -> None:
        '''
        This method receives the root of a heap of objects of type Node connected by pointers.
        '''
        if node:
            self._traverse_in_order(node.left, out)
            out.append(node.value)
            self._traverse_in_order(node.right, out)


    def in_order(self) -> List[int]:
        res: List[int] = []
        self._traverse_in_order(self._build_pointer_tree(), res)
        return res


    def display_array_and_parents(self) -> None:
        if not self._data:
            print("<empty heap>")
            return
        parents = [-1] + [(i - 1) // 2 for i in range(1, len(self._data))]
        print("Values : ", "  ".join(f"{v:>2}" for v in self._data))
        print("Parents: ", "  ".join(f"{p:>2}" for p in parents))


if __name__ == "__main__":

    heap = MinHeap()

    '''
    for value in (5, 7, 15, 8, 11, 17, 16, 9):
        heap.add(value)

    print("\nInitial heap:")
    heap.draw()
    print("\nArray view (values / parent indices):")
    heap.display_array_and_parents()

    print("\ndelete() ->", heap.delete())
    heap.draw()
    heap.display_array_and_parents()
    print("\ndelete() ->", heap.delete())
    heap.draw()
    heap.display_array_and_parents()
    print("\nIn-order traversal:", heap.in_order())

    for value in (12, 18, 6):
        print(f"\nadd({value})")
        heap.add(value)
        heap.draw()
        heap.display_array_and_parents()

    print("\nFinal heap:")
    heap.draw()
    print("\nArray view:")
    heap.display_array_and_parents()
    print("\nFinal in-order traversal:", heap.in_order())
    '''

    for value in (5, 20, 30, 31, 60, 40):
        heap.add(value)
    heap.draw()

    heap.delete()
    heap.draw()