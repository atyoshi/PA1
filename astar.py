import sys
import random
import math
# MAPS [(map_string, start_coord, goal_coord)...]
MAPS = [
    # MAP 1
    ("""
        2421452
        0123531
        2044124
        2553201
        4332101
     """,
        (1, 2),
        (4, 3)
    ),
    
    # MAP 2
    ("""
        1325143
        2131325
        3050122
        5321503
        2410020
        4021534
        1510241
     """,
        (3, 6),
        (5, 1)
    ),
    
    # MAP 3
    ("""
        2020200220
        1235212512
        2022121242
        2010111001
        1100503222
        2222101210
        1021314301
        2051521241
        1222020110
        5121112012
     """,
        (1, 2),
        (8, 8)
    ),
    
    # MAP 4
    ("""
        1111111311
        1234501234
        1111111111
        1010101010
        1133431111
        1098765432
        1111111111
        1010101010
        1114201111
        1111111111
     """,
        (0, 0),
        (9, 9)
    ),
    
    
    # MAP 5
    ("""
        3453453453
        2120122122
        3453453053
        2122122122
        3453053053
        2122122022
        3453050403
        2120122122
        3403053453
        2122122122
     """,
        (0, 0),
        (9, 9)
    )
]


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

import time

def h_func(child, end_node, heuristic):
    # Manhattan Distance
    manhattan = abs((child.position[0] - end_node.position[0])) + abs((child.position[1] - end_node.position[1]))
    
    if heuristic == 1: # H1: All Zeros
        return 0
    if heuristic == 2: # H2: Manhattan Distance
        return manhattan
    if heuristic == 3: # H3: Euclidean Distance (Custom)
        return math.sqrt((child.position[0] - end_node.position[0])**2 + (child.position[1] - end_node.position[1])**2)
    if heuristic == 4: # H4: Manhattan Distance - Error
        error = random.choice([-3,-2,-1,1,2,3])
        return max(0, manhattan + error)

def astar(maze, start, end, heuristic):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    
    # Start stopwatch
    start_time = time.time() #Time in seconds

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    
    # Nodes Created
    nodes_created = 1

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
                
            # Stop Stopwatch
            end_time = time.time()
            
            # Find running time in milliseconds
            duration_ms = (end_time - start_time) * 1000
            
            return (current_node.g, path[::-1], nodes_created, duration_ms) # Return Total Path Cost, Path Sequence, Node Count, Runtime

        # Generate children
        children = []
        
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            
            # Increment counter
            nodes_created += 1

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + maze[child.position[0]][child.position[1]]
            child.h = h_func(child,end_node, heuristic)
            child.f = child.g + child.h

            # Child is already in the open list
            skip = False
            for open_node in open_list:
                if child == open_node and child.g >= open_node.g:
                    skip = True
                    break

            # Add the child to the open list
            if not skip:
                open_list.append(child)
            
    # Stop Stopwatch
    end_time = time.time()    
    # Find running time in milliseconds
    duration_ms = (end_time - start_time) * 1000
            
    return (-1, "NULL", nodes_created, duration_ms)
            
    
def read_map_from_string(map_string):
    # Split the string into lines and strip whitespace
    lines = map_string.strip().split('\n')
    
    # Convert each character in each line into an integer
    # 0 = Impassable, 1-5 = Varying costs
    return [[int(char) for char in line.strip()] for line in lines] 

def main():
    # Ensure user provides enough arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py [map_number 1-5] [heuristic_number 1-4]")
        return

    # Map choice (1-5) and Heuristic choice (1-4)
    map_choice = int(sys.argv[1]) - 1
    heuristic_choice = int(sys.argv[2])
    
    # Map Selection
    maze = read_map_from_string(MAPS[map_choice][0])
    start = MAPS[map_choice][1]
    end = MAPS[map_choice][2]

    # A* with Chosen Heuristic
    result = astar(maze, start, end, heuristic_choice)
    
    print(f"1) Path Cost: {result[0]}")
    print(f"2) Path: {result[1]}")
    print(f"3) Nodes Created: {result[2]}")
    print(f"4) Runtime: {round(result[3],4)} ms")


if __name__ == '__main__':
    main()