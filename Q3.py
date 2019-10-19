# from reference import build_cave
from collections import defaultdict


def shortest_path(data, start, end, has_sword):
    """shortest_path determines the length of the shortest valid path between
    two locations in a cave."""

    # List of all unwalkable positions
    forbidden = []
    if 'walls' in data:
        forbidden += data['walls']
    if 'dragon' in data and not has_sword:
        x, y = data['dragon']
        forbidden += [(x + i, y + j) for i in range(-1, 2)
                      for j in range(-1, 2)]

    position = start
    unexplored = [position]
    explored = set()
    tree = defaultdict(tuple)

    while True:
        if len(unexplored) == 0:
            return None

        position = unexplored.pop(0)

        # The end is nigh, traverse the tree and return distance
        if position == end:
            distance = 0
            current = end
            while current != start:
                current = tree[current]
                distance += 1
            return distance

        explored.add(position)

        # See which directions we can move in
        x, y = position
        moves = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        valid_moves = [(x, y) for x, y in moves if (x, y) not in forbidden and
                       -1 < x < data['size'] and -1 < y < data['size']]

        # Add more moves onto the que and tree
        for move in valid_moves:
            if move not in explored and move not in unexplored:
                tree[move] = position
                unexplored.append(move)