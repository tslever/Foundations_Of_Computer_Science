'''
Bubble Sort

Time complexity is O(n^2) in worst case.

• Procedure:
    • The algorithm works by comparing each item in the list with the item next to it, and swapping them if required (if array[i] > array[j])
    • The name comes from the effect that the largest element in a given iteration of the algorithm “bubbles” its way to the top (bottom) of the array
    • The algorithm repeats this process until it makes a pass all the way through the list without swapping any items
'''


def bubble_sort(data):
    '''
    Bubble elements down to the bottom of the list of data.
    '''
    # For each element at index i from 0 inclusive to n exclusive...
    for i in range(0, len(data)):
        # For each element at index j from n - 1 inclusive to i exclusive...
        for j in range(len(data) - 1, i, -1):
            # If the element at j is less than that at j - 1, swap them.
            if data[j] < data[j - 1]:
                swap(data, j, j - 1)
        print("[" + ", ".join(str(datum) for datum in data) + "]")
    print("Final list is [" + ", ".join(str(datum) for datum in data) + "].")


def swap(data, x, y):
    temp = data[x]
    data[x] = data[y]
    data[y] = temp


if __name__ == "__main__":
    
    data = [7, 5, 2, 4, 3, 9]

    print("Data is [" + ", ".join(str(datum) for datum in data) + "].\n")
    bubble_sort(data)