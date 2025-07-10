def merge(array: list, first: int, mid: int, last: int) -> None:
    '''
    Merge two adjacent, already-sorted slices of array.
    Result is written back into array[first : last + 1].
    '''
    # Copy halves of the array into temporary lists.
    left_half = array[first : mid + 1]
    right_half = array[mid + 1 : last + 1]

    i = 0 # Define an index into the left half i.
    j = 0 # Define an index into the right half j.
    k = first # Define an index into the full array k.

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            array[k] = left_half[i]
            i += 1
        else:
            array[k] = right_half[j]
            j += 1
        k += 1

    # Place any leftovers.
    array[k : last + 1] = left_half[i:] or right_half[j:]


def merge_sort_in_place(array: list, first: int = 0, last: int | None = None) -> None:
    '''
    Perform in place, stable merge sort.
    Call with a list (e.g., `merge_sort(the_list)`) to sort the list.
    '''
    # Default to the last index of the array.
    if last is None:
        last = len(array) - 1

    if first < last:
        mid = (first + last) // 2
        merge_sort_in_place(array, first, mid) # Sort the left half of the array.
        merge_sort_in_place(array, mid + 1, last) # Sort the right half of the array.
        merge(array, first, mid, last) # Merge the two halves of the array.


def merge_sort(iterable) -> list:
    '''
    Merge Sort in place a copy of an iterable and provide that list.
    '''
    lst = list(iterable)
    merge_sort_in_place(lst)
    return lst


if __name__ == "__main__":
    print(merge_sort({8, 3, 2, 9, 7, 1, 5, 4}))