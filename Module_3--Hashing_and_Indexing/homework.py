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

def hash(commodity: Commodity) -> int:
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
hash(list_of_commodities[0])
hash(list_of_commodities[len(list_of_commodities) - 1])
print(
'''
Complete the diagram below using the Chaining collision resolution technique:
'''
)

hash_table = {i: collections.deque() for i in range(HASH_TABLE_SIZE)}
dictionary_of_commodities_and_hash_codes = {}
for commodity in list_of_commodities:
    hash_code_of_commodity = hash(commodity)
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

'''
Output

PS C:\\Users\\thoma\\OneDrive\\Desktop> python .\\homework.py
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
'''