"""
Tromino tiling for a 2^n × 2^n board with one missing square
------------------------------------------------------------
Strategy (Divide & Conquer):
1. Divide the board into four quadrants.
2. Put one L-shaped tromino at the centre so it touches the three quadrants
   *without* the original missing square.  That creates a new “missing” square
   in each of those three quadrants.
3. Recursively tile the four quadrants (each is now a smaller instance of the
   same problem) until the 2 × 2 base case is reached.
The function returns an integer grid; identical numbers mark the three cells
belonging to the same tromino.
"""

from itertools import count
from typing import List

def tile_board(size: int, hole_r: int, hole_c: int) -> List[List[int]]:
    """Return an integer matrix representing a tromino tiling.

    Parameters
    ----------
    size   : power-of-two board dimension (2, 4, 8, …)
    hole_r : row index (0-based) of the missing square
    hole_c : column index (0-based) of the missing square
    """
    assert size & (size - 1) == 0 and size >= 2, "size must be a power of two ≥ 2"
    board = [[0] * size for _ in range(size)]
    next_id = count(1)                       # unique label generator for trominoes

    def fill(sr: int, sc: int, d: int, hr: int, hc: int):
        """
        sr, sc : top-left corner of current sub-board
        d      : dimension of current sub-board
        hr, hc : coordinates of the hole relative to the whole board
        """
        if d == 2:                           # -------- base case --------
            t_id = next(next_id)
            for r in range(sr, sr + 2):
                for c in range(sc, sc + 2):
                    if (r, c) != (hr, hc):
                        board[r][c] = t_id
            return

        # -------- recursive case --------
        mid = d // 2
        # indices of quadrant holes (initially the real hole only)
        quad_holes = [[sr + mid - 1, sc + mid - 1],   # top-left
                      [sr + mid - 1, sc + mid],       # top-right
                      [sr + mid,     sc + mid - 1],   # bottom-left
                      [sr + mid,     sc + mid]]       # bottom-right

        # Which quadrant already contains the real hole?
        quad = (hr >= sr + mid) * 2 + (hc >= sc + mid)
        quad_holes[quad] = [hr, hc]       # keep the genuine hole in its quadrant

        # Place central tromino covering the other three quadrants’ centres
        t_id = next(next_id)
        for k, (r, c) in enumerate(quad_holes):
            if k != quad:
                board[r][c] = t_id

        # Recurse into four quadrants
        for k in range(4):
            dr = sr + (k // 2) * mid
            dc = sc + (k % 2) * mid
            hr_sub, hc_sub = quad_holes[k]
            fill(dr, dc, mid, hr_sub, hc_sub)

    fill(0, 0, size, hole_r, hole_c)
    return board


def print_board(board: List[List[int]]) -> None:
    """Pretty-print the tiled board (fixed-width columns)."""
    width = len(str(max(max(row) for row in board)))  # widest number
    for row in board:
        print(" ".join(f"{cell:>{width}}" if cell else "·" * width for cell in row))
    print()


if __name__ == "__main__":
    # ---------- demo ----------
    cases = [
        (2, 0, 0),         # 2×2
        (4, 1, 2),         # 4×4
        (8, 5, 6),         # 8×8
    ]
    for sz, hr, hc in cases:
        print(f"Tiling a {sz}×{sz} board (hole at row {hr}, col {hc}):")
        print_board(tile_board(sz, hr, hc))