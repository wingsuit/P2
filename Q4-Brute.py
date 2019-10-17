from reference import build_cave, shortest_path
from collections import defaultdict
from heapq import heappush, heappop
import itertools

def get_all_paths(data):
    '''get_all_paths returns a list of every permutation of journeys through
    the cave'''
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
        
    # Create dictionary of weights between each node, with and without sword
    weights_dict = defaultdict(tuple)
    weights_dict_sword = defaultdict(tuple)
    
    if map_sword:
        for i in range(len(map_sword) - 1):
            for j in range(1, len(map_sword)):
                # Without sword flag off
                dista = shortest_path(data, map_sword[i], 
                                             map_sword[j], False)
                weights_dict[(map_sword[i], map_sword[j])] = dista
                weights_dict[(map_sword[j], map_sword[i])] = dista
                             
                # With sword flag on
                dista = shortest_path(data, map_sword[i], 
                                             map_sword[j], True)
                weights_dict_sword[(map_sword[i], map_sword[j])] = dista
                weights_dict_sword[(map_sword[j], map_sword[i])] = dista
                
    else:
        for i in range(len(map_without) - 1):
            for j in range(1, len(map_without)):
                dista = shortest_path(data, map_without[i], 
                                             map_without[j], False)
                weights_dict[(map_without[i], map_without[j])] = dista
                weights_dict[(map_without[j], map_without[i])] = dista
    
    # Create all possible permutations of routes through cave
    permutations = list(itertools.permutations(map_without))
    permutations += list(itertools.permutations(map_sword))

    # Change to list of lists removing empties
    permutations = [list(tup) for tup in permutations if tup]

    # Add in the entry and exit
    for i in range(len(permutations)):
        permutations[i].insert(0, data['entrance'])
        permutations[i].append(data['exit'])
        
    return (permutations, weights_dict_sword, weights_dict)

def get_distance(path, data):
    sword = (-1, -1)
    if 'sword' in data:
        sword = data['sword']
        
    total = 0
    # for each step in the path through the cave
    has_sword = False
    for i in range(len(path) - 1):
        # if current spot is a sword
        if path[i] == sword:
            has_sword = True
        result = shortest_path(data, path[i], path[i + 1], has_sword)
        if result:
            total += result
        else:
            return None
    return total
        
def optimal_path(data):
    
    # A list holding every possible path through the cave
    paths, weights_dict_sword, weights_dict = get_all_paths(data)
    
    # a list of the distances found testing the paths
    path_distances = []

    # Get all the distances
    for path in paths:
        path_distances.append(get_distance(path, data))

    path_distances = [x for x in path_distances if x is not None]
    return sorted(path_distances)[0] if len(path_distances) > 0 else None
