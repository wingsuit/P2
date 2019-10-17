from reference import build_cave
from collections import defaultdict

def valid_moves(pos, cave, has_sword, dragon_pos):
    '''valid_moves takes data about the cave and player and returns a list
    of valid moves they can make according to the rules of the game'''
    x, y = pos
    moves = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    valid_moves = []
    
    for x, y in moves:
        
        # Check for index validity
        if not -1 < x < len(cave) or not -1 < y < len(cave):
            continue

        # Check for wall or dragon
        if cave[x][y] == '#' or (x, y) in dragon_pos:
            continue
      
        valid_moves.append((x, y))
        
    return valid_moves
    
def shortest_path(data, start, end, has_sword):
    '''shortest_path determines the length of the shortest valid path between 
    two locations in a cave.'''
    
    cave = build_cave(data)
    
    # List of any dangerous positions
    dragon_pos = []
    if not has_sword and 'dragon' in data:
        d_x, d_y = data['dragon']
        dragon_pos = [((d_x + i, d_y + j)) for i in range(-1, 2) 
                                             for j in range(-1, 2)]

    pos = start
    unexplored = [pos]
    explored = set()
    tree = defaultdict(tuple)
    
    while True:
        if len(unexplored) == 0:
            return None
        
        pos = unexplored.pop(0)
         
        # The end is nigh, traverse the tree and return distance
        if pos == end:
            distance = 0
            current = end
            while current != start:
                current = tree[current]
                distance += 1
            return distance
            
        explored.add(pos)

        # Add more moves onto the que and tree
        for move in valid_moves(pos, cave, has_sword, dragon_pos):
            if move not in explored and move not in unexplored:
                tree[move] = pos
                unexplored.append(move)

## Test Code ##
import time
def run_test(num, data, ent, ex, sword, expected, explanation):
    start = time.time()
    output = str(shortest_path(data, ent, ex, sword))
    end = time.time()
    success = "PASSED" if output == expected else "FAIL"
    print(f"{num:>3}{'|':>9}{output:>8}{'|':>9}{expected:>9}{'|':>8}{success:>11}{'|':>7}  {(end-start):.7f}{'|':>3}  {explanation}")
   
def test():
    tests = [
        (
            {'size': 4,'entrance': (0, 0),'exit': (2, 1),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            (0, 0),
            (3, 3),
            False,
            '6',
            "Example 1",
        ),
        (
            {'size': 4,'entrance': (0, 0),'exit': (2, 1),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            (0, 0),
            (1, 3),
            False,
            'None',
            "Example 2",
        ),
        (
            {'size': 4,'entrance': (0, 0),'exit': (2, 1),'dragon': (0, 2),'sword': (3, 3),'treasure': [(1, 3)],'walls': [(1, 1), (1, 2), (2, 2), (2, 3)]},
            (0, 0),
            (1, 3),
            True,
            '4',
            "Example 2 but with sword",
        )
    ]
    
    print(" Test #    |    Received    |    Expected    |    PASS/FAIL    |    Time     |    Test Type")
    print("-----------------------------------------------------------------------------------------------------")
    num = 1
    for data, ent, ex, sword, expected, explanation in tests:
        run_test(num, data, ent, ex, sword, expected, explanation)
        num += 1
        
test()
## Test Code ##
