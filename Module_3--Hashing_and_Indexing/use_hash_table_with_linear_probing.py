HASH_TABLE_SIZE = 10

def insert(integer: int, hash_table: dict[int, list]):
    probe_sequence = []
    list_of_comments = []
    index = integer % HASH_TABLE_SIZE
    #probe_sequence.append(index)
    number_of_probe = 0
    probe_sequence.append("h_" + str(number_of_probe) + "(" + str(integer) + ") = (" + str(integer) + " + " + str(number_of_probe) + ") % " + str(HASH_TABLE_SIZE) + " = " + str(index))
    number_of_statuses_checked = 0
    while hash_table[index][0] not in ['D', 'E']:
        number_of_statuses_checked += 1
        if number_of_statuses_checked > HASH_TABLE_SIZE:
            raise Exception("All statuses were checked.")
        list_of_comments.append("Collision")
        index = (index + 1) % HASH_TABLE_SIZE
        #probe_sequence.append(index)
        number_of_probe += 1
        probe_sequence.append("h_" + str(number_of_probe) + "(" + str(integer) + ") = (" + str(integer) + " + " + str(number_of_probe) + ") % " + str(HASH_TABLE_SIZE) + " = " + str(index))
    if hash_table[index][0] in ['D', 'E']:
        hash_table[index] = ['O', integer]
        list_of_comments.append("Success")
    else:
        raise Exception("Status is not 'D' or 'E'.")
    return probe_sequence, list_of_comments

def find(integer: int, hash_table: dict[int, list]):
    probe_sequence = []
    list_of_comments = []
    index = integer % HASH_TABLE_SIZE
    #probe_sequence.append(index)
    number_of_probe = 0
    probe_sequence.append("h_" + str(number_of_probe) + "(" + str(integer) + ") = (" + str(integer) + " + " + str(number_of_probe) + ") % " + str(HASH_TABLE_SIZE) + " = " + str(index))
    number_of_statuses_checked = 0
    while (hash_table[index][1] != integer) and (hash_table[index][0] != 'E'):
        number_of_statuses_checked += 1
        if number_of_statuses_checked > HASH_TABLE_SIZE:
            raise Exception("All statuses were checked.")
        list_of_comments.append("Collision")
        index = (index + 1) % HASH_TABLE_SIZE
        #probe_sequence.append(index)
        number_of_probe += 1
        probe_sequence.append("h_" + str(number_of_probe) + "(" + str(integer) + ") = (" + str(integer) + " + " + str(number_of_probe) + ") % " + str(HASH_TABLE_SIZE) + " = " + str(index))
    if hash_table[index][1] == integer:
        list_of_comments.append("Success")
    else:
        list_of_comments.append("Fail")
    return probe_sequence, list_of_comments

hash_table = {i: ['E', None] for i in range(0, HASH_TABLE_SIZE)}

for integer in [5, 29, 20, 0, 21, 15]:
    probe_sequence, list_of_comments = insert(integer, hash_table)
    print("Insert(" + str(integer) + ")," + '|'.join(str(i) for i in probe_sequence) + ',' + '|'.join(comment for comment in list_of_comments))

print(
    '''Index,Status,Value\n''' +
    '\n'.join([str(i) + "," + the_list[0] + ',' + str(the_list[1]) for (i, the_list) in hash_table.items()]) + '\n'
)