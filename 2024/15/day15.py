# %%
import pandas as pd
import numpy as np
import re

def load_data(option):
    if option == 0:
        with open('sample.txt') as f:
            data = f.read().splitlines()
    else:
        with open('input.txt') as f:
            data = f.read().splitlines()

    arr = pd.DataFrame(data).to_numpy()
    div = np.where(arr == [''])[0][0]
    map = np.array([list(row[0]) for row in arr[:div, :]], dtype=object)

    move_list = ''
    for row in arr[div+1:, :]:
        move_list += row[0]

    return map, list(move_list)

arr, moves = load_data(0)
print(arr)
print(moves)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr, moves = load_data(1)

y, x = 0, 0
# Find location of the robot
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == '@':
            y, x = i, j

for move in moves:
    match move:
        case '<':
            loc = x - 1
            # Nearest wall/empty space to the left
            while loc > 0 and (arr[y, loc] != '#' and arr[y, loc] != '.'):
                loc -= 1
            
            # Check if there is any empty space
            if arr[y, loc] == '.':
                # Move everything in-between
                arr[y, loc:x] = arr[y, loc+1:x+1]
                arr[y, x] = '.'
                x -= 1

        case '>':
            loc = x + 1
            # Nearest wall/empty space to the left
            while loc < len(arr[0]) - 1 and (arr[y, loc] != '#' and arr[y, loc] != '.'):
                loc += 1
            
            # Check if there is any empty space
            if arr[y, loc] == '.':
                # Move everything in-between
                arr[y, x+1:loc+1] = arr[y, x:loc]
                arr[y, x] = '.'
                x += 1

        case '^':
            loc = y - 1
            # Nearest wall/empty space upward
            while loc > 0 and (arr[loc, x] != '#' and arr[loc, x] != '.'):
                loc -= 1
            
            # Check if there is any empty space
            if arr[loc, x] == '.':
                # Move everything in-between
                arr[loc:y, x] = arr[loc+1:y+1, x]
                arr[y, x] = '.'
                y -= 1

        case 'v':
            loc = y + 1
            # Nearest wall/empty space downward
            while loc < len(arr) - 1 and (arr[loc, x] != '#' and arr[loc, x] != '.'):
                loc += 1
            
            # Check if there is any empty space
            if arr[loc, x] == '.':
                # Move everything in-between
                arr[y+1:loc+1, x] = arr[y:loc, x]
                arr[y, x] = '.'
                y += 1

# Compute sum of boxes' GPS coordinates
res = 0
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == 'O':
            res += 100*i + j
print(res)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr, moves = load_data(1)

# Create the new map
for i in range(len(arr)):
    for j in range(len(arr[0])):
        match arr[i, j]:
            case '#':
                arr[i][j] = '##'
            case 'O':
                arr[i, j] = '[]'
            case '.':
                arr[i, j] = '..'
            case '@':
                arr[i, j] = '@.'

arr = np.array([list(''.join(row)) for row in arr])

y, x = 0, 0
# Find location of the robot
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == '@':
            y, x = i, j

for move in moves:
    match move:
        case '<':
            loc = x - 1
            # Nearest wall/empty space to the left
            while loc > 0 and (arr[y, loc] != '#' and arr[y, loc] != '.'):
                loc -= 1
            
            # Check if there is any empty space
            if arr[y, loc] == '.':
                # Move everything in-between
                arr[y, loc:x] = arr[y, loc+1:x+1]
                arr[y, x] = '.'
                x -= 1

        case '>':
            loc = x + 1
            # Nearest wall/empty space to the left
            while loc < len(arr[0]) - 1 and (arr[y, loc] != '#' and arr[y, loc] != '.'):
                loc += 1
            
            # Check if there is any empty space
            if arr[y, loc] == '.':
                # Move everything in-between
                arr[y, x+1:loc+1] = arr[y, x:loc]
                arr[y, x] = '.'
                x += 1

        case '^':
            empty = [(y-1, x)]
            # Move robot up if empty space
            if arr[y-1, x] == '.':
                arr[y-1, x] = '@'
                arr[y, x] = '.'
                y -= 1

            # Stop robot if wall, else it's a box, start finding possible spots
            elif arr[y-1, x] != '#':
                things_to_move = []
                spots = []

                if arr[y-1, x] == ']':
                    spots.append((y-2, x))
                    spots.append((y-2, x-1))
                    things_to_move.append((y-1, x))
                    things_to_move.append((y-1, x-1))
                else:
                    spots.append((y-2, x))
                    spots.append((y-2, x+1))
                    things_to_move.append((y-1, x))
                    things_to_move.append((y-1, x+1))
                
                items = [arr[pos[0], pos[1]] for pos in spots]
                while items.count('#') == 0 and items.count('.') < len(items):
                    new_spots = []
                    for i, item in enumerate(items):
                        if item == '.':
                            new_spots.append(spots[i])
                            continue

                        # Found another box, the spot is no longer empty
                        removed_pos = spots[i]
                        if item == ']':
                            new_spots.append((removed_pos[0]-1, removed_pos[1]))
                            new_spots.append((removed_pos[0]-1, removed_pos[1]-1))
                            things_to_move.append((removed_pos[0], removed_pos[1]))
                            things_to_move.append((removed_pos[0], removed_pos[1]-1))
                        else:
                            new_spots.append((removed_pos[0]-1, removed_pos[1]))
                            new_spots.append((removed_pos[0]-1, removed_pos[1]+1))
                            things_to_move.append((removed_pos[0], removed_pos[1]))
                            things_to_move.append((removed_pos[0], removed_pos[1]+1))
                    
                    spots = list(set(new_spots))
                    items = [arr[pos[0], pos[1]] for pos in spots]

                # Sort based on row
                things_to_move = list(set(things_to_move))
                things_to_move.sort(key=lambda x: x[0])

                # If all spots are empty, move
                if items.count('.') == len(items):
                    for pos in things_to_move:
                        arr[pos[0]-1, pos[1]] = arr[pos[0], pos[1]]
                        arr[pos[0], pos[1]] = '.'
                    # Update robot location
                    arr[y-1, x] = '@'
                    arr[y, x] = '.'
                    y -= 1

        case 'v':
            empty = [(y+1, x)]
            # Move robot down if empty space
            if arr[y+1, x] == '.':
                arr[y+1, x] = '@'
                arr[y, x] = '.'
                y += 1

            # Stop robot if wall, else it's a box, start finding possible spots
            elif arr[y+1, x] != '#':
                things_to_move = []
                spots = []

                if arr[y+1, x] == ']':
                    spots.append((y+2, x))
                    spots.append((y+2, x-1))
                    things_to_move.append((y+1, x))
                    things_to_move.append((y+1, x-1))
                else:
                    spots.append((y+2, x))
                    spots.append((y+2, x+1))
                    things_to_move.append((y+1, x))
                    things_to_move.append((y+1, x+1))
                
                items = [arr[pos[0], pos[1]] for pos in spots]
                while items.count('#') == 0 and items.count('.') < len(items):
                    new_spots = []
                    for i, item in enumerate(items):
                        if item == '.':
                            new_spots.append(spots[i])
                            continue

                        # Found another box, the spot is no longer empty
                        removed_pos = spots[i]
                        if item == ']':
                            new_spots.append((removed_pos[0]+1, removed_pos[1]))
                            new_spots.append((removed_pos[0]+1, removed_pos[1]-1))
                            things_to_move.append((removed_pos[0], removed_pos[1]))
                            things_to_move.append((removed_pos[0], removed_pos[1]-1))
                        else:
                            new_spots.append((removed_pos[0]+1, removed_pos[1]))
                            new_spots.append((removed_pos[0]+1, removed_pos[1]+1))
                            things_to_move.append((removed_pos[0], removed_pos[1]))
                            things_to_move.append((removed_pos[0], removed_pos[1]+1))
                    
                    spots = list(set(new_spots))
                    items = [arr[pos[0], pos[1]] for pos in spots]

                # Sort based on row
                things_to_move = list(set(things_to_move))
                things_to_move.sort(key=lambda x: x[0], reverse=True)

                # If all spots are empty, move
                if items.count('.') == len(items):
                    for pos in things_to_move:
                        arr[pos[0]+1, pos[1]] = arr[pos[0], pos[1]]
                        arr[pos[0], pos[1]] = '.'
                    # Update robot location
                    arr[y+1, x] = '@'
                    arr[y, x] = '.'
                    y += 1

# Compute sum of boxes' GPS coordinates
res = 0
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == '[':
            res += 100*i + j
print(res)

# %%



