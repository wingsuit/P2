from reference import build_cave


def check_path(data, path):
    """check_path checks if a given path is a valid route through the
    cave according to the rules of the game and returns a boolean result

    data:  a dictionary of features in the cave
    path:  a list of moves constituting a path through the cave"""

    cave = build_cave(data)

    # Replace all letters with values in path
    moves_dic = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    path = [moves_dic[m] for m in path]

    # Our current position
    y, x = data['entrance']

    # Dragon and adjacent positions
    dragon_pos = []
    if 'dragon' in data:
        d_y, d_x = data['dragon']
        dragon_pos = [(d_y + i, d_x + j) for i in range(-1, 2)
                                          for j in range(-1, 2)]

    # Treasure collected
    treasure = 0

    # Our main loop, go through every location and check for validity.
    for move in path:
        # Perform the move
        y += move[0]
        x += move[1]

        # Check for index validity
        if not -1 < y < data['size'] or not -1 < x < data['size']:
            return False

        # Check for wall or dragon
        if cave[y][x] == '#' or (y, x) in dragon_pos:
            return False

        # Pickup sword and treasure
        if cave[y][x] == 't':
            dragon_pos = []
        elif cave[y][x] == '$':
            treasure += 1
            cave[y][x] = '.'

    # Are we at the exit with all treasure
    success = [(y, x) == data['exit'],
               not ('treasure' in data and treasure != len(data['treasure']))]
    return False not in success
