from reference import build_cave, shortest_path
from heapq import heappush, heappop


def search(data, locations):
    """search returns the shortest path between the entry and exit after
    visiting the required locations

    data:       a dictionary of features in the cave
    locations:  list holding the locations of the treasure and sword"""

    # A class holding info on the path
    class Node:
        def __init__(self, weight, visited, sword):
            self.visited = visited[:]
            self.weight = weight
            self.sword = sword

    # Location of sword for comparison
    sword_location = (-1, -1)
    if 'sword' in data:
        sword_location = data['sword']

    # Our entrance
    node = Node(0, [data['entrance']], False)

    # Priority que
    unexplored = []
    # Add the first node onto the que
    heappush(unexplored, (0, id(node), node))

    # There is nothing to collect
    if len(locations) == 0:
        locations.append(data['exit'])

    while unexplored:

        # Our current position
        node = heappop(unexplored)[2]

        # Check for the sword
        if node.visited[-1] == sword_location:
            node.sword = True

        # We made it to the end, return the distance
        if node.visited[-1] == data['exit']:
            return node.weight

        # We have collected all treasure, find cost to exit
        if len(node.visited) == len(locations) + 1:
            cost = shortest_path(data, node.visited[-1], data['exit'],
                                                                node.sword)
            if cost:
                node.weight += cost
                node.visited += [data['exit']]
                heappush(unexplored, (cost, id(node), node))
        else:
            # There is still treasure to collect
            for point in locations:
                if point not in node.visited:
                    cost = shortest_path(data, node.visited[-1], point,
                                                                node.sword)
                    if not cost:
                        continue
                    new_node = Node(node.weight + cost,
                                    node.visited + [point], node.sword)
                    heappush(unexplored, (cost, id(new_node), new_node))

    return data['size'] ** 3


def optimal_path(data):
    """optimal_path returns the length of the shortest path that enables Falca
    to collect all of the treasures and exit from the dungeon

    data: a dictionary of features in the cave"""

    # See if there are any treasures to collect
    no_sword = data['treasure'][:] if 'treasure' in data else []
    sword = no_sword[:] + [data['sword']] if 'sword' in data else []

    # Get the shortest distances, with and without the sword
    dist = search(data, no_sword)
    dist_sword = search(data, sword) if 'sword' in data else data['size'] ** 3

    # Get the shortest of the two, return it or None if no path was found
    distance = dist if dist < dist_sword else dist_sword
    return distance if distance < data['size'] ** 3 else None
