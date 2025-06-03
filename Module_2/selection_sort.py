'''
Selection Sort

Time complexity is O(n^2) in best, average, and worst cases.

• Procedure:
    • Algorithm works by selection the smallest unsorted item and then swapping it with the item in the next position to be filled
• Pseudocode:
    • Look through the entire array for the smallest element
    • Swap it with the first element of the array
    • Look for the smallest element in the remaining array (an array without the first element) and swap it with the second element
    • Keep going until done

• The data is divided into two sublists
    • Sorted and unsorted zones
• We find the smallest element from the unsorted sublist and swap it with the element at the beginning of the (same) unsorted data/list.
• This first element becomes the end of the sorted zone.
• Searching and swapping continues until the whole list has been sorted.
'''


def selection_sort(data):
    for i in range(0, len(data) - 1):
        min = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min]:
                min = j
        print("Element formerly at minimum index in unsorted sublist: " + str(data[i]))
        print("Smallest element in unsorted sublist: " + str(data[min]))
        temp = data[i]
        data[i] = data[min]
        data[min] = temp
        print("[" + ", ".join(str(datum) for datum in data) + "]\n")
    print("Final list is [" + ", ".join(str(datum) for datum in data) + "].")


if __name__ == "__main__":

    data = [29, 64, 73, 34, 20]

    print("Data is [" + ", ".join(str(datum) for datum in data) + "].\n")
    selection_sort(data)