from reference import build_cave, shortest_path


def optimal_path(data):
    """optimal_path returns the length of the shortest path that enables Falca
    to collect all of the treasures and exit from the dungeon.

    data: a dictionary of features in the cave"""

    # An object holding info on the path
    class Node:
        def __init__(self, weight, visited, sword, treasures):
            self.visited = visited[:]
            self.cost = weight
            self.sword = sword
            self.treasures = treasures

    # Location of the sword
    sword_location = data['sword'] if 'sword' in data else (-1, -1)

    # Treasure locations
    treasure_locations = data['treasure'][:] if 'treasure' in data else []

    # All locations
    locations = [data['sword']] if 'sword' in data else []
    locations += [data['exit']] + treasure_locations

    # Entrance node
    node = Node(0, [data['entrance']], False, 0)

    # Add the first node onto the que
    unexplored = [(0, id(node), node)]

    while unexplored:

        # Our current position
        unexplored.sort(reverse=True)
        node = unexplored.pop(-1)[2]

        # Check for the sword
        if node.visited[-1] == sword_location:
            node.sword = True

        # We made it to the end, return the distance
        if node.visited[-1] == data['exit']:
            return node.cost

        # Find every spot we can go from here
        for spot in locations:
            if spot not in node.visited:

                # Dont exit without all the treasure
                if spot == data['exit'] and \
                        node.treasures < len(treasure_locations):
                    continue

                # If the new spot is reachable, add it to the que
                cost = shortest_path(data, node.visited[-1], spot, node.sword)
                if cost:
                    treasure = 1 if spot in treasure_locations else 0
                    new_node = Node(node.cost + cost, node.visited +
                                [spot], node.sword, node.treasures + treasure)
                    unexplored.append((new_node.cost, id(new_node), new_node))

    return None
