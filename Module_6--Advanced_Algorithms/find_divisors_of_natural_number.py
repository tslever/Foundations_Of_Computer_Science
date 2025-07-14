import math


def find_divisors_of_natural_number(n: int) -> list[int]:
    '''
    Return all positive divisors of a natural number n using a brute-force scan up to ⌊√n⌋.

    Parameters
    ----------
    n : int
        Natural number (n ≥ 1).

    Returns
    -------
    list[int]
        Sorted list of all divisors of n.
    '''
    if n < 1:
        raise ValueError("n must be a positive integer.")

    small_divs = [] # divisors ≤ sqrt(n)
    large_divs = [] # their complementary partners n // d

    limit = int(math.isqrt(n)) # ⌊√n⌋ using integer sqrt
    for d in range(1, limit + 1): # 1 ... ⌊√n⌋ inclusive
        if n % d == 0: # d divides n with no remainder
            small_divs.append(d)
            partner = n // d
            if partner != d: # avoid double-adding perfect-square root
                large_divs.append(partner)

    return small_divs + large_divs[::-1] # combine and keep ascending order


if __name__ == "__main__":
    print(find_divisors_of_natural_number(100))