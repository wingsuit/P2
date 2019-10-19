def valid_index(size, pos):
    """valid_index takes the size of the cave and checks whether or not the
    given position is inside the dimensions of the cave"""
    if -1 < pos[0] < size and -1 < pos[1] < size:
        return True
    else:
        return False


def build_cave(data):
    """build_cave builds a two-dimensional representation of a cave from a data
    dictionary"""

    # List to check for multiple conflicting coordinates
    coordinates_list = []

    # Check for a size
    if 'size' not in data:
        return None

    # Our cave to return
    cave = [['.'] * data['size'] for i in range(data['size'])]

    # Check for an entrance
    if 'entrance' not in data or not isinstance(data['entrance'], tuple):
        return None
    else:
        if not valid_index(data['size'], data['entrance']):
            return None
        coordinates_list.append(data['entrance'])
        cave[data['entrance'][0]][data['entrance'][1]] = '@'

    # Check for an exit
    if 'exit' not in data or not isinstance(data['exit'], tuple):
        return None
    else:
        if not valid_index(data['size'], data['exit']):
            return None
        coordinates_list.append(data['exit'])
        cave[data['exit'][0]][data['exit'][1]] = 'X'

    # Check for a dragon, check location of dragon
    if 'dragon' in data:
        if not isinstance(data['dragon'], tuple):
            return None
        elif not valid_index(data['size'], data['dragon']):
            return None
        # If draon is at the entrance
        elif (data['entrance'][0] - 1 <= data['dragon'][0] <=
              data['entrance'][0] + 1 and data['entrance'][1] - 1 <=
              data['dragon'][1] <= data['entrance'][1] + 1):
            return None
        else:
            coordinates_list.append(data['dragon'])
            cave[data['dragon'][0]][data['dragon'][1]] = 'W'

    # Check for one or no sword
    if 'sword' in data:
        if not isinstance(data['sword'], tuple):
            return None
        if not valid_index(data['size'], data['sword']):
            return None
        else:
            coordinates_list.append(data['sword'])
            cave[data['sword'][0]][data['sword'][1]] = 't'

    # Check for 3 or fewer treasures
    if 'treasure' in data:
        if len(data['treasure']) > 3:
            return None
        else:
            for coord in data['treasure']:
                if not valid_index(data['size'], coord):
                    return None
                coordinates_list.append(coord)
                cave[coord[0]][coord[1]] = '$'

    # Check for walls
    if 'walls' in data:
        for coord in data['walls']:
            if not valid_index(data['size'], coord):
                return None
            coordinates_list.append(coord)
            cave[coord[0]][coord[1]] = '#'

    # Check for conflicting coordinates
    for coordinate in coordinates_list:
        if coordinates_list.count(coordinate) > 1:
            return None

    return cave