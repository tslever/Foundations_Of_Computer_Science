# Revise the following code to resolve the following error.

'''
Gerrymandering HW
Instructions
Implement a dynamic programming solution to the Gerrymandering Problem as defined in class and in accompanying presentation.
Test code on synthetic and real data set(s) as indicated in exercises below.

Storage
For data storage and retrieval SQLite is used.
Here, we establish a connection to the database and define a cursor to be used throughout.
'''

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats  as stats
import math
import numpy as np

conn = sqlite3.connect('gerrymander.db')
cursor = conn.cursor()

recreate = True
if recreate == True:
  cursor.execute("DROP TABLE IF EXISTS precinct")
  cursor.execute("DROP TABLE IF EXISTS party")
  cursor.execute("DROP VIEW IF EXISTS for_algo")
  conn.commit()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
  cursor.fetchall()

'''
Data and scripts on GitHub
The scripts for building the database, including the data and schema, are in a github repository.
urllib3 library is used to communicate over https.
'''

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
gitread = urllib3.PoolManager()

'''
1) Provide an Introduction
Provide a Formal Problem Statement, define all variables needed, and state all assumptions.

Problem Statement: Gerrymandering
The purpose of this problem is to study Dynamic Programming by considering a Gerrymandering case study. Gerrymandering is the manipulation of electoral district boundaries to favor one's political party over other political parties. Gerrymandering is redistricting to benefit one or more political parties. A "Gerrymander" was depicted in an 1812 political cartoon after Governor Elbridge Gerry signed a bill that redistricted Massachusetts to benefit the Democratic-Republican Party. Virginia's fifth district looks like the original Gerrymander. Gerrymandering in the United States may be unconstitutional. According to [Politico](https://www.politico.com/story/2017/10/03/supreme-court-gerrymandering-wisconsin-arguments-243401), in 2017 Supreme Court Associate Justice Anthony Kennedy believed that extreme partisan Gerrymandering might violate the Constitution. On 09/03/2019, in Common Cause v. Lewis, the Wake County Superior Court ruled that a state legislative map violated the North Carolina Constitution. In hearings after Bethune-Hill v. Virginia State Board of Elections was remanded on 03/01/2017, the United States District Court for the Eastern District of Virginia held that redistricting in 2011 involved unconstitutional racial Gerrymandering. On 06/27/2019, in Rucho v. Common Cause, the Supreme Court of the United States ruled that federal courts cannot review allegations of partisan Gerrymandering.

Gerrymandering works by political parties maximizing the number of districts in a state with a majority of voters favoring that party.  Districts in a state have roughly the same number of voters. States and districts are composed of precincts. All precincts have the same number of voters.

We can conduct Gerrymandering as follows. Consider a set of precincts $P = {p_1, p_2, ..., p_n}$ representing all voters in a state. Let a precinct $p$ contain $m$ voters. The state has $s = mn$ voters. Define a district $D$ as a proper subset of $P$. Determine $d$ districts $D_1, D_2, ..., D_d$ that represent all voters in a state and meet the following criteria. $d = 2$. The number of precincts in $D_1$ is equal to the number of precincts in $D_2$. By extension, the number of voters in $D_1$ is equal to the number of voters in $D_2$. The sum of the number of voters $R(D_1)$ and $R(D_2)$ in $D_1$ and $D_2$ who favor party $R$ is greater than $\frac{s}{2}$. By extension, the number of voters $R(D_1)$ or $R(D_2)$ in $D_1$ or $D_2$ who favor party $R$ is greater than $\frac{s}{2d} = \frac{s}{4}$. Note if such districts cannot be determined.


2) Dynamic Programming Solution.
Formally define the solution and state the recurrence used.
Identify how it employs dynamic programming and clearly explain and justify. 
Solution must
1) Determine if Gerrymandering is possible and if gerrymandering is possible
2) provide the associated precinct re-assignment.
Be clear and explain how.

Dynamic Programming is a way of solving complex problems by dividing them into similar sub-problems, and then combining the solutions of sub-problems to achieve an overall "optimal" solution. The results of sub-problems are memoized; i.e., stored to avoid working on the same sub-problem again and to eliminate unnecessary repetition. Dynamic Programming seeks to solve each sub-problem only once.

Dynamic Programming requires "optimal substructure"; the solution to a larger problem must contain the solutions to smaller problems.

To conduct Dynamic Programming, we will identify a recursive structure of our problem. We will select a good order for solving subproblems. We may solve each problem in a "top down" manner or recursively. We may solve each problem in a "bottom up" manner or iteratively from smallest problem to largest problem. We will save the solution to each subproblem in memory.

We formally define a Dynamic Programming Solution as follows. Let boolean $b(j, k, x, y)$ be true if there exists an assignment of the first $j$ precincts in a state such that exactly $k$ precincts are assigned to district $D_1$, $x$ voters in those $k$ precincts in $D_1$ favor party $R$, and exactly $y$ voters in the remaining $j - k$ precincts in district $D_2$ favor party $R$. We define $b(0, 0, 0, 0)$ to be true and $b(0, k, x, y)$ to be false. Recall that $n$ is the number of precincts in the state. The goal of Gerrymandering is to see if there exists a value $x > \frac{s}{4}$ and a value $y > \frac{s}{4}$ such that $b(n, \frac{n}{2}, x, y)$ is true.

Suppose $b(j, k, x, y)$ is true and there are precincts $p_1$, $p_2$, ..., $p_j$ in the state. $p_j$ must be in either $D_1$ or $D_2$.

If $p_j$ is in $D_1$, then $b(j, k, x, y)$ is true if $b(j - 1, k - 1, x - R(p_j), y)$ is true; i.e., if we can assign $k - 1$ out of the first $j - 1$ precincts to $D_1$ such that exactly $x - R(p_j)$ voters in $D_1$ favor $R$ and exactly $y$ voters in $D_2$ favor $R$. If we can, then we can assign $k$ out of the first $j$ precincts to $D_1$ such that exactly $x$ voters in $D_1$ favor $R$ and exactly $y$ voters in $D_2$ favor $R$.

If $p_j$ is in $D_2$, then $b(j, k, x, y)$ is true if $b(j - 1, k, x, y - R(p_j))$ is true; i.e., if we can assign $k$ out of the first $j - 1$ precincts to $D_1$ such that exactly $x$ voters in $D_1$ favor $R$ and exactly $y - R(p_j)$ voters in $D_2$ favor $R$. If we can, then we can assign $k$ out of the first $j$ precincts to $D_1$ such that exactly $x$ voters in $D_1$ favor $R$ and exactly $y$ voters in $D_2$ favor $R$.

Since $p_j$ is in $D_1$ or $D_2$, $b(j, k, x, y)$ is true if $b(j - 1, k - 1, x - R(p_j), y)$ is true or $b(j - 1, k, x, y - R(p_j))$. In math, $b(j, k, x, y) = b(j - 1, k - 1, x - R(p_j), y) OR b(j - 1, k, x, y - R(p_j))$.

Because each boolean refers only to booleans with a smaller first index $j - 1$, Gerrymandering exhibits the optimal substructure and overlapping subproblem requirements for dynamic programming.

Use a tabulation algorithm to determine whether Gerrymanding is possible.

```
Let s be number of voters in state.
Let goal equal s / 4. Each district needs a number of voters favoring party R that is greater than goal.
Create a 4D Boolean array b[j][k][x][y] where j ranges from 0 to n, k ranges from 0 to n, x ranges from 0 to s, and y ranges from 0 to s.
Create a 4D character array parent[j][k][x][y] that stores '1' if p_j was put in D_1 and '2' if p_j was put in D_2.
Set b[0][0][0][0] to True.
for j in [1, n]:
    Define r to be R(p_j), the number of voters in precinct p_j who favor party R.
    for k in [0, j]:
        for x in [0, s]:
            for y in [0, s]:
                if (k > 0 and x >= r and b[j-1][k-1][x-r][y]) or (y >= r and b[j-1][k][x][y-r]):
                    Set b[j][k][x][y] to True.
                    Set parent[j][k][x][y] to '1' if (k > 0 and x >= r and b[j-1][k-1][x-r][y]) or '2' otherwise.

for x in [goal + 1, s]:
    for y in [goal + 1, s]:
        if b[n][n/2][x][y] is True:
            Gerrymandering is possible.
            Reconstruct assignment.
            Record j, k, x, and y.
            Stop.
Gerrymandering is impossible.
```

If Gerrymandering is possible, we add p_j, p_{j-1}, ...., p_0 to D_1 or D_2.

```
Define D_1 to be an empty set of precincts.
Define D_2 to be an empty set of precincts.
while j > 0:
    if parent[j][k][x][y] equals '1':
        Add p_j to D_1.
        Set k to k - 1.
        Set x to x - R(p_j).
    otherwise:
        Add p_j to D2.
        Set y to y - R(p_j).
    Set j to j - 1.
Reverse D_1.
Reverse D_2.
```

3) Implement your Gerrymandering Algorithm
Provide ample comments and justify each line of code.
You may wish to use or implement a sparse matrix (or something similar) to store the "memos".
'''

import pandas as pd # Import pandas for processing data frames.
from collections import defaultdict # Import defaultdict for defining a sparse memo.


def helpDetermineWhetherGerrymanderPossible(precinct_data: pd.DataFrame):
    '''
    Decide whether the precincts of the provided data frame can be split into 2 districts with the same number of precincts
    such that the majority of voters in each district favor party R.

    Parameters
    precinct_data is a data frame with column "REP_VOTES" containing numbers of voters who favor party R in various precincts.

    Returns
    An indicator of whether Gerrymanding is possible is returned.
    A data frame of assignments of precincts to district is returned if the indicator is True. Otherwise None is returned.

    Side Effects
    This function prints an assignment of precincts to districts when Gerrymandering is possible.
    '''

    if "Total_Votes" in precinct_data.columns:
        array_of_unique_total_values = precinct_data["Total_Votes"].unique()
        if len(array_of_unique_total_values) != 1:
            raise ValueError("All precincts must contain the same number of voters.")
        voters_per_precinct = int(array_of_unique_total_values[0])
    else:
        voters_per_precinct = 100

    precincts_per_district = len(precinct_data) // 2
    votes_per_district = precincts_per_district * voters_per_precinct
    number_of_voters_needed_in_each_district = votes_per_district / 2

    # Check that column "REP_VOTES" is present so that the following code does not fail.
    if "REP_VOTES" not in precinct_data.columns:
        raise ValueError("DataFrame must contain column \"REP_VOTES\".")
    
    # Extract list of numbers of voters who favor party R for various purposes.
    list_of_numbers_of_voters_who_favor_party_R = precinct_data["REP_VOTES"].tolist()

    # Extract precinct IDs and numbers of voters who favor party R for printing precinct split.
    list_of_IDs_of_precincts = precinct_data.index.tolist()

    # The number of precincts in the state must be even so that each district can have half of the precincts.
    number_of_precincts_in_state = len(list_of_numbers_of_voters_who_favor_party_R)
    if number_of_precincts_in_state % 2 != 0:
        raise ValueError(f"The districts must have the same number of precincts.")
    
    # Each district must have a number of voters who favor party R greater than majority
    # so that the 2 districts together have a majority of voters who favor R in the state.
    number_of_voters_who_favor_party_R_in_state = sum(list_of_numbers_of_voters_who_favor_party_R)
    
    # j is the number of the first precincts that have been placed in districts.
    # k is the number of the first j processed precincts that have been placed in district D_1.
    # x is the total number of voters who favor party R in D_1.
    # y is the total number of voters who favor party R in D_2.
    # Create a sparse memo to minimize memory usage when the number of possible configurations of precincts is huge.
    # memo is a dictionary that maps values of k to sets of values of x
    # achievable after added a set of precincts {p_1, p_2, ..., p_j} to D_1 or D_2.
    # A redundant state is a tuple (j, k, x, y).
    # y can be determined based on j, k, and x.
    # A full state is a tuple (j, k, x).
    # A reachable full state is a full state reflecting a concrete assignment of the first j precincts.
    # A j-based state is a tuple (k, x).
    # A reachable j-based state is a j-based state reflecting a concrete assignment of the first j precincts.
    # memo represents all j-based states.
    # Creating memo is more memory efficient than creating a dense 4D tensor of Booleans b[j][k][x][y] representing redundant states.
    # Most permutations of values j, k, x, and y are not reachable.
    memo = defaultdict(set)
    memo[0].add(0) # With 0 precincts we have 0 voters who favor party R in D_1.

    # parent is a dictionary that records, for every reachable full state (j, k, x),
    # a tuple of the indices in the preceding j-based state and an indicator of which district the jth precinct was assigned.
    # These items allow us to reconstruct 1 valid assignment of precincts to districts
    # once Dynamic Programming has found a full state for which Gerrymandering is possible.
    parent = {}

    # Iterate over every precinct.
    for j, r in enumerate(list_of_numbers_of_voters_who_favor_party_R, start = 1):
        # j is the index of a precinct in [1, n] and the length of the set of precincts {p_1, p_2, ..., p_n}.
        # r is the number of voters who favor party R in precinct j.
        
        next_memo = defaultdict(set) # We build our next memo from scratch.
        
        # For each currently reachable pair (k, x), branch on whether p_j is placed in D_1 or D_2.
        for k, xs in memo.items(): # k represents the number of precincts in D_1.
            for x in xs: # x represents the number of voters who favor party R in D_1.
                if k + 1 <= number_of_precincts_in_state // 2: # We consider placing precinct j in district 1.
                    
                    # The number of precincts in District 1 k + 1 cannot exceed half of the number of precincts in the state.
                    if x + r not in next_memo[k + 1]:
                        
                        # We store for each full state a tuple of the indices of the preceding j-based state and an indicator of D_1
                        # because any single valid path indicates that Gerrymandering is possible and
                        # allows us to build a concrete assignment of precincts to districts.
                        parent[(j, k + 1, x + r)] = (k, x, 1) # 1 indicates district D_1.

                    next_memo[k + 1].add(x + r)

                # Consider placing precinct j in District 2.
                # In this case, k and x remain unchanged.
                if x not in next_memo[k]:
                    parent[(j, k, x)] = (k, x, 2) # 2 indicates district D_2.
                
                next_memo[k].add(x)
        memo = next_memo

    # Search for any full state (n, n/2, x) for which  the numbers of voters who favor party R in both districts is greater than majority.
    full_state = None
    for x in memo.get(number_of_precincts_in_state // 2, set()): # District 1 must contain n/2 precincts.
        y = number_of_voters_who_favor_party_R_in_state - x # District 2 has the voters in the remaining precincts.
        if x > number_of_voters_needed_in_each_district and y > number_of_voters_needed_in_each_district:
            # Both x and y must be greater than number of voters needed in each district.
            full_state = (number_of_precincts_in_state, number_of_precincts_in_state // 2, x)
            break
    if full_state is None:
        # We have exhausted all reachable full states without satisfying the majority condition.
        # Gerrymandering is impossible.
        return False, None
    
    # Reconstruct one concrete assignment of precincts to districts.
    assignment = [None] * number_of_precincts_in_state # assignment holds 1 or 2 for each precinct.
    j, k, x = full_state
    while j > 0:
        k_prev, x_prev, choice = parent[(j, k, x)]
        assignment[j - 1] = choice
        j, k, x = j - 1, k_prev, x_prev

    # Print out the precinct split and voter split.    
    # Print the precinct split, a data frame that lists every precinct and the district to which the precinct was assigned.
    df = pd.DataFrame(
        {
            'Precinct' : list_of_IDs_of_precincts,
            'RedVotes' : list_of_numbers_of_voters_who_favor_party_R,
            'District' : assignment
        }
    )
    print(df.to_string(index = False))
    # Print the voter split, the numbers of voters who favor R in D_1 and D_2.
    number_of_voters_who_favor_R_in_D1 = sum(r for r, lab in zip(list_of_numbers_of_voters_who_favor_party_R, assignment) if lab == 1)
    number_of_voters_who_favor_R_in_D2 = sum(r for r, lab in zip(list_of_numbers_of_voters_who_favor_party_R, assignment) if lab == 2)
    print(f"The number of voters who favor party R in district D_1 is {number_of_voters_who_favor_R_in_D1}.")
    print(f"The number of voters who favor party R in district D_2 is {number_of_voters_who_favor_R_in_D2}.")

    return True, assignment # True indicates that Gerrymandering is possible.


def isGerrymanderPossible(precinct_data) -> bool:
    '''
    Determine if gerrymandering is possible given a dataframe that contains
    REP voting and Total votes for precincts in two neighboring districts.
    Return True or False, and if True, print out the precinct split and voter split.
    '''
    indicator, data_frame = helpDetermineWhetherGerrymanderPossible(precinct_data)
    return indicator


'''
4) Algorithmic Analysis
TODO: Provide a time complexity analysis of your algorithms in terms of the size and /or parameters of the input.
Be clear and precise.
TODO: Provide comprehensive justification and state all assumptions. 


5) Test your algorithm
Run your algorithm on the example data set below.
Is gerrymandering possible?
Create two other synthtetic data sets (dataframes ... like the one below):
one where gerrymandering is possible and one where gerrymandering is not possible.
Confirm your hypothesis using your implementation. 
'''

'''
precinct_data = pd.DataFrame()
precinct_data = precinct_data.append(pd.DataFrame({"PRECINCT":"DUMMY ROW","District": 0,"REP_VOTES":0, "DEM_VOTES": 0, "Total_Votes": 0},index=[0]))
precinct_data = precinct_data.append(pd.DataFrame({"PRECINCT":"92","District": 1,"REP_VOTES":65, "DEM_VOTES": 35, "Total_Votes": 100},index=[0]))
precinct_data = precinct_data.append(pd.DataFrame({"PRECINCT":"93","District": 1,"REP_VOTES":60, "DEM_VOTES": 40, "Total_Votes": 100},index=[0]))
precinct_data = precinct_data.append(pd.DataFrame({"PRECINCT":"94","District": 2,"REP_VOTES":45, "DEM_VOTES": 55, "Total_Votes": 100},index=[0]))
precinct_data = precinct_data.append(pd.DataFrame({"PRECINCT":"95","District": 2,"REP_VOTES":47, "DEM_VOTES": 53, "Total_Votes": 100},index=[0]))
precinct_data.reset_index(inplace = True)    
precinct_data.drop('index',axis=1,inplace=True)
'''
rows = [
    {"PRECINCT": "92", "District": 1, "REP_VOTES": 65, "DEM_VOTES": 35, "Total_Votes": 100},
    {"PRECINCT": "93", "District": 1, "REP_VOTES": 60, "DEM_VOTES": 40, "Total_Votes": 100},
    {"PRECINCT": "94", "District": 2, "REP_VOTES": 45, "DEM_VOTES": 55, "Total_Votes": 100},
    {"PRECINCT": "95", "District": 2, "REP_VOTES": 47, "DEM_VOTES": 53, "Total_Votes": 100},
]
precinct_data = pd.concat([pd.DataFrame([r]) for r in rows], ignore_index=True)


LetsRun = isGerrymanderPossible(precinct_data)

if LetsRun:
    print("Gerrymandering is possible.")
else:
    print("Gerrymandering is not possible.")

df_possible = pd.DataFrame(
    {"REP_VOTES": [55, 55, 55, 55]}, index=["A", "B", "C", "D"]
)

df_impossible = pd.DataFrame(
    {"REP_VOTES": [90, 2, 2, 2]}, index=["X", "Y", "Z", "W"]
)

print("\n---- Test 2 (should be POSSIBLE) ----")
print("Result:", isGerrymanderPossible(df_possible))

print("\n---- Test 3 (should be IMPOSSIBLE) ----")
print("Result:", isGerrymanderPossible(df_impossible))

'''
Precinct  RedVotes  District
        0        65         2
        1        60         1
        2        45         1
        3        47         2
The number of voters who favor party R in district D_1 is 105.
The number of voters who favor party R in district D_2 is 112.
Gerrymandering is possible.

---- Test 2 (should be POSSIBLE) ----
Precinct  RedVotes  District
       A        55         1
       B        55         1
       C        55         2
       D        55         2
The number of voters who favor party R in district D_1 is 110.
The number of voters who favor party R in district D_2 is 110.
Result: True

---- Test 3 (should be IMPOSSIBLE) ----
Result: False
'''

'''
# 6) Real-world Data Trials
There are voter data from 5 states available herein: Alaska, Arizona, Kentucky, North Carolina, and Rhode Island.
For this question you are asked to analyze Arizona and Kentucky Data. 
Note: In the example below the data is "preprocessed" to match our assumptions and downsized for reasonable experimental runtimes. 

Notes about the tables
The create statements are stored in scripts in github including tables.sql.
Two tables in the schema:
* Precinct: Holds all data for precincts, districts, and number of voter registrations by party. There is a row for every party in each precinct, so precinct is not a unique key. Additionally, within states, precinct is not unique, it must be used with district.
* Party: An id and party name, just to keep the party data consistent within our database - party names and abbreviations change between states, but here we want them to be consistent. Party can be joined with precinct on precinct.party = party.id
'''

create_tables = 'https://raw.githubusercontent.com/boltonvandy/gerrymander/main/State_Data/tables.sql'
dat = gitread.request("GET", create_tables)
cursor.executescript(dat.data.decode("utf-8"))
view_def = ''' 
CREATE VIEW for_algo AS
SELECT * FROM
((SELECT STATE, PRECINCT, DISTRICT, VOTERS as REP_VOTES
FROM precinct WHERE PARTY = 'REP') NATURAL JOIN (
SELECT STATE, PRECINCT, DISTRICT, SUM(VOTERS) as Total_Votes
FROM precinct
WHERE (PARTY = 'REP' OR PARTY = 'DEM') 
GROUP BY STATE, PRECINCT, DISTRICT))
'''
cursor.execute(view_def)
conn.commit()
ourtables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
if ourtables:
  print('\nTables in the Gerrymander Database\n')
  for atable in ourtables:
    print("\t"+atable[0])

'''
Tables in the Gerrymander Database

	precinct
	party
'''

'''
## Example usage: Arizona
Here,the data from Arizona is loaded into the database.
[Original Arizona Data on Kaggle](https://www.kaggle.com/arizonaSecofState/arizona-voter-registration-by-precinct)
'''

cursor.execute("DELETE FROM precinct WHERE STATE = 'AZ'")
conn.commit()
az_url = 'https://raw.githubusercontent.com/boltonvandy/gerrymander/main/State_Data/az/az.insert.sql'
dat = gitread.request("GET", az_url)
cursor.executescript(dat.data.decode("utf-8"))
conn.commit()
cursor.execute("SELECT count(*) from precinct")
verify = cursor.fetchone()[0]
cursor.execute("SELECT sum(voters), party from precinct where state = 'AZ' group by party order by 1 DESC")
print(verify, cursor.fetchall())

'''
7270 [(1308384, 'REP'), (1251984, 'OTH'), (1169259, 'DEM'), (32096, 'LBT'), (6535, 'GRN')]
'''

'''
6a) Arizona Districts 1,2,&3

In this example, assume Districts 1/2 and 2/3 are neighboring and that precincts can be reassigned between them.
Confirm (both using your code and manually) that Gerrymandering is possible between districts 2 & 3, but not 1 & 2 (given the preprocessing steps, assumptions, and downsampling done below).
For the former, what is the Precinct breakdown?
Your answer should be shown as code output. 
'''

import math


def show_revised_district_totals(df_pair: pd.DataFrame, assignment: list | None) -> None:
    if assignment is None:
        print(
            "We manually check that an assignment of precincts to districts resulting in Gerrymandered districts exists.\n"
            "helpDetermineWhetherGerrymanderPossible did not find an assignment.\n"
            "We conclude that Gerrymandering is not possible."
        )
        return
    print("We manually check that the numbers of voters who favor party R in each district are greater than 200.")
    df_pair["new_number_of_district"] = assignment
    d1 = df_pair[df_pair["new_number_of_district"] == 1]
    d2 = df_pair[df_pair["new_number_of_district"] == 2]
    d1_total = d1["REP_VOTES"].sum()
    d2_total = d2["REP_VOTES"].sum()
    print("Below are new precincts in the first district and the numbers of voters who favor party R in those precincts.")
    print(d1[["PRECINCT", "REP_VOTES"]].to_string(index = False))
    print(f"The total number of voters who favor party R in the first district is {d1_total}.")
    print("Below are new precincts in the second district and the numbers of voters who favor party R in those precincts.")
    print(d2[["PRECINCT", "REP_VOTES"]].to_string(index = False))
    print(f"The total number of voters who favor party R in the second district is {d2_total}.")
    print(f"It is {"true" if d1_total > 200 and d2_total > 200 else "false"} that each district has more than 200 voters who favor party R.")


def run_gerrymander_trial(df_pair: pd.DataFrame, label: str) -> None:

    print(f"\n----- Gerrymandering trial for {label} -----")
    print("Input precinct data for 2 districts rescaled to 100 voters per precinct is the following.")
    print(df_pair.to_string(index = False))
    print("isGerrymanderingPossible is being run on the precinct data for 2 districts.")
    possible, assignment = helpDetermineWhetherGerrymanderPossible(df_pair)
    verdict = "is possible" if possible else "is not possible"
    print(f"Gerrymandering {verdict} for {label}.")
    if possible:
      print("The table printed above by the algorithm shows 1 valid precinct reassignment and the resulting per-district R totals.")
    show_revised_district_totals(df_pair, assignment)
    print("-----")

# To inspect the raw data see here: https://github.com/boltonvandy/gerrymander/tree/main/State_Data

# Using top 4 precincts only for each district 
# Districts 1 and 2 are not gerrymanderable
# Districts 2 and 3 are gerrymanderable 
# Feel free to use the following preprocessing steps
#   and downsampling scheme for all experimental trials 
# Here we assume only 2 parties (Rep and Dem), all voters vote along party lines, and data is 
#   rescaled to 100 total voters per precinct.


# First query database by district and state, take top 4 
#   precincts, and append both districts into one dataframe

sql = '''
SELECT * FROM for_algo WHERE state = 'AZ' AND (DISTRICT = 1)
'''
Arizona_dh = pd.read_sql_query(sql, conn).head(4)

sql = '''
SELECT * from for_algo where state = 'AZ' AND (DISTRICT = 2) 
'''
Arizona_di = pd.read_sql_query(sql, conn)
Arizona_di = Arizona_di.head(4)

sql = '''
SELECT * from for_algo where state = 'AZ' AND ( DISTRICT = 3) 
'''
Arizona_dj = pd.read_sql_query(sql, conn)
Arizona_dj = Arizona_dj.head(4)

Arizona_1_2 = pd.concat([Arizona_dh, Arizona_di], ignore_index = True)
'''
Arizona = Arizona_di.append(Arizona_dj)
Arizona = Arizona.reset_index(drop=True)
'''
Arizona = pd.concat([Arizona_di, Arizona_dj], ignore_index=True)

# Rescale data to match our assumptions (for these trials)

Arizona_1_2["REP_VOTES"] = (Arizona_1_2["REP_VOTES"] / Arizona_1_2["Total_Votes"] * 100).round().astype(int)
Arizona_1_2["Total_Votes"] = 100
Arizona["REP_VOTES"] = Arizona["REP_VOTES"] / Arizona["Total_Votes"] 
Arizona["REP_VOTES"] = pd.Series([math.ceil(Arizona["REP_VOTES"][x]*100) for x in range(len(Arizona.index))])
Arizona["Total_Votes"] = pd.Series([100 for x in range(len(Arizona.index))])

#Arizona.sort_values(by=['REP_VOTES'], ascending=False ,inplace=True)

print("Districts 2 and 3:")
print(Arizona)

if isGerrymanderPossible(Arizona):
  print("GerryMandering Possible In Arizona District")
else:
  print("GerryMandering Not Possible In Arizona District")

run_gerrymander_trial(Arizona_1_2, "Arizona districts 1 & 2")
run_gerrymander_trial(Arizona, "Arizona districts 2 & 3")

'''
Districts 2 and 3:
  STATE PRECINCT DISTRICT  REP_VOTES  Total_Votes
0    AZ   CH0001        2         65          100
1    AZ   CH0002        2         75          100
2    AZ   CH0003        2         63          100
3    AZ   CH0004        2         18          100
4    AZ   MC0016        3         36          100
5    AZ   MC0029        3         76          100
6    AZ   MC0037        3         26          100
7    AZ   MC0062        3         53          100
 Precinct  RedVotes  District
        0        65         2
        1        75         2
        2        63         1
        3        18         2
        4        36         1
        5        76         1
        6        26         1
        7        53         2
The number of voters who favor party R in district D_1 is 201.
The number of voters who favor party R in district D_2 is 211.
GerryMandering Possible In Arizona District

----- Gerrymandering trial for Arizona districts 1 & 2 -----
Input precinct data for 2 districts rescaled to 100 voters per precinct is the following.
STATE PRECINCT DISTRICT  REP_VOTES  Total_Votes
   AZ   AP0002        1         75          100
   AZ   AP0003        1         15          100
   AZ   AP0005        1         17          100
   AZ   AP0009        1         79          100
   AZ   CH0001        2         64          100
   AZ   CH0002        2         75          100
   AZ   CH0003        2         63          100
   AZ   CH0004        2         18          100
isGerrymanderingPossible is being run on the precinct data for 2 districts.
Gerrymandering is not possible for Arizona districts 1 & 2.
We manually check that an assignment of precincts to districts resulting in Gerrymandered districts exists.
helpDetermineWhetherGerrymanderPossible did not find an assignment.
We conclude that Gerrymandering is not possible.
-----

----- Gerrymandering trial for Arizona districts 2 & 3 -----
Input precinct data for 2 districts rescaled to 100 voters per precinct is the following.
STATE PRECINCT DISTRICT  REP_VOTES  Total_Votes
   AZ   CH0001        2         65          100
   AZ   CH0002        2         75          100
   AZ   CH0003        2         63          100
   AZ   CH0004        2         18          100
   AZ   MC0016        3         36          100
   AZ   MC0029        3         76          100
   AZ   MC0037        3         26          100
   AZ   MC0062        3         53          100
isGerrymanderingPossible is being run on the precinct data for 2 districts.
 Precinct  RedVotes  District
        0        65         2
        1        75         2
        2        63         1
        3        18         2
        4        36         1
        5        76         1
        6        26         1
        7        53         2
The number of voters who favor party R in district D_1 is 201.
The number of voters who favor party R in district D_2 is 211.
Gerrymandering is possible for Arizona districts 2 & 3.
The table printed above by the algorithm shows 1 valid precinct reassignment and the resulting per-district R totals.
We manually check that the numbers of voters who favor party R in each district are greater than 200.
Below are new precincts in the first district and the numbers of voters who favor party R in those precincts.
PRECINCT  REP_VOTES
  CH0003         63
  MC0016         36
  MC0029         76
  MC0037         26
The total number of voters who favor party R in the first district is 201.
Below are new precincts in the second district and the numbers of voters who favor party R in those precincts.
PRECINCT  REP_VOTES
  CH0001         65
  CH0002         75
  CH0004         18
  MC0062         53
The total number of voters who favor party R in the second district is 211.
It is true that each district has more than 200 voters who favor party R.
-----
'''

'''
6b) Kentucky Districts

In this example, find two districts that are gerrymanderable and two that are not.
Perform similar preprocessing steps as done in the Arizona data set, eg select 4 precincts, downsample and rescale.
Confirm both district pairs using your code and manually.
For the district pair that is gerrymanderable, what is the Precinct breakdown?
Your answer should be shown as code output. 
'''

## Kentucky!
# NOTE: the Kentucky Districts are stored as Strings. Be sure to build your query correctly :)
# See here: https://github.com/boltonvandy/gerrymander/tree/main/State_Data

cursor.execute("DELETE FROM precinct WHERE STATE = 'KY'")
conn.commit()

ky_url = 'https://raw.githubusercontent.com/boltonvandy/gerrymander/main/State_Data/ky/ky.insert.sql'

## GET contents of the script from a github url 
dat = gitread.request("GET", ky_url)

## INSERT Data using statements from the github insert script
cursor.executescript(dat.data.decode("utf-8"))
conn.commit()

## Quick verification that data was loaded for this state
cursor.execute("SELECT count(*) from precinct")
verify = cursor.fetchone()[0]

cursor.execute("SELECT sum(voters), party from precinct where state = 'KY' group by party order by 1 DESC")
print(verify, cursor.fetchall())

'''
40498 [(1649790, 'DEM'), (1576259, 'REP'), (184839, 'OTH'), (131242, 'IND'), (14326, 'LBT'), (2014, 'GRN'), (1012, 'CONST'), (322, 'SOCWK'), (157, 'REFORM')]
'''

#Kentucky

# Select and downsample district pairs 1 & 2.
KY_d1 = pd.read_sql_query(
    "SELECT * FROM for_algo WHERE STATE = 'KY' AND CAST(DISTRICT AS INTEGER) = 1",
    conn
).head(4)
KY_d2 = pd.read_sql_query(
    "SELECT * FROM for_algo WHERE STATE = 'KY' AND CAST(DISTRICT AS INTEGER) = 2",
    conn
).head(4)
KY_1_2 = pd.concat([KY_d1, KY_d2], ignore_index=True)

# Select and downsample district pairs 3 & 4.
KY_d3 = pd.read_sql_query(
    "SELECT * FROM for_algo WHERE STATE = 'KY' AND CAST(DISTRICT AS INTEGER) = 3",
    conn
).head(4)
KY_d4 = pd.read_sql_query(
    "SELECT * FROM for_algo WHERE STATE = 'KY' AND CAST(DISTRICT AS INTEGER) = 4",
    conn
).head(4)
KY_3_4 = pd.concat([KY_d3, KY_d4], ignore_index=True)

# Rescale both dataframes to 100 voters per precinct.
for df in (KY_1_2, KY_3_4):
    df["REP_VOTES"]   = pd.to_numeric(df["REP_VOTES"],   errors="raise")
    df["Total_Votes"] = pd.to_numeric(df["Total_Votes"], errors="raise")
    df["REP_VOTES"]   = (df["REP_VOTES"] / df["Total_Votes"] * 100).round().astype(int)
    df["Total_Votes"] = 100

# Run trials.
run_gerrymander_trial(KY_1_2, "Kentucky districts 1 & 2")
run_gerrymander_trial(KY_3_4, "Kentucky districts 3 & 4")


'''
----- Gerrymandering trial for Kentucky districts 1 & 2 -----
Input precinct data for 2 districts rescaled to 100 voters per precinct is the following.
STATE PRECINCT   DISTRICT  REP_VOTES  Total_Votes
   KY     A102 1-16-051-3         34          100
   KY     A104 1-16-051-3         26          100
   KY     A105 1-16-051-3         88          100
   KY     B102 1-16-051-3         32          100
   KY     A101 2-09-023-2         45          100
   KY     A102 2-09-023-2         43          100
   KY     A103 2-09-023-2         50          100
   KY     A104 2-09-023-2         53          100
isGerrymanderingPossible is being run on the precinct data for 2 districts.
Gerrymandering is not possible for Kentucky districts 1 & 2.
We manually check that an assignment of precincts to districts resulting in Gerrymandered districts exists.
helpDetermineWhetherGerrymanderPossible did not find an assignment.
We conclude that Gerrymandering is not possible.
-----

----- Gerrymandering trial for Kentucky districts 3 & 4 -----
Input precinct data for 2 districts rescaled to 100 voters per precinct is the following.
STATE PRECINCT   DISTRICT  REP_VOTES  Total_Votes
   KY     A105 3-37-028-4         34          100
   KY     A107 3-37-028-4         34          100
   KY     A108 3-37-028-4         40          100
   KY     A111 3-37-028-4         40          100
   KY     A102 4-11-060-6         72          100
   KY     A103 4-11-066-6         73          100
   KY     A104 4-11-066-6         69          100
   KY     A105 4-11-060-6         75          100
isGerrymanderingPossible is being run on the precinct data for 2 districts.
 Precinct  RedVotes  District
        0        34         1
        1        34         1
        2        40         2
        3        40         2
        4        72         1
        5        73         2
        6        69         1
        7        75         2
The number of voters who favor party R in district D_1 is 209.
The number of voters who favor party R in district D_2 is 228.
Gerrymandering is possible for Kentucky districts 3 & 4.
The table printed above by the algorithm shows 1 valid precinct reassignment and the resulting per-district R totals.
We manually check that the numbers of voters who favor party R in each district are greater than 200.
Below are new precincts in the first district and the numbers of voters who favor party R in those precincts.
PRECINCT  REP_VOTES
    A105         34
    A107         34
    A102         72
    A104         69
The total number of voters who favor party R in the first district is 209.
Below are new precincts in the second district and the numbers of voters who favor party R in those precincts.
PRECINCT  REP_VOTES
    A108         40
    A111         40
    A103         73
    A105         75
The total number of voters who favor party R in the second district is 228.
It is true that each district has more than 200 voters who favor party R.
-----
'''