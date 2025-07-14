def make_change(amount_cents: int) -> dict[int, int]:
    """
    Return the fewest-coin change for `amount_cents` using U.S. coins.

    Parameters
    ----------
    amount_cents : int
        Amount of change, in cents, to be returned.  Must be ≥ 0.

    Returns
    -------
    dict[int, int]
        Mapping coin value → quantity used (0 omitted for readability).
    """
    if amount_cents < 0:
        raise ValueError("Amount must be non-negative.")

    coin_values = (25, 10, 5, 1)     # ordered largest → smallest
    change: dict[int, int] = {}

    remaining = amount_cents
    for coin in coin_values:
        qty, remaining = divmod(remaining, coin)  # greedy choice
        if qty:                                   # record only if used
            change[coin] = qty
        if remaining == 0:                        # done early if exact
            break

    return change


# ---------- demo ----------
if __name__ == "__main__":
    for x in (0, 4, 17, 30, 87):
        print(f"{x:>3}¢ → {make_change(x)}")