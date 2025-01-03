# %%
import pandas as pd
import numpy as np

def load_data(option):
    if option == 0:
        with open('sample.txt') as f:
            data = f.read().splitlines()
    else:
        with open('input.txt') as f:
            data = f.read().splitlines()

    arr = pd.DataFrame(data).to_numpy()
    arr = np.array([list(row[0]) for row in arr], dtype=object)

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

arr = load_data(1)

num_keypad = np.array([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['-', '0', 'A']])
dir_keypad = np.array([['-', '^', 'A'], ['<', 'v', '>']])

# Given start/end position in the target map, return a list of move that
# the player should make to direct the robot to reach the end
# This also includes a "tap" action A at the end of the move list
def find_moves(robot_pos, robot_map, end):
    # Find the shortest path to end on the robot map
    # Perform Dijkstra's
    # The cost is based on how far the player has to move on the directional keypad
    ys, xs = robot_pos
    ye, xe = end

    # Player always start at 'A'
    shortest_path_len = abs(ye - ys) + abs(xe - xs)
    q = [(ys, xs, 0, (0, 2), [])] # y, x, cost, player_pos, path so far
    best_cost = 999999
    best_path = None # (best_path, cost)

    while q:
        y, x, prev_cost, prev_player_pos, cur_path = q.pop()
        new_path = []

        # If the path is longer than the shortest possible path, skip
        if len(cur_path) > shortest_path_len:
            continue

        # If we reach the end, record the path
        if (y, x) == (ye, xe):
            cur_path.append('A') # Add a tap action
            if prev_cost < best_cost:
                best_cost = prev_cost
                best_path = [cur_path]
            elif prev_cost == best_cost:
                best_path.append(cur_path)

        for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_y = y + dy
            new_x = x + dx

            if new_y >= 0 and new_y < len(robot_map) and new_x >= 0 and new_x < len(robot_map[0]) and robot_map[new_y, new_x] != '-':
                # Target position
                target_pos = (1, 0) # '<'
                new_path = ['<']
                if dy == -1:
                    target_pos = (0, 1) # '^'
                    new_path = ['^']
                elif dx == 1:
                    target_pos = (1, 2) # '>'
                    new_path = ['>']
                elif dy == 1:
                    target_pos = (1, 1) # 'v'
                    new_path = ['v']

                # Calculate cost, based on player position
                dist = abs(prev_player_pos[0] - target_pos[0]) + abs(prev_player_pos[1] - target_pos[1])
                cost = prev_cost + dist + 1 # 1 cost to tap the button
                player_pos = target_pos

                # If we reach the end, add the cost of going to 'A'
                if (new_y, new_x) == (ye, xe):
                    target_pos = (0, 2) # 'A'
                    dist = abs(player_pos[0] - target_pos[0]) + abs(player_pos[1] - target_pos[1])
                    cost += dist + 1 # 1 cost to tap the button
                    player_pos = target_pos

                # Add adjacent nodes
                q.append((new_y, new_x, cost, player_pos, cur_path + new_path))

    return best_path


# Main program to find paths
result = 0
for puzzle in arr:
    moves_count = [-1] * len(puzzle)
    for idx, end in enumerate(puzzle):
        # There are 3 stages, one for each robot
        # If a sequence reach stage 3 with an empty target, returns the shortest count
        # Targets, current moves list, robot_1_pos, robot_2_pos, robot_3_pos, stage
        # Except the first robot, all other robots always start at 'A' on the directional pad
        robot_1_pos = tuple([pos[0] for pos in np.where(num_keypad == 'A')])
        if idx > 0:
            robot_1_pos = tuple([pos[0] for pos in np.where(num_keypad == puzzle[idx-1])])

        q = [([end], [], robot_1_pos, (0, 2), (0, 2), 1)]
        while q:
            mini_puzzle, moves_list, r1_pos, r2_pos, r3_pos, stage = q.pop()
            
            # Should we move on to next stage? Did we reach the end?
            if len(mini_puzzle) == 0:
                if stage < 3:
                    q.append((moves_list, [], r1_pos, r2_pos, r3_pos, stage+1))
                else:
                    if moves_count[idx] == -1 or len(moves_list) < moves_count[idx]:
                        moves_count[idx] = len(moves_list)
                continue

            end = mini_puzzle[0]

            match stage:
                # Find moves for robot 1
                case 1:
                    end_pos = tuple([pos[0] for pos in np.where(num_keypad == end)])
                    possible_moves = find_moves(r1_pos, num_keypad, end_pos)
                    r1_pos = end_pos

                    for move in possible_moves:
                        q.append((mini_puzzle[1:], moves_list + move, r1_pos, r2_pos, r3_pos, stage))

                # Find moves for robot 2
                case 2:
                    end_pos = tuple([pos[0] for pos in np.where(dir_keypad == end)])
                    possible_moves = find_moves(r2_pos, dir_keypad, end_pos)
                    r2_pos = end_pos

                    for move in possible_moves:
                        q.append((mini_puzzle[1:], moves_list + move, r1_pos, r2_pos, r3_pos, stage))

                # Find moves for robot 3
                case 3:
                    end_pos = tuple([pos[0] for pos in np.where(dir_keypad == end)])
                    possible_moves = find_moves(r3_pos, dir_keypad, end_pos)
                    r3_pos = end_pos

                    for move in possible_moves:
                        q.append((mini_puzzle[1:], moves_list + move, r1_pos, r2_pos, r3_pos, stage))

    # Once the final sequence is found, calculate the complexity
    print(int(re.findall(r'\d+', ''.join(puzzle))[0]))
    print(sum(moves_count))
    result += sum(moves_count) * int(re.findall(r'\d+', ''.join(puzzle))[0])

print(result)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

arr = load_data(1)

num_keypad = np.array([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['-', '0', 'A']])
dir_keypad = np.array([['-', '^', 'A'], ['<', 'v', '>']])

# Given start/end position in the target map, return a list of move that
# the player should make to direct the robot to reach the end
# This also includes a "tap" action A at the end of the move list
def find_moves(robot_pos, robot_map, end):
    # Find the shortest path to end on the robot map
    # Perform Dijkstra's
    # The cost is based on how far the player has to move on the directional keypad
    ys, xs = robot_pos
    ye, xe = end

    # Player always start at 'A'
    shortest_path_len = abs(ye - ys) + abs(xe - xs)
    q = [(ys, xs, 0, (0, 2), [])] # y, x, cost, player_pos, path so far
    best_cost = 999999
    best_path = None # (best_path, cost)

    while q:
        y, x, prev_cost, prev_player_pos, cur_path = q.pop()
        new_path = []

        # If the path is longer than the shortest possible path, skip
        if len(cur_path) > shortest_path_len:
            continue

        # If we reach the end, record the path
        if (y, x) == (ye, xe):
            cur_path.append('A') # Add a tap action
            if prev_cost < best_cost:
                best_cost = prev_cost
                best_path = [cur_path]
            elif prev_cost == best_cost:
                best_path.append(cur_path)

        for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_y = y + dy
            new_x = x + dx

            if new_y >= 0 and new_y < len(robot_map) and new_x >= 0 and new_x < len(robot_map[0]) and robot_map[new_y, new_x] != '-':
                # Target position
                target_pos = (1, 0) # '<'
                new_path = ['<']
                if dy == -1:
                    target_pos = (0, 1) # '^'
                    new_path = ['^']
                elif dx == 1:
                    target_pos = (1, 2) # '>'
                    new_path = ['>']
                elif dy == 1:
                    target_pos = (1, 1) # 'v'
                    new_path = ['v']

                # Calculate cost, based on player position
                dist = abs(prev_player_pos[0] - target_pos[0]) + abs(prev_player_pos[1] - target_pos[1])
                cost = prev_cost + dist + 1 # 1 cost to tap the button
                player_pos = target_pos

                # If we reach the end, add the cost of going to 'A'
                if (new_y, new_x) == (ye, xe):
                    target_pos = (0, 2) # 'A'
                    dist = abs(player_pos[0] - target_pos[0]) + abs(player_pos[1] - target_pos[1])
                    cost += dist + 1 # 1 cost to tap the button
                    player_pos = target_pos

                # Add adjacent nodes
                q.append((new_y, new_x, cost, player_pos, cur_path + new_path))

    return best_path


# Given start/end pos and depth info, return the cost from start to end at depth
# The first iteration always start with the num_keypad (the puzzle itself is at depth 0)
memo = {}
def calculate_cost(start, end, depth, is_numpad=True):
    if depth == 1:
        if is_numpad:
            return min([len(move) for move in find_moves(start, num_keypad, end)]) # Only run once, if depth = 1
        else:
            return min([len(move) for move in find_moves(start, dir_keypad, end)])

    if (start, end, depth) in memo:
        return memo[(start, end, depth)]
    
    possible_moves = []
    if is_numpad:
        possible_moves = find_moves(start, num_keypad, end) # Only run once, at start
    else:
        possible_moves = find_moves(start, dir_keypad, end)

    best_cost = np.inf
    for move in possible_moves:
        cost = 0
        for i in range(len(move)):
            s, e = '', ''

            if i == 0:
                s, e = tuple([pos[0] for pos in np.where(dir_keypad == 'A')]), tuple([pos[0] for pos in np.where(dir_keypad == move[i])])
            else:
                s, e = tuple([pos[0] for pos in np.where(dir_keypad == move[i-1])]), tuple([pos[0] for pos in np.where(dir_keypad == move[i])])
            cost += calculate_cost(s, e, depth-1, False)

        best_cost = min(cost, best_cost)
    
    # Update memo
    memo[(start, end, depth)] = best_cost
    return best_cost

result = 0
depth = 26
for puzzle in arr:
    total_cost = 0
    for i in range(len(puzzle)):
        s, e = '', ''
        if i == 0:
            s, e = tuple([pos[0] for pos in np.where(num_keypad == 'A')]), tuple([pos[0] for pos in np.where(num_keypad == puzzle[i])])
        else:
            s, e = tuple([pos[0] for pos in np.where(num_keypad == puzzle[i-1])]), tuple([pos[0] for pos in np.where(num_keypad == puzzle[i])])

        total_cost += calculate_cost(s, e, depth)

    # Once the cost is found, calculate the complexity
    print(int(re.findall(r'\d+', ''.join(puzzle))[0]))
    print(total_cost)
    result += total_cost * int(re.findall(r'\d+', ''.join(puzzle))[0])

print(result)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)


