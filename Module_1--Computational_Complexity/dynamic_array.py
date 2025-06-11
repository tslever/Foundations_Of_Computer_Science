class DynamicArray:
    def __init__(self):
        self._capacity = 1
        self._n = 0 # number of actual elements
        self._A = [None] * self._capacity

    def _resize(self, new_capacity):
        # Create new array B
        B = [None] * new_capacity

        # Copy elements from A to B
        for i in range(self._n):
            B[i] = self._A[i]

        # Update array reference and capacity
        self._A = B
        self._capacity = new_capacity

    def append(self, element):
        if self._n == self._capacity:
            # Resize to double capacity when full
            new_capacity = 2 * self._capacity
            self._resize(new_capacity)

        # Append element (after potential resize)
        self._A[self._n] = element
        self._n += 1