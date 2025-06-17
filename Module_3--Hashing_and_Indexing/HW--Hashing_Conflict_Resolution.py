'''
Responses

Exercise 1: Hashing and Chaining with String keys
Let's assume the hash table size = 13
Use the hash function to load the following commodity items into the hash table:
onion,1,10.0
tomato,1,8.5
cabbage,3,3.5
carrot,1,5.5
okra,1,6.5
mellon,2,10.0
potato,2,7.5
Banana,3,4.0
olive,2,15.0
salt,2,2.5
cucumber,3,4.5
mushroom,3,5.5
orange,2,3.0

Will use ASCII code for the characters as follows:
character,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v
ASCII code,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118

For instance,

hash(onion) = (111 + 110 + 105 + 111 + 110) % 13 = 547 % 13 = 1
hash(orange) = (111 + 114 + 97 + 110 + 103 + 101) % 13 = 636 % 13 = 12

Complete the diagram below using the Chaining collision resolution technique:

hash(onion) = (111 + 110 + 105 + 111 + 110) % 13 = 547 % 13 = 1
hash(tomato) = (116 + 111 + 109 + 97 + 116 + 111) % 13 = 660 % 13 = 10
hash(cabbage) = (99 + 97 + 98 + 98 + 97 + 103 + 101) % 13 = 693 % 13 = 4
hash(carrot) = (99 + 97 + 114 + 114 + 111 + 116) % 13 = 651 % 13 = 1
hash(okra) = (111 + 107 + 114 + 97) % 13 = 429 % 13 = 0
hash(mellon) = (109 + 101 + 108 + 108 + 111 + 110) % 13 = 647 % 13 = 10
hash(potato) = (112 + 111 + 116 + 97 + 116 + 111) % 13 = 663 % 13 = 0
hash(Banana) = (98 + 97 + 110 + 97 + 110 + 97) % 13 = 609 % 13 = 11
hash(olive) = (111 + 108 + 105 + 118 + 101) % 13 = 543 % 13 = 10
hash(salt) = (115 + 97 + 108 + 116) % 13 = 436 % 13 = 7
hash(cucumber) = (99 + 117 + 99 + 117 + 109 + 98 + 101 + 114) % 13 = 854 % 13 = 9
hash(mushroom) = (109 + 117 + 115 + 104 + 114 + 111 + 111 + 109) % 13 = 890 % 13 = 6
hash(orange) = (111 + 114 + 97 + 110 + 103 + 101) % 13 = 636 % 13 = 12

0 |-|->|okra|-|->|potato|/|
1 |-|->|onion|-|->|carrot|/|
2 |-|->|/|
3 |-|->|/|
4 |-|->|cabbage|/|
5 |-|->|/|
6 |-|->|mushroom|/|
7 |-|->|salt|/|
8 |-|->|/|
9 |-|->|cucumber|/|
10 |-|->|tomato|-|->|mellon|-|->|olive|/|
11 |-|->|Banana|/|
12 |-|->|orange|/|

Item,Qty,Price,h(key)
onion,1,10.0,1
tomato,1,8.5,10
cabbage,3,3.5,4
carrot,1,5.5,1
okra,1,6.5,0
mellon,2,10.0,10
potato,2,7.5,0
Banana,3,4.0,11
olive,2,15.0,10
salt,2,2.5,7
cucumber,3,4.5,9
mushroom,3,5.5,6
orange,2,3.0,12

Exercise 2: Hashing and Linear Probing
Given this hash table's initial configuration: (Note: size of table = 13, 'E' = Empty state)
Index,Status,Value
0,E,None
1,E,None
2,E,None
3,E,None
4,E,None
5,E,None
6,E,None
7,E,None
8,E,None
9,E,None
10,E,None
11,E,None
12,E,None

1. Perform the operations in the table below showing the following two things after each operation:
    a. The hash index or the probe sequence if necessary
    b. A comment "Collision" / "Success" / "Fail" to indicate the appropriate event*
2. Show the final hash table after all the operations have been performed.
The first operation has been done for you:

Operation,Index or Probe Sequence,Comment
Insert(18),h_0(18) = (18 + 0) % 13 = 5,Success
Insert(26),h_0(26) = (26 + 0) % 13 = 0,Success
Insert(35),h_0(35) = (35 + 0) % 13 = 9,Success
Insert(9),h_0(9) = (9 + 0) % 13 = 9|h_1(9) = (9 + 1) % 13 = 10,Collision|Success
Find(15),h_0(15) = (15 + 0) % 13 = 2,Fail
Find(48),h_0(48) = (48 + 0) % 13 = 9|h_1(48) = (48 + 1) % 13 = 10|h_2(48) = (48 + 2) % 13 = 11,Collision|Collision|Fail
Find(9),h_0(9) = (9 + 0) % 13 = 9|h_1(9) = (9 + 1) % 13 = 10,Collision|Success
Insert(64),h_0(64) = (64 + 0) % 13 = 12,Success
Insert(47),h_0(47) = (47 + 0) % 13 = 8,Success
Find(35),h_0(35) = (35 + 0) % 13 = 9,Success

One entry in final hash table (notice the change of status from 'E' to 'O') [is the row with index 5]:

Index,Status,Value
0,O,26
1,E,None
2,E,None
3,E,None
4,E,None
5,O,18
6,E,None
7,E,None
8,O,47
9,O,35
10,O,9
11,E,None
12,O,64

* Note for Exercise 2 on when to use the "Collision" / "Success" / "Fail" comments:
    - "Collision"
        - Inserting but cell is occupied
        - Finding but something else is there
    - "Success"
        - Able to insert
        - Able to find
    - "Fail"
        - Unable to find [while linear probing you find a cell with status "Empty" ('E')]

Exercise 3: Additional questions

Q1) Name one advantage of Chaining over Linear Probing.
According to https://stackoverflow.com/questions/23821764/why-do-we-use-linear-probing-in-hash-tables-when-there-is-separate-chaining-link ,
"One weakness of linear probing is that, with a bad choice of hash function, primary clustering can cause the performance of the table to degrade significantly.
While chained hashing can still suffer from bad hash functions, it's less sensitive to elements with nearby hash codes, which don't adversely impact the runtime.".

Q2) Name one disadvantage of Chaining that isn't a problem in Linear Probing.
According to https://stackoverflow.com/questions/23821764/why-do-we-use-linear-probing-in-hash-tables-when-there-is-separate-chaining-link ,
"insertions into a linear probing hash table don't require any new allocations (unless you're rehashing the table),
so in applications like network routers where memory is scarce, it's nice to know that once the table is set up,
the elements can be placed into it with no risk of a malloc fail."
In contrast, chaining involves a new allocation of a linked list node for each inserted object.

Q3) If using Chaining, how can finding an element in the linked list be made more efficient?
Finding an element in a linked list in a hash table can be made more efficient by
resizing the hash table to keep linked lists short,
moving found elements to the front of the linked list (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431),      
sorting the linked list to allow stopping sorting after examining elements similar to but not equal to the element of interest (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431), or
replacing the linked list with an array, hash table, or Binary Search Tree (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431, https://en.wikipedia.org/wiki/Hash_table)

Q4) Why does Linear Probing require a three-state (Occupied, Empty, Deleted) "flag" for each cell, but Chaining does not?
Linear probing requires a three-state (Occupied, Empty, Deleted) "flag" for each cell
because linear probing in searching for an element checks for the element in all cells in which the element could be,
passes by occupied cells with different elements and cells from which elements were deleted most recently, and
stops after it checks an empty cell that has never been filled.
Linear probing checks for the element of interest in all occupied cells and cells from which elements were deleted
between the cell corresponding to the element's hash code inclusive and the nearest empty cell with a greater index inclusive.

When an element with a hash code is inserted into the corresponding cell of a hash table with linear probing,
a flag for that cell may change from "Empty" or "Deleted" to "Occupied".
If an element with a different hash code is inserted into the corresponding cell,
a flag for that cell may change from "Empty" or "Deleted" to "Occupied".
If an element with a previous hash code is inserted,
a collision occurs, the potential insertion cell is advanced
until the potential insertion cell has a flag of "Empty" or "Deleted",
and the element is placed and the flag is updated to "Occupied".
If an element is deleted from a cell, the corresponding flag may change from "Occupied" to "Deleted".
If an element with a hash code were searched for in the corresponding cell, and
an element had been deleted from that cell but the cell had no "Deleted" flag,
then the algorithm would assume incorrectly that because the cell was empty the element searched for was not in the hash table.
Due to potential insertion cells advancing, the element searched for might actually be in the next cell over.
If an element with a hash code were searched for in the corresponding cell, and
an element had been deleted from that cell and the cell had a "Deleted" flag,
then the algorithm would recognize that the element searched for was not in that cell and continue searching the hash table
until the algorithm arrived at an empty cell.

Chaining does not require a three-state flag for each cell
because when an element with a hash code is searched for
the element must be in the linked list corresponding to that hash code
and the linked list is usually searched linearly.
'''


import collections

HASH_TABLE_SIZE = 13

class Commodity():

    def __init__(self, name_to_use: str, number_to_use: int, price_to_use: float):
        self.name = name_to_use
        self.number = number_to_use
        self.price = price_to_use
    
    def __str__(self):
        return self.name + "," + str(self.number) + "," + str(self.price)

    def get_name(self) -> str:
        return self.name

def hash_function_for_exercise_1(commodity: Commodity) -> int:
    name_of_commodity = commodity.get_name()
    sum_of_ASCII_codes_of_characters_in_name_of_commodity = 0
    list_of_ASCII_codes_of_characters_in_name_of_commodity = []
    for character in name_of_commodity:
        lowercase_version_of_character = character.lower()
        ASCII_code_of_character = ord(lowercase_version_of_character)
        sum_of_ASCII_codes_of_characters_in_name_of_commodity += ASCII_code_of_character
        list_of_ASCII_codes_of_characters_in_name_of_commodity.append(ASCII_code_of_character)
    hash_code = sum_of_ASCII_codes_of_characters_in_name_of_commodity % HASH_TABLE_SIZE
    print("hash(" + name_of_commodity + ") = (" + ' + '.join([str(ASCII_code) for ASCII_code in list_of_ASCII_codes_of_characters_in_name_of_commodity]) + ") % " + str(HASH_TABLE_SIZE) + " = " + str(sum_of_ASCII_codes_of_characters_in_name_of_commodity) + " % " + str(HASH_TABLE_SIZE) + " = " + str(hash_code))
    return hash_code

def run_exercise_1():
    list_of_commodities = []

    list_of_commodities.append(Commodity("onion", 1, 10.00))
    list_of_commodities.append(Commodity("tomato", 1, 8.50))
    list_of_commodities.append(Commodity("cabbage", 3, 3.50))
    list_of_commodities.append(Commodity("carrot", 1, 5.50))
    list_of_commodities.append(Commodity("okra", 1, 6.50))
    list_of_commodities.append(Commodity("mellon", 2, 10.00))
    list_of_commodities.append(Commodity("potato", 2, 7.50))
    list_of_commodities.append(Commodity("Banana", 3, 4.00))
    list_of_commodities.append(Commodity("olive", 2, 15.00))
    list_of_commodities.append(Commodity("salt", 2, 2.50))
    list_of_commodities.append(Commodity("cucumber", 3, 4.50))
    list_of_commodities.append(Commodity("mushroom", 3, 5.50))
    list_of_commodities.append(Commodity("orange", 2, 3.00))

    print(
    '''Exercise 1: Hashing and Chaining with String keys
Let's assume the hash table size = ''' + str(HASH_TABLE_SIZE) + '''
Use the hash function to load the following commodity items into the hash table:
''' + '\n'.join([str(commodity) for commodity in list_of_commodities]) + '''

Will use ASCII code for the characters as follows:\n''' +
    "character," + ','.join([chr(i) for i in range(97, 118 + 1)]) + '\n' +
    "ASCII code," + ','.join([str(i) for i in range(97, 118 + 1)]) + '''

For instance,
    '''
    )
    hash_function_for_exercise_1(list_of_commodities[0])
    hash_function_for_exercise_1(list_of_commodities[len(list_of_commodities) - 1])
    print(
    '''
Complete the diagram below using the Chaining collision resolution technique:
    '''
    )

    hash_table = {i: collections.deque() for i in range(HASH_TABLE_SIZE)}
    dictionary_of_commodities_and_hash_codes = {}
    for commodity in list_of_commodities:
        hash_code_of_commodity = hash_function_for_exercise_1(commodity)
        deque_at_hash_code = hash_table[hash_code_of_commodity]
        deque_at_hash_code.append(commodity)
        dictionary_of_commodities_and_hash_codes[commodity] = hash_code_of_commodity

    print(
        '\n' + '\n'.join(
            [str(hash_code) + " |-|->" + "|-|->".join('|' + item.get_name() for item in deque) + "|/|" for hash_code, deque in hash_table.items()]
        )
    )

    print(
    '''
Item,Qty,Price,h(key)\n''' + '\n'.join([str(commodity) + "," + str(dictionary_of_commodities_and_hash_codes[commodity]) for commodity in list_of_commodities])
    )

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

def run_exercise_2():
    hash_table = {i: ['E', None] for i in range(0, HASH_TABLE_SIZE)}

    print(
'''
Exercise 2: Hashing and Linear Probing
Given this hash table's initial configuration: (Note: size of table = ''' + str(HASH_TABLE_SIZE) + ''', 'E' = Empty state)
Index,Status,Value\n''' + '\n'.join([str(i) + "," + the_list[0] + ',' + str(the_list[1]) for (i, the_list) in hash_table.items()]) + '''

1. Perform the operations in the table below showing the following two things after each operation:
    a. The hash index or the probe sequence if necessary
    b. A comment "Collision" / "Success" / "Fail" to indicate the appropriate event*
2. Show the final hash table after all the operations have been performed.
The first operation has been done for you:

Operation,Index or Probe Sequence,Comment'''
    )
    for integer in [18, 26, 35, 9]:
        probe_sequence, list_of_comments = insert(integer, hash_table)
        print("Insert(" + str(integer) + ")," + '|'.join(str(i) for i in probe_sequence) + ',' + '|'.join(comment for comment in list_of_comments))
    
    for integer in [15, 48, 9]:
        probe_sequence, list_of_comments = find(integer, hash_table)
        print("Find(" + str(integer) + ")," + '|'.join(str(i) for i in probe_sequence) + ',' + '|'.join(comment for comment in list_of_comments))

    for integer in [64, 47]:
        probe_sequence, list_of_comments = insert(integer, hash_table)
        print("Insert(" + str(integer) + ")," + '|'.join(str(i) for i in probe_sequence) + ',' + '|'.join(comment for comment in list_of_comments))

    for integer in [35]:
        probe_sequence, list_of_comments = find(integer, hash_table)
        print("Find(" + str(integer) + ")," + '|'.join(str(i) for i in probe_sequence) + ',' + '|'.join(comment for comment in list_of_comments))

    print(
        '''
One entry in final hash table (notice the change of status from 'E' to 'O') [is the row with index 5]:

Index,Status,Value\n''' +
        '\n'.join([str(i) + "," + the_list[0] + ',' + str(the_list[1]) for (i, the_list) in hash_table.items()]) + '\n' +
        '''
* Note for Exercise 2 on when to use the "Collision" / "Success" / "Fail" comments:
    - "Collision"
        - Inserting but cell is occupied
        - Finding but something else is there
    - "Success"
        - Able to insert
        - Able to find
    - "Fail"
        - Unable to find [while linear probing you find a cell with status "Empty" ('E')]
'''
    )

def run_exercise_3():
    print(
        '''Exercise 3: Additional questions

Q1) Name one advantage of Chaining over Linear Probing.
According to https://stackoverflow.com/questions/23821764/why-do-we-use-linear-probing-in-hash-tables-when-there-is-separate-chaining-link ,
"One weakness of linear probing is that, with a bad choice of hash function, primary clustering can cause the performance of the table to degrade significantly.
While chained hashing can still suffer from bad hash functions, it's less sensitive to elements with nearby hash codes, which don't adversely impact the runtime.".

Q2) Name one disadvantage of Chaining that isn't a problem in Linear Probing.
According to https://stackoverflow.com/questions/23821764/why-do-we-use-linear-probing-in-hash-tables-when-there-is-separate-chaining-link ,
"insertions into a linear probing hash table don't require any new allocations (unless you're rehashing the table),
so in applications like network routers where memory is scarce, it's nice to know that once the table is set up,
the elements can be placed into it with no risk of a malloc fail."
In contrast, chaining involves a new allocation of a linked list node for each inserted object.

Q3) If using Chaining, how can finding an element in the linked list be made more efficient?
Finding an element in a linked list in a hash table can be made more efficient by
resizing the hash table to keep linked lists short,
moving found elements to the front of the linked list (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431),
sorting the linked list to allow stopping sorting after examining elements similar to but not equal to the element of interest (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431), or
replacing the linked list with an array, hash table, or Binary Search Tree (https://stackoverflow.com/questions/27931175/how-to-improve-linked-list-searching-c/27932431#27932431, https://en.wikipedia.org/wiki/Hash_table)

Q4) Why does Linear Probing require a three-state (Occupied, Empty, Deleted) "flag" for each cell, but Chaining does not?
Linear probing requires a three-state (Occupied, Empty, Deleted) "flag" for each cell
because linear probing in searching for an element checks for the element in all cells in which the element could be,
passes by occupied cells with different elements and cells from which elements were deleted most recently, and
stops after it checks an empty cell that has never been filled.
Linear probing checks for the element of interest in all occupied cells and cells from which elements were deleted
between the cell corresponding to the element's hash code inclusive and the nearest empty cell with a greater index inclusive.

When an element with a hash code is inserted into the corresponding cell of a hash table with linear probing,
a flag for that cell may change from "Empty" or "Deleted" to "Occupied".
If an element with a different hash code is inserted into the corresponding cell,
a flag for that cell may change from "Empty" or "Deleted" to "Occupied".
If an element with a previous hash code is inserted,
a collision occurs, the potential insertion cell is advanced
until the potential insertion cell has a flag of "Empty" or "Deleted",
and the element is placed and the flag is updated to "Occupied".
If an element is deleted from a cell, the corresponding flag may change from "Occupied" to "Deleted".
If an element with a hash code were searched for in the corresponding cell, and
an element had been deleted from that cell but the cell had no "Deleted" flag,
then the algorithm would assume incorrectly that because the cell was empty the element searched for was not in the hash table.
Due to potential insertion cells advancing, the element searched for might actually be in the next cell over.
If an element with a hash code were searched for in the corresponding cell, and
an element had been deleted from that cell and the cell had a "Deleted" flag,
then the algorithm would recognize that the element searched for was not in that cell and continue searching the hash table
until the algorithm arrived at an empty cell.

Chaining does not require a three-state flag for each cell
because when an element with a hash code is searched for
the element must be in the linked list corresponding to that hash code
and the linked list is usually searched linearly.
'''
    )

if __name__ == "__main__":
    run_exercise_1()
    run_exercise_2()
    run_exercise_3()