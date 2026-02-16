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

def astar(maze, start, end):
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
    nodes_created = 2

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
            child.h = abs((child.position[0] - end_node.position[0])) + abs((child.position[1] - end_node.position[1]))
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
            
    
    


def main():

    maze = [
    [1, 5, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 5, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 5, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 5, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 5, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
# Start: (0,0), End: (4,5)

    start = (0, 0)
    end = (8, 0)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()