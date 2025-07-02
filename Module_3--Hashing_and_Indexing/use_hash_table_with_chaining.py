import collections

HASH_TABLE_SIZE = 10

def hash_function(whole_number: int) -> int:
    return whole_number % HASH_TABLE_SIZE

hash_table = {i: collections.deque() for i in range(HASH_TABLE_SIZE)}
for whole_number in [5, 29, 20, 0, 21, 15]:
    hash_code = hash_function(whole_number)
    deque_at_hash_code = hash_table[hash_code]
    deque_at_hash_code.append(whole_number)

print(
    '\n' + '\n'.join(
        [str(hash_code) + " |-|->" + "|-|->".join('|' + str(item) for item in deque) + "|/|" for hash_code, deque in hash_table.items()]
    )
)