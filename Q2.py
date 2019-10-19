from reference import build_cave


def check_path(data, path):
    """check_path takes two arguments - data, a dictionary of features in the
    cave and path, a list of moves constituting a path through the dungeon.
    It returns True if the path is valid, or False if it is not valid."""
    cave = build_cave(data)

    # Replace all letters with values in path
    moves_dic = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    path = [moves_dic[m] for m in path]

    # Our current position
    x, y = data['entrance']

    # Dragon and adjacent positions
    dragon_pos = []
    if 'dragon' in data:
        d_x, d_y = data['dragon']
        dragon_pos = [((d_x + i, d_y + j)) for i in range(-1, 2)
                      for j in range(-1, 2)]

    # Treasure collected
    treasure = 0

    # Our main loop, go through every location and check for validity.
    for move in path:
        # Perform the move
        x += move[0]
        y += move[1]

        # Check for index validity
        if not -1 < x < data['size'] or not -1 < y < data['size']:
            return False

        # Check for wall or dragon
        if cave[x][y] == '#' or (x, y) in dragon_pos:
            return False

        # Pickup sword and treasure
        if cave[x][y] == 't':
            dragon_pos = []
        elif cave[x][y] == '$':
            treasure += 1
            cave[x][y] = '.'

    # Are we at the exit with all treasure
    if (x, y) == data['exit']:
        if 'treasure' in data and treasure != len(data['treasure']):
            return False
        return True
    return False