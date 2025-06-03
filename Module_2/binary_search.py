'''
Binary Search

• Strategy:
    • Eliminate about half the items left with one comparison. Data array is successively divided into two parts, thus the name binary.
• Pseudocode:
    • Look at the middle element
    • If target value == middle element -- DONE!
    • If target value > middle element -- must be in 2nd half
    • If target value < middle element -- must be in 1st half
'''


def binary_search(data: list[int], target: int):
    data_are_ascending = True
    if data[1] > data[0]:
        data_are_ascending = True
    else:
        data_are_ascending = False

    print("The sorted list is [" + ", ".join([str(datum) for datum in data]) + "].")
    print("There are " + str(len(data)) + " elements.")
    print("The list is in " + ("ascending" if data_are_ascending else "descending") + " order.")
    print("We are searching for " + str(target) + ".\n")

    low = 0
    high = len(data) - 1
    list_of_middle_indices = []
    while low <= high:
        middle = int((low + high) / 2)
        list_of_middle_indices.append(middle)
        print("Low, high, and middle indices are " + str(low) + ", " + str(high) + ", and " + str(middle) + ".")
        middle_element = data[middle]
        print("The middle element is " + str(middle_element) + ".")
        if target < middle_element:
            print("Target is less than middle element.")
        elif target > middle_element:
            print("Target is greater than middle element.")
        else:
            print("Target is equal to middle element.\n")

        if data_are_ascending:
            if target > data[middle]:
                low = middle + 1
                print("Low becomes " + str(low) + ".\n")
            elif target < data[middle]:
                high = middle - 1
                print("High becomes " + str(high) + ".\n")
            else:
                print("Target was found at index " + str(middle) + ".")
                print("List of middle indices was " + ', '.join([str(middle_index) for middle_index in list_of_middle_indices]) + ".")
                return
        
        else:
            if target > data[middle]:
                high = middle - 1
                print("High becomes " + str(high) + ".\n")
            elif target < data[middle]:
                low = middle + 1
                print("Low becomes " + str(low) + ".\n")
            else:
                print("Target was found at index " + str(middle) + ".")
                print("List of middle indices was " + ", ".join([str(middle_index) for middle_index in list_of_middle_indices]) + ".")
                return
    
    if low > high:
        print("Low is greater than high.")
    else:
        raise Exception("Low should be greater than high.")
    print("Target was not found.")
    print("List of middle indices was " + ', '.join([str(middle_index) for middle_index in list_of_middle_indices]) + ".")


if __name__ == "__main__":
    
    #data = [5, 12, 17, 23, 38, 44, 77, 84, 90]
    #target = 44

    #data = [15, 27, 33, 83, 92, 99]
    #target = 99

    #data = [9, 7, 6, 4, 3, 2, 1]
    #target = 6

    #data = [-1, 4, 5, 11, 13]
    #target = 4

    #data = [-5, -2, -1, 4, 5, 11, 13, 14, 17, 18]
    #target = 3

    data = [-1, 4, 5, 11, 13]
    target = 13
    
    binary_search(data, target)