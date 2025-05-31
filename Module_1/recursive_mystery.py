def recursive_mystery(data):
    n = len(data)
    # Base case
    if n <= 1:
       return 1

    # Recursive step: Divide into 3 parts (approx n/3)
    size_third = n // 3
    part1 = data[0 : size_third]
    part2 = data[size_third : 2 * size_third]
    part3 = data[2 * size_third : n]

    # Make 3 recursive calls
    res1 = recursive_mystery(part1)
    res2 = recursive_mystery(part2)
    res3 = recursive_mystery(part3)

    # Combine step:
    count = 0
    for i in range(n):
        # Performing some constant time work per element
        count += (i + res1 + res2 + res3) % 100

    return count