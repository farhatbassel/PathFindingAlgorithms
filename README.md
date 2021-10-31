# Traveling Salesman Problem
The following is the solution to the traveling salesman using a bit mask.

The problem is as follows: Given a n amount of nodes. Find the shortest path between all of them from a point and return to that point.

e.g.

 \ | A  | B  | C  | D
---|---|---|---|---
A | 0  | 10 | 15 | 20
B | 10  | 0 | 25 | 30
C | 15 | 25   | 0 | 35
D | 20 | 30  | 35  | 0

The code looks at the closest values in the nodes and gives the shortest route length and route.

# Functionality

- The following code also allows the addition, removal of nodes. 
- A rest key was also added to return to the default example.
- The is an option to view the code at any time.
- The code has a minimum requirement of 2 nodes.
