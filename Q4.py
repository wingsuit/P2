from reference import build_cave, shortest_path
from heapq import heappush, heappop


def search(data, locations):
    """search takes a cave dictionary 'data' and a list of the locations of the
    sword and treasure 'locations' and returns the shortest path between the
    entry and exit after visiting all of the locations"""

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

        if len(node.visited) == len(locations) + 1:
            cost = shortest_path(data, node.visited[-1], data['exit'], node.sword)
            if cost:
                node.weight += cost
                node.visited += [data['exit']]
                heappush(unexplored, (cost, id(node), node))
        for point in locations:
            # If the spot hasn't yet been visited on this path
            if point not in node.visited:
                # Find the weight to get to this point
                cost = shortest_path(data, node.visited[-1], point, node.sword)
                if not cost:
                    continue
                # Store the new weight
                new_node = Node(node.weight + cost,
                                node.visited + [point], node.sword)
                heappush(unexplored, (cost, id(new_node), new_node))

    return data['size'] ** 3


def optimal_path(data):
    """optimal_path takes a single argument data, a dictionary of features in
    the cave and returns the length of the shortest path that enables Falca
    to collect all of the treasures and exit from the dungeon."""

    # See if there are any treasures to collect
    treasure = data['treasure'][:] if 'treasure' in data else []
    treasure_sword = treasure[:] + [data['sword']] if 'sword' in data else []

    # If there is no sword or treasure, go straight to exit.
    # if len(treasure) == 0 and len(treasure_sword) == 0:
    #     return shortest_path(data, data['entrance'], data['exit'], False)

    # Get the shortest distance, once with the sword and once without
    distance = search(data, treasure)
    distance_sword = data['size'] ** 3
    if 'sword' in data:
        distance_sword = search(data, treasure_sword)

    # Get the shortest of the two
    distance = distance if distance < distance_sword else distance_sword

    return distance if distance < data['size'] ** 3 else None