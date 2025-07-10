from typing import List, Any


def partition(A: List[Any], p: int, r: int) -> int:
    '''
    Rearrange A[p], A[p + 1], ..., A[r] around a pivot so that
    every element less than or equal to the pivot is to the left of the pivot and
    every element greater than pivot is to the right.
    Return the index where the pivot finally lands.
    Choose the last element A[r] as pivot.
    '''
    x = A[r] # The pivot is A[r].
    i = p - 1 # The index of the right edge of the list of elements less than or equal to the pivot is i.
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i] # Swap A[i] and A[j].
    A[i + 1], A[r] = A[r], A[i + 1] # Place pivot in its final spot.
    return i + 1


def quick_sort(A: List[Any], p: int = 0, r: int | None = None) -> List[Any]:
    '''
    Quick sort in place A[p], A[p + 1], ... A[r].
    By default, quick sort the whole list A.
    Divide: partition around a pivot, obtaining its final index q.
    Conquer: Quick sort the left and right parts separately.
    Combine: Don't do anything because concatenation is implicit because we're sorting in place.
    '''
    if r is None:
        r = len(A) - 1
    if p < r:
        q = partition(A, p, r)
        quick_sort(A, p, q - 1)
        quick_sort(A, q + 1, r)
    return A


if __name__ == "__main__":
    data = [19, 4, 88, 7, 3, 1, 42, 7]
    print("Before:", data)
    quick_sort(data)
    print("After: ", data)