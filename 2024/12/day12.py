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
    arr = [list(row[0]) for row in arr]
    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)

sum = 0
checked = np.zeros((len(arr), len(arr[0]))) # For checking if a tile belong to an area
# Find area
for i in range(len(arr)):
    for j in range(len(arr[0])):
        q = []
        if checked[i][j] == 0:
            q.append((arr[i][j], i, j))
            checked[i][j] = 1
            count = 1
            perimeter = 0

            while q:
                char, x, y = q.pop(0)
                perimeter += 4 # 4 fence around a char by default
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= x + dx < len(arr) and 0 <= y + dy < len(arr[0]) and arr[x + dx][y + dy] == char:
                        perimeter -= 1 # remove fence since a char is part of an area
                        if checked[x + dx][y + dy] == 1:
                            continue

                        q.append((char, x + dx, y + dy))
                        checked[x + dx][y + dy] = 1
                        count += 1

            sum += count * perimeter
print(sum)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)

def add_border_type(arr):
    if len(arr) == 1:
        return arr[0] + 1
    elif len(arr) == 2:
        if 0 in arr and 1 in arr:
            return 5
        elif 0 in arr and 2 in arr:
            return 6
        elif 0 in arr and 3 in arr:
            return 7
        elif 1 in arr and 2 in arr:
            return 8
        elif 1 in arr and 3 in arr:
            return 9
        elif 2 in arr and 3 in arr:
            return 10
    elif len(arr) == 3:
        if 0 in arr and 1 in arr and 2 in arr:
            return 11
        elif 0 in arr and 1 in arr and 3 in arr:
            return 12
        elif 0 in arr and 2 in arr and 3 in arr:
            return 13
        elif 1 in arr and 2 in arr and 3 in arr:
            return 14
    elif len(arr) == 4:
        return 15
    else:
        return 0

total = 0
checked = np.zeros((len(arr), len(arr[0]))) # For checking if a tile belong to an area
# Find area
for i in range(len(arr)):
    for j in range(len(arr[0])):
        q = []
        border_map = np.zeros((len(arr), len(arr[0])))
        side_map = np.zeros((len(arr), len(arr[0])))
        if checked[i][j] == 0:
            q.append((arr[i][j], i, j))
            checked[i][j] = 1
            count = 1

            while q:
                char, x, y = q.pop(0)
                sides = 4
                possible_borders = [0, 1, 2, 3] # 0 = up, 1 = down, 2 = left, 3 = right
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= x + dx < len(arr) and 0 <= y + dy < len(arr[0]) and arr[x + dx][y + dy] == char:
                        sides -= 1

                        # Determine which border can be added to a char
                        if (dx, dy) == (-1, 0):
                            possible_borders.remove(0)
                        
                        if (dx, dy) == (1, 0):
                            possible_borders.remove(1)
                        
                        if (dx, dy) == (0, -1):
                            possible_borders.remove(2)
                        
                        if (dx, dy) == (0, 1):
                            possible_borders.remove(3)

                        if checked[x + dx][y + dy] == 1:
                            continue

                        q.append((char, x + dx, y + dy))
                        checked[x + dx][y + dy] = 1
                        count += 1

                border_map[x][y] = add_border_type(possible_borders)  # Border type
                side_map[x][y] = sides # Number of sides

            # Merge borders horizontally (to the right), and vertically (to the bottom)
            # The idea is only the top left-most corner will keep the count for the entire side
            for x in range(len(border_map)):
                for y in range(len(border_map[0])):
                    border_type = border_map[x][y]

                    if border_type == 0:
                        continue
                    
                    if y + 1 < len(border_map[0]):
                        # Merge top
                        top_borders = [1, 5, 6, 7, 11, 12, 13, 15]
                        if border_type in top_borders and border_map[x][y + 1] in top_borders:
                            side_map[x][y+1] -= 1 # Remove duplicate borders

                        # Merge bottom
                        bottom_borders = [2, 5, 8, 9, 11, 12, 14, 15]
                        if border_type in bottom_borders and border_map[x][y + 1] in bottom_borders:
                            side_map[x][y+1] -= 1 # Remove duplicate borders
                    
                    if x + 1 < len(border_map):
                        # Merge left
                        left_borders = [3, 6, 8, 10, 11, 13, 14, 15]
                        if border_type in left_borders and border_map[x + 1][y] in left_borders:
                            side_map[x+1][y] -= 1 # Remove duplicate borders

                        # Merge right
                        right_borders = [4, 7, 9, 10, 12, 13, 14, 15]
                        if border_type in right_borders and border_map[x + 1][y] in right_borders:
                            side_map[x+1][y] -= 1 # Remove duplicate borders

            total += count * sum(side_map.flatten())

print(total)


