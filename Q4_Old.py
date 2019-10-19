from reference import build_cave, shortest_path
from heapq import heappush, heappop

def get_locations(data):
    '''get_locations takes a single argument data and returns two lists
    of the locations to visit in the map, one with the sword (if it exists)
    and one without'''
    map_sword = []
    map_without = []

    if 'treasure' in data:
        for treasure_xy in data['treasure']:
            map_sword.append(treasure_xy) 
            map_without.append(treasure_xy)
    
    if 'sword' in data:
        map_sword.append(data['sword'])
    else:
        map_sword = []
        
    return (map_without, map_sword)


def get_cost(child, unexplored):
    '''get_cost finds the current cost of a node in the pque'''
    print("GET COST")
    for entry in unexplored:
        if child == entry[2]:
            return entry[0]


def replace_cost(child, child_weight, old_unexplored):
    '''replace_weight replaces the child's current weight with the given'''
    print("REPLACE COST")
    #weight
    unexplored = []
    heappush(unexplored, (child_weight, id(child), child))
    for entry in old_unexplored:
        if entry[2] != child:
            heappush(unexplored, entry)
    return unexplored 


def search(data, locations):
    '''search takes a data dictionary and a list of locations to visit and 
    returns a Node object containing the route and cost of the shortest path 
    to the exit after visiting every treasure location.'''
    
    # A node holding a list of each place before it, and the current weight
    class Node:
        '''a node holding all the nodes before it'''
        def __init__(self):
            self.visited = []
        weight = 0    
   
    # Location of sword for comparison
    sword_location = (-1, -1)
    if 'sword' in data:
        sword_location = data['sword']
        
    sword = False
    node = Node()
    node.visited.append(data['entrance'])
    # Priority que
    unexplored = []
    # priorityque tuple consists of (cost, id for equal cost comparison, node)
    heappush(unexplored, (0, id(node), node))
    
    while unexplored:

        # Our current position
        node = heappop(unexplored)[2]

        # Check for the sword
        if node.visited[-1] == sword_location:
            sword = True

        # We made it to the end
        if node.visited[-1] == data['exit']:
            return node
        
        for point in locations:
            # If the spot hasn't yet been visited on this specific path
            if point not in node.visited:
                # Create the next Node
                new_node = Node()
                # Give it a copy of the path that came before it
                new_node.visited += node.visited
                # Give it the weight that it took to get here.
                new_node.weight += node.weight
                # Append the current location along the path
                new_node.visited.append(point)
                # Find the weight to get to this point
                cost = shortest_path(data, node.visited[-1], point, sword)
                # Replace None returns with very high cost
                if not cost:
                    cost = 4 * data['size']**2
                new_node.weight += cost 
                if new_node not in unexplored:
                    heappush(unexplored, (cost, id(new_node), new_node))
                elif new_node in unexplored and cost < get_cost(new_node, 
                                                                unexplored):
                    unexplored = replace_cost(new_node, cost, unexplored)
            # Add the exit location into the list of locations
            elif len(node.visited) == len(locations) + 1:
                locations.append(data['exit'])
    return None

def optimal_path(data):
    '''optimal_path takes a single argument data, a dictionary of features in 
    the cave and returns the length of the shortest path that enables Falca 
    to collect all of the treasures and exit from the dungeon.'''
    # Check for valid cave
    if not build_cave(data):
        return None
    
    # Initialise to an unrealistic distance for comparison
    unrealistic_distance = 4 * data['size']**2
    distance = unrealistic_distance
    
    # The coordinates to visit, with and without the sword
    locations, locations_sword = get_locations(data)
    
    # If there is no sword or treasure, go straight to exit.
    if len(locations) == 0 and len(locations_sword) == 0:
        return shortest_path(data, data['entrance'], data['exit'], False)
    
    # Get the shortest distance, once with the sword and once without
    path1 = search(data, locations)
    path2 = search(data, locations_sword)
    
    # See if paths were found, if they were, update weight
    if path1:
        distance = path1.weight
    if path2 and path2.weight < distance:
        distance = path2.weight
    return distance if distance < unrealistic_distance else None
