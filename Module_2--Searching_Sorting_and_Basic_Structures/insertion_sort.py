'''
Insertion Sort

Time complexity is O(n) in best case and O(n^2) in average and worst cases.

• Insertion sort is a simple and appropriate algorithm for small inputs
• Most common sorting technique used by card players
• Procedure:
    • The list is divided into two parts: sorted and unsorted
    • In each pass, the first element of the unsorted part is picked up, transferred to the sorted sublist, and inserted at the appropriate (sorted) place
• A list of n elements will take at most n-1 passes to sort the data
'''


def insertion_sort(data):
    for j in range(1, len(data)):
        value = data[j]
        print("Value at data[" + str(j) + "] is " + str(value) + ".")
        i = j - 1
        # Advance elements in sorted sublist greater than value.
        while (i >= 0) and (data[i] > value):
            data[i + 1] = data[i]
            print(str(data[i]) + " was advanced from " + str(i) + " to " + str(i + 1) + ".")
            i = i - 1
        # Insert value in the gap.
        data[i + 1] = value
        print("Value was inserted at " + str(i + 1) + ".")
        print("Inserting value yields [" + ", ".join(str(datum) for datum in data) + "].\n")


if __name__ == "__main__":

    #data = [5, 2, 4, 6, 1, 3]
    data = [29, 20, 73, 34, 64]

    print("Data is [" + ", ".join(str(datum) for datum in data) + "].\n")
    insertion_sort(data)