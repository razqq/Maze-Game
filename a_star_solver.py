import math


class Cell:
    """Class cell for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        """
        The init function for the class: g is the distance between the current node and the start node, f is the total
        cost of the nod, and h is the heuristic(estimated distance from the current node to the end node). f = g + h
        :param parent:
        :param position:
        """
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        """
        Function that verifies if two cells are the same
        :param other:
        :return: True if so, False otherwise
        """
        return self.position == other.position


def astar(maze, start, end, distance_type):
    history = []
    """
    This method returns a list of tuples as the path from the start to the end of the maze
    :param maze: the maze path will be searched on
    :param start: the start position
    :param end: the end position
    :return: a list of tuples as the path from the start to the end of the maze
    """

    # Create the start cell
    start_cell = Cell(None, start)
    start_cell.g = 0
    start_cell.f = 0
    start_cell.h = 0

    # Create the end cell
    end_cell = Cell(None, end)
    end_cell.g = 0
    end_cell.f = 0
    end_cell.h = 0

    # Initialize the open and closed list
    open_list = []
    closed_list = []

    # Append the start node to the open list
    open_list.append(start_cell)

    # Main loop of the algorithm (stops when the player reaches the end cell)
    while 0 < len(open_list):
        # Get the current node from the open list
        current_cell = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_cell.f:
                current_cell = item
                current_index = index

        # Move the current cel from the open list to the closed list
        open_list.pop(current_index)
        closed_list.append(current_cell)

        # Set the current position as blocked for future use
        maze[current_cell.position[0]][current_cell.position[1]] = 0

        # Check if the player found the goal (reached the end cell), and returns the reversed path
        # print(current_cell.position, current_cell.parent, end_cell.position, end_cell.parent)
        if current_cell == end_cell:
            path = []
            current = current_cell
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], history

        # Generate children
        children = []

        if distance_type == 0:  # Directions using diagonal distance
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:  # Directions using manhattan distance
            directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        for new_position in directions:

            # Get the cell position
            cell_position = (current_cell.position[0] + new_position[0], current_cell.position[1] + new_position[1])

            # Check if the cell position is within range
            if cell_position[0] > (len(maze) - 1) or cell_position[0] < 0 or cell_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or cell_position[1] < 0:
                continue
            # Check it the position is empty and is not a block
            if maze[cell_position[0]][cell_position[1]] != 1:
                continue

            # Create the new cell and append it to the children list
            new_cell = Cell(current_cell, cell_position)
            # if new_cell in closed_list:
            #     continue
            children.append(new_cell)

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                # Create the f, g, and h values
                child.g = current_cell.g + 1
                # H: Manhattan distance to end point
                if distance_type == 0:
                    child.h = math.sqrt((child.position[0] - end_cell.position[0]) **2 + (child.position[1] - end_cell.position[1]) ** 2)
                else:
                    child.h = abs(child.position[0] - end_cell.position[0]) + abs(child.position[1] - end_cell.position[1])
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worst or equal
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    # Add the child to the open list
                    open_list.append(child)
        history.append([o.position for o in open_list])
    return [], history

if __name__ == '__main__':
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (0, 9)
    path = astar(maze, start, end)
    print(path)
