from reference import build_cave, shortest_path


def optimal_path(data):
    """optimal_path returns the length of the shortest path that enables Falca
    to collect all of the treasures and exit from the dungeon.

    data: a dictionary of features in the cave"""

    # An object holding info on the path
    class Node:
        def __init__(self, weight, visited, treasures, sword):
            self.cost = weight
            self.visited = visited[:]
            self.treasures = treasures
            self.sword = sword

    # Location of the sword
    sword_location = data['sword'] if 'sword' in data else (-1, -1)

    # Treasure locations
    treasure_locations = data['treasure'] if 'treasure' in data else []

    # All locations
    locations = [data['exit']] + treasure_locations
    locations += [data['sword']] if 'sword' in data else []

    # Entrance node
    node = Node(0, [data['entrance']], 0, False)

    # Add the first node onto the que
    unexplored = [(0, id(node), node)]

    while unexplored:

        # Our current position
        unexplored.sort()
        node = unexplored.pop(0)[2]

        # Check for the sword
        if node.visited[-1] == sword_location:
            node.sword = True

        # We made it to the end, return the distance
        if node.visited[-1] == data['exit']:
            return node.cost

        # Find every location we can go from here
        for spot in locations:
            if spot not in node.visited:

                # Dont exit without all the treasure
                if spot == data['exit'] and \
                        node.treasures < len(treasure_locations):
                    continue

                # If the location is reachable, add it to the que
                cost = shortest_path(data, node.visited[-1], spot, node.sword)
                if cost:
                    treasure = 1 if spot in treasure_locations else 0
                    new_node = Node(node.cost + cost, node.visited +
                                [spot], node.treasures + treasure, node.sword)
                    unexplored.append((new_node.cost, id(new_node), new_node))

    return None
