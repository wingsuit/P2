from reference import build_cave, shortest_path
import random


def get_cost(point, unexplored):
    """get_cost finds the current cost of a node in the pque"""
    for node in unexplored:
        if point == node[2].location:
            return node[2].weight


def replace_cost(node, old):
    """replace_cost replaces the child's current cost with the given"""
    unexplored = [(node.weight, id(node), node)]
    unexplored += [entry for entry in old if entry[2].location != node.location]
    return unexplored


def cost_locations(data, node, locations):
    cost_locs = []
    for loc in locations:
        if loc not in node.visited + [node.location]:
            cost = shortest_path(data, node.location, loc, node.sword)
            if cost:
                cost_locs.append((cost, loc))
    return sorted(cost_locs)

def search(data, with_sword):

    # An object holding info on the path
    class Node:
        def __init__(self, coords, weight, visited, treasures, sword):
            self.location = coords
            self.visited = visited[:]
            self.weight = weight
            self.treasures = treasures
            self.sword = sword

        def __eq__(self, other):
            return self.location == other[2].location

    # Treasure locations
    treasure_locations = data['treasure'][:] if 'treasure' in data else []

    # Get the coordinates of the treasures and sword
    locations = treasure_locations[:] + [data['exit']]
    locations += [data['sword']] if with_sword and 'sword' in data else []

    # Location of the sword
    sword_location = data['sword'] if 'sword' in data else (-1, -1)

    # Entrance node
    node = Node(data['entrance'], 0, [], 0, False)

    # Add the first node onto the que
    unexplored = [(0, id(node), node)]

    while unexplored:

        # for item in unexplored:
            # print(f"Cost: {item[0]}, at {node.visited + [node.location]}")
        # print("Done")

        # Our current position
        unexplored.sort(reverse=True)
        node = unexplored.pop(-1)[2]

        # Check for the sword
        if node.location == sword_location:
            node.sword = True

        # We made it to the end, return the distance
        if node.treasures == len(treasure_locations):
            if node.location == data['exit']:
                return node.weight
            # locations += [data['exit']]

        # Find the next location sorted by descending distance
        for cost, next_location in cost_locations(data, node, locations):
            # Find the next potential move
            if next_location == data['exit'] and node.treasures < len(treasure_locations):
                continue
            treasure = 1 if next_location in treasure_locations else 0
            new_node = Node(next_location, node.weight + cost, node.visited + [node.location], node.treasures + treasure, node.sword)
            # If we haven't been there before, add it to the que
            if new_node not in unexplored:
                # unexplored.append((new_node.weight, id(new_node), new_node))
                unexplored.append((new_node.weight, id(new_node), new_node))
            # If we have seen it before at a higher cost, update it
            elif new_node.weight < get_cost(next_location, unexplored):
                unexplored = replace_cost(new_node, unexplored)
    return 1000


def optimal_path(data):
    """optimal_path returns the length of the shortest path that enables Falca
    to collect all of the treasures and exit from the dungeon

    data: a dictionary of features in the cave"""

    a = search(data, True)
    b = search(data, False)

    if a >= 1000 and b >= 1000:
        return None

    return a if a < b else b