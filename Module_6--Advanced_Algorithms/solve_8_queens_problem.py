def solve_n_queens(n: int = 8) -> list[list[int]]:
    '''
    Return a list of solutions for the n-queens problem.
    Each solution is a length-n list whose i-th entry is the column
    where the queen is placed in row i (rows are 0-based, top-to-bottom).
    '''
    solutions: list[list[int]] = []

    def backtrack(row: int,
                  cols: set[int],
                  diag1: set[int],
                  diag2: set[int],
                  current: list[int]) -> None:
        if row == n:                 # placed queens in every row
            solutions.append(current[:])
            return
        for col in range(n):
            if (col in cols or
                (row - col) in diag1 or
                (row + col) in diag2):
                continue             # conflict – skip

            # place queen
            cols.add(col)
            diag1.add(row - col)     # “\” diagonal (r - c is constant)
            diag2.add(row + col)     # “/” diagonal (r + c is constant)
            current.append(col)

            backtrack(row + 1, cols, diag1, diag2, current)

            # remove queen (back-track)
            current.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0, set(), set(), set(), [])
    return solutions


if __name__ == "__main__":
    first = solve_n_queens()[0]   # grab one solution
    print("One 8-queens solution:\n")
    for r in range(8):
        row_str = "".join("Q " if first[r] == c else ". " for c in range(8))
        print(row_str)