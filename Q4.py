from reference import build_cave, shortest_path
from collections import defaultdict
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
    print(f"unexplored is {unexplored}")
    for entry in unexplored:
        if child == entry[2]:
            return entry[0]
    print(f"now unexplored is {unexplored}")

def replace_cost(child, child_weight, old_unexplored):
    '''replace_weight replaces the child's current weight with the given
    weight'''
    # TODO, verify this function words
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
    # Initialise to an unrealistic distance for comparison
    unrealistic_distance = 4 * data['size']**2
    weight = unrealistic_distance
    
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
        weight = path1.weight
    if path2 and path2.weight < weight:
        weight = path2.weight
    return weight if weight < unrealistic_distance else None

## Test Code ##
import time
def run_test(num, data, expected, explanation):
    start = time.time()
    output = str(optimal_path(data))
    end = time.time()
    success = "PASSED" if output == expected else "FAIL"
    print(f"{num:>3}{'|':>9}{output:>8}{'|':>9}{expected:>9}{'|':>8}{success:>11}{'|':>7}  {(end-start):.7f}{'|':>3}  {explanation}")
   
def test():
    tests = [
        (
            {'size': 4,'entrance': (0, 0),'exit': (2, 1),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "23",
            "Example 1"
        ),(
            {'size': 5,'entrance': (0, 2),'exit': (0, 4),'sword': (0, 0),'dragon': (2, 1),'treasure': [(0, 3), (4, 1)],'walls': [(1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]},
            "14",
            "Example 2"
        ),(
            {'size': 5,'entrance': (0, 2),'exit': (4, 4),'sword': (0, 0),'dragon': (2, 1),'treasure': [(0, 3), (4, 1)],'walls': [(4,3),(3,4),(1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]},
            'None',
            "Exit unreachable"
        ),(
            {'size': 5,'entrance': (0, 2),'exit': (0, 4),'dragon': (2, 1),'treasure': [(0, 3), (4, 1)],'walls': [(1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]},
            '16',
            "No sword"
        ),(
            {'size': 6, 'entrance': (0, 1), 'exit': (0,5), 'dragon': (0, 3), 'sword': (0, 0)},
            '6',
            "No treasure or walls. Grab sword kill dragon exit"
        ),(
            {'size': 6, 'entrance': (0, 1), 'exit': (0,5), 'dragon': (0, 3)},
            '8',
            "No treasure, walls or sword. Walk around dragon"
        ),(
            {'size': 6, 'entrance': (5, 5), 'exit': (0,1)},
            '9',
            "Just entrance and exit, far"
        ),(
            {'size': 6, 'entrance': (0, 0), 'exit': (0,1)},
            '1',
            "Just entrance and exit, close"
        ),(
            {'size': 6, 'entrance': (0, 0), 'exit': (2, 2), 'walls': [(0, 1), (1, 1), (1, 0)]},
            'None',
            "Just entrance and exit, but exit unreachable"
        ),(
            {'size': 5,'entrance': (0, 2),'exit': (0, 4),'sword': (0, 0),'dragon': (2, 1),'treasure': [(0, 3), (3, 4)],'walls': [(1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]},
            '8',
            "Quicker without the sword"
        ),(
            {'size': 7,'entrance': (0, 0),'exit': (6, 6),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "18",
            "Big"
        ),(
            {'size': 8,'entrance': (0, 0),'exit': (7, 7),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "20",
            "Bigger"
        ),(
            {'size': 9,'entrance': (0, 0),'exit': (8, 8),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "22",
            "Biggerrr"
        ),(
            {'size': 10,'entrance': (0, 0),'exit': (9, 9),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "24",
            "Biggest"
        ),(
            {'size': 11,'entrance': (0, 0),'exit': (10, 10),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            "26",
            "Biggest"
        )
    ]
    
    print(" Test #    |    Received    |    Expected    |    PASS/FAIL    |    Time     |    Test Type")
    print("-----------------------------------------------------------------------------------------------------")
    num = 1
    for data, expected, explanation in tests:
        run_test(num, data, expected, explanation)
        num += 1
        
test()
## Test Code ##
