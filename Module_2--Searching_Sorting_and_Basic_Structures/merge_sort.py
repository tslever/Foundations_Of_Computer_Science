def merge_sorted_lists(A, B):
    i = 0
    j = 0
    C = []
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            C.append(A[i])
            i += 1
        else:
            C.append(B[j])
            j += 1
    # extend with the remaining slice of whichever list is not exhausted
    C.extend(A[i:])
    C.extend(B[j:])
    return C