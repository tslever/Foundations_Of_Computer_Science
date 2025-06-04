'''
Module ICA explores classic searching and sorting algorithms.
'''


'''
Searching Algorithms
'''

def search_linear(arr, tgt):
    '''
    Scan array from left to right until target is found.
    '''

    # Pseudocode
    # n <- size of the array
    # i <- 0 ~ n - 1
        # arr[i] == tgt
            # if match: i
            # if not: move on
    
    '''
    First implementation
    n = len(arr)
    for i in range(n):
        if arr[i] == tgt:
            return i
    return -1
    '''

    for i, value in enumerate(arr):
        if value == tgt:
            return i
    return -1


def search_binary(arr, tgt):
    '''
    This function assumes that array is sorted in ascending order and searches iteratively.
    '''

    # Pseudocode
    # std, end <- arr[0], arr[-1]
    # compute mid between start and end
    # arr[mid] == tgt: return mid
    # arr[mid] > tgt: st = mid
    # arr[mid] <= tgt

    '''
    First implementation
    n = len(arr)
    st, end = 0, n - 1

    if arr[st] == tgt:
        return st
    if arr[end] == tgt:
        return end
    
    while True:
        mid = ((end - st) // 2) + st
        
        if mid == end or mid == st: # checking end case
            return -1

        if arr[mid] == tgt: # hit, found target
            return mid
        elif arr[mid] >= tgt: # tgt is on left half
            end = mid
        else: # target is on right half
            st = mid
    '''

    st = 0
    end = len(arr) - 1

    while st <= end:
        mid = (st + end) // 2
        if arr[mid] == tgt:
            return mid
        if arr[mid] < tgt:
            st = mid + 1
        else:
            end = mid - 1
    return -1


'''
Sorting Algorithms
'''

def sort_selection(arr):

    # Pseudocode
    # i: 0 ~ n - 1
        # j: i ~ n
            # arr[i] > arr[j]
                # find the index for minimum comparing i and j
    
    '''
    First implementation
    n = len(arr)
    for i in range(0, n - 1): # st to end-1: sorted
        min_val = arr[i]
        min_idx = i
        for j in range(1, n): # i to end: unsorted
            if arr[j] < min_val:
                min_val = arr[j]
                min_idx = j
        # swap
        temp = arr[i]
        arr[i] = min_val
        arr[min_idx] = temp
    return arr
    '''

    n = len(arr)
    for i in range(0, n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        temp = arr[i]
        arr[i] = arr[min_idx]
        arr[min_idx] = temp
    return arr


def divide(arr, pivot_idx):
    '''
    This function is a helper used by function `sort_quick`.
    '''

    arr_left = []
    arr_right = []
    n = len(arr)
    for i in range(n):
        if i == pivot_idx:
            continue
        if arr[i] <= arr[pivot_idx]:
            arr_left.append(arr[i])
        else:
            arr_right.append(arr[i])
    return arr_left, arr_right

def sort_quick(arr):
    '''
    This function is recursive.
    '''

    # Pseudocode
    # pivot
    # divide: left array & right array
    # repeat 1-2 until there's no more to split
    # combine

    if len(arr) <= 1:
        return arr
    pivot_idx = len(arr) // 2
    left_arr, right_arr = divide(arr, pivot_idx)
    sorted_left = sort_quick(left_arr)
    sorted_right = sort_quick(right_arr)

    return sorted_left + [ arr[pivot_idx] ] + sorted_right


def sort_shell(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


if __name__ == "__main__":

    '''
    1) Linear Search
    a) Given an unsorted list of integers [23, 1, 45, 34, 17], write a linear search algorithm to find the position of the number 34.
    The position of 34 is 3. See above implementation of function `search_linear`.

    b) Advantages of Linear Search
    Linear search is simple to implement and doesn't require the data to be sorted.
    
    c) Disadvantages
    Linear search is inefficient for large arrays and compares each element of the array to the target.

    d) Time Complexity
    Time complexity is
    O(1) in best case when first element of array matches target,
    O(n) in average case when about half the array is searched, and
    O(n) in worst case when entire list is searched or target is not found.

    e) When Would You Use This Algorithm
    I would use this algorithm when array is small or when the algorithm is used once in a while.
    '''
    arr = [23, 1, 45, 34, 17]
    tgt = 34
    print(search_linear(arr, tgt)) # 3

    tgt = 23
    print(search_linear(arr, tgt)) # 0

    tgt = 17
    print(search_linear(arr, tgt)) # 4

    tgt = 21
    print(search_linear(arr, tgt)) # -1


    '''
    2) Binary Search
    a) Given a sorted list of integers [1, 4, 7, 9, 15, 24, 30], implement a binary search algorithm to find the position of the number 15.
    The position of 15 is 4. See above implementation of function `search_binary`.

    b) Advantages of Binary Search
    Binary search is fast given constant time complexity in best case and logarithmic time complexity in average and worst cases.
    Binary search is relatively simple.

    c) Disadvantages
    Binary search requires array to be sorted.
    Binary search would slow down if looking up middle element of array had time complexity other than O(1), such as with linked lists.

    d) Time Complexity
    Time complexity is
    O(1) in best case when middle element matches target,
    O[log(n)] in average case, and
    O[log(n)] in worst case.

    e) Binary search is ideal when
    Binary search is ideal when finding targets in large, sorted arrays.
    '''
    arr = [1, 4, 7, 9, 15, 24, 30]
    tgt = 15
    print(search_binary(arr, tgt)) # 4

    tgt = 0
    print(search_binary(arr, tgt)) # -1


    '''
    3) Selection Sort
    a) Given an unsorted list [34, 17, 23, 1, 45], write a selection sort algorithm to sort the list.
    The sorted list is [1, 17, 23, 34, 45]. See above implementation of function `sort_selection`.
    
    b) Advantages
    In place selection sort doesn't use much memory and involves a number of swaps equal to the number of elements in the array minus 1.
    
    c) Disadvantages
    Selection sort has quadratic time complexity and is not stable.

    d) Time complexity
    Time complexity is
    O(n^2) in the best case,
    O(n^2) in the average case, and
    O(n^2) in the worst case.

    e) When Would You Use This Algorithm
    I would use this algorithm when the array is small or the cost of swaps dominates the costs of comparisons.
    '''
    arr = [34, 17, 23, 1, 45]
    print(sort_selection(arr)) # [1, 17, 23, 34, 45]


    '''
    4) Quick Sort
    a) Given an unsorted list [12, 4, 5, 6, 7, 3, 1, 15], write a quick sort algorithm to sort the list.
    The sorted list is [1, 3, 4, 5, 6, 7, 12, 15]. See above implementation of function `sort_quick`.
    
    b) Advantages
    Quick sort has good time complexity in best and average cases.
    In place quick sort uses O[log(n)] space.

    c) Disadvantages
    Quick sort has poor time complexity in worst case, is not stable, and is overkill for small arrays.

    d) Time Complexity
    Time complexity is
    O[nlog(n)] in best case,
    O[nlog(n)] in average case, and
    O(n^2) in worst case.

    e) When Would You Use This Algorithm
    I would use this algorithm when array is large or when memory is limited given space complexity O[log(n)].
    '''
    arr = [12, 4, 5, 6, 7, 3, 1, 15]
    print(sort_quick(arr)) # [1, 3, 4, 5, 6, 7, 12, 15]


    '''
    5) Shell Sort
    As a group, answer the following questions regarding Shell Sort:
    a. General Description of the algorithm
    According to Wikipedia, shell sort is a generalized version of insertion sort that allows the exchange of elements that are far apart.
    Shell sort sorts elements separated by a gap that may be thought of as being in a subarray, then reduces gap between elements.
    Let h be a gap that might start at n // 2, where n is the number of elements in array.
    Shell sort arranges array so that, starting anywhere, taking every hth element produces a sorted list.
    Alternatively, shell sort arranges array so that that array consists of h interleaved sorted arrays.

    Consider an array of 1024 numbers.
    Let h start at 512.
    Ensure each element in first half of array is less than corresponding element in second half.
    Redefine h as 256.
    Ensure each element in first quarter of array is less than corresponding element in second quarter,
    each element in second quarter is less than corresponding element in third quarter, and
    each element in third quarter of array is less than corresponding element in fourth quarter.
    Redefine h as 128, 64, 32, 16, 8, 4, 2, and 1.
    When h is 1, shell sort performs insertion sort.

    Consider an example run of shell sort with gaps 5, 3, and 1.
                    a1	a2	a3	a4	a5	a6	a7	a8	a9	a10	a11	a12
    Input data	    62	83	18	53	07	17	95	86	47	69	25	28
    After 5-sorting	17	28	18	47	07	25	83	86	53	69	62	95
    After 3-sorting	17	07	18	47	28	25	69	62	53	83	86	95
    After 1-sorting	07	17	18	25	28	47	53	62	69	83	86	95

    b. State at least one advantage of shell sort.
    Shell sort allows elements to move long distances initially, reducing disorder quickly and reducing later work.
    Shell sort executes faster when array is partially sorted than when array is random.
    Shell sort is simple and may be faster than sorts with time complexity O[n^2].

    c. State at least one of the disadvantages of shell sort.
    Shell sort may be slower than sorts like merge sort with time complexity O[nlog(n)].
    Shell sort is unstable.

    d. State the complexity and briefly explain why it has that complexity.
    Time complexity is

    O[nlog(n)] in best case.
    For a gap h, insertion sort is performed on h interleaved subarrays of length ceiling(n / h).
    The number of comparisons in the best case of insertion sort on a subarray is n/h.
    For h interleaved subarrays, the number of comparisons in the best case is hn/h = n.
    For gaps n/2, n/4, n/8, ..., 1, the number of comparisons in the best case is
    n + n + n ... + n =
    nlog(n)
    The corresponding time complexity is O[nlog(n)].
    
    If time complexity of insertion sort in average case is O(n^2), then time complexity of shell sort in average case may be O(n^2).

    O(n^2) in worst case.
    For a gap h, insertion sort is performed on h interleaved subarrays of length ceiling(n / h).
    The number of comparisons in the worst case of insertion sort on a subarray is (n/h)^2.
    For h interleaved subarrays, the number of comparisons in the worst case is h(n/h)^2 = hn^2/h^2 = n^2/h.
    For gaps n/2, n/4, n/8, ..., 1, the number of comparisons in the worst case is
    n^2/(n/2) + n^2/(n/4) + n^2/(n/8) ... + n^2/1 =
    2n + 4n + 8n + ... nn =
    sum from i = 0 to log_2(n) of n^2/(n/2^i) =
    sum from i = 0 to log_2(n) of n 2^i =
    n sum from i = 0 to log_2(n) of 2^i =
    n [pow(2, upper limit + 1) - 1] =
    n {pow[2, log_2(n) + 1] - 1} =
    n {2 pow[2, log_2(n)] - 1} =
    n {2n - 1} =
    2n^2 - n
    The corresponding time complexity is O(n^2).

    e. When would you use this algorithm
    I would use this algorithm when array when I want simple code and sorting in place.
    '''
    arr = [12, 4, 5, 6, 7, 3, 1, 15]
    print(sort_shell(arr)) # [1, 3, 4, 5, 6, 7, 12, 15]