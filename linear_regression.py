def linear_regression_loops(X, y):
    '''
    X is an n x d matrix and may be thought of as a list of lists.
    y is a vector of length n.
    '''
    
    n = len(X) # Number of samples
    d = len(X[0]) # Number of features

    # 1. Transpose X: XT is d x n
    XT = [[0 for _ in range(n)] for _ in range(d)]
    for i in range(n):
        for j in range(d):
            XT[j][i] = X[i][j]

    # 2. Matrix Multiplication: XT * X -> XT_X (XT_X is d x d)
    XT_X = [[0 for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            sum_val = 0
            for k in range(n):
                sum_val += XT[i][k] * X[k][j]
            XT_X[i][j] = sum_val

    # 3. Matrix Inversion: inv(XT_X) -> inv_XT_X (d x d)
    inv_XT_X = np.linalg.inv(XT_X)

    # 4. Compute intermediate term: XT * y -> XT_y (d x 1)
    XT_y = [0 for _ in range(d)]
    for i in range(d): # Row of result (d)
        sum_val = 0
        for j in range(n): # Common dimension (n)
            sum_val += XT[i][j] * y[j]
        XT_y[i] = sum_val

    # 5. Final Multiplication: inv_XT_X * XT_y -> w (d x 1)
    w = [0 for _ in range(d)]
    for i in range(d):
        sum_val = 0
        for j in range(d):
            sum_val += inv_XT_X[i][j] * XT_y[j] #
        w[i] = sum_val

    return w