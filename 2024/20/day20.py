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

arr = load_data(1)

# Find start/end
ys, xs, ye, xe = 0, 0, 0, 0
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == 'S':
            ys, xs = i, j
            arr[i, j] = '.'
        if arr[i, j] == 'E':
            ye, xe = i, j
            arr[i, j] = '.'

# Find the shortest path (with cost)
q = [(ys, xs, 0)] # y, x, prev_cost
cost_dir = {}

while q:
    y, x, prev_cost = q.pop()
    for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        new_y = y + dy
        new_x = x + dx

        if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) and arr[new_y, new_x] == '.':
            # Calculate cost
            cost = prev_cost + 1

            # If reach the end, update cost, then continue
            if (y, x) == (ye, xe):
                if (ye, xe) in cost_dir:
                    if cost < cost_dir[(ye, xe)]: # Is it better?
                        cost_dir[(ye, xe)] = cost
                else:
                    cost_dir[(ye, xe)] = cost
                continue
            
            # Did we check this node?
            if (y, x) in cost_dir:
                if cost < cost_dir[(y, x)]: # Is it better?
                    cost_dir[(y, x)] = cost
            else:
                cost_dir[(y, x)] = cost
                q.append((new_y, new_x, cost))

            # Should we add adjacent nodes if it's potentially better?
            if (new_y, new_x) not in cost_dir or cost+1 < cost_dir[(new_y, new_x)]:
                q.append((new_y, new_x, cost))

# For each walkable spot, check for shortcut
result = 0
threshold = 100
for spot in cost_dir.keys():
    y, x = spot
    for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        # If found a cheat that would save enough picoseconds, record it
        # new_y and new_x is the coordinate of the next possible spot, if applicable
        new_y = y+(2*dy)
        new_x = x+(2*dx)
        if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) and \
            arr[y+dy, x+dx] == '#' and arr[new_y, new_x] == '.' and cost_dir[(new_y, new_x)] - cost_dir[(y, x)] - 2 >= threshold:
            result += 1

print(result)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)

# Find start/end
ys, xs, ye, xe = 0, 0, 0, 0
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == 'S':
            ys, xs = i, j
            arr[i, j] = '.'
        if arr[i, j] == 'E':
            ye, xe = i, j
            arr[i, j] = '.'

# Find the shortest path (with cost)
q = [(ys, xs, 0)] # y, x, prev_cost
cost_dir = {}

while q:
    y, x, prev_cost = q.pop()
    for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        new_y = y + dy
        new_x = x + dx

        if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) and arr[new_y, new_x] == '.':
            # Calculate cost
            cost = prev_cost + 1

            # If reach the end, update cost, then continue
            if (y, x) == (ye, xe):
                if (ye, xe) in cost_dir:
                    if cost < cost_dir[(ye, xe)]: # Is it better?
                        cost_dir[(ye, xe)] = cost
                else:
                    cost_dir[(ye, xe)] = cost
                continue
            
            # Did we check this node?
            if (y, x) in cost_dir:
                if cost < cost_dir[(y, x)]: # Is it better?
                    cost_dir[(y, x)] = cost
            else:
                cost_dir[(y, x)] = cost
                q.append((new_y, new_x, cost))

            # Should we add adjacent nodes if it's potentially better?
            if (new_y, new_x) not in cost_dir or cost+1 < cost_dir[(new_y, new_x)]:
                q.append((new_y, new_x, cost))

# For each walkable spot, check for shortcut
result = 0
threshold = 100
all_spots = list(cost_dir.keys()) # This list is already in order from cost 1 to N

for i in range(len(all_spots)):
    # Check every other spots that would save enough picoseconds
    for j in range(i+threshold+2, len(all_spots)):
        # Would it be able to reach the other spot with only 20 picoseconds?
        dist = abs(all_spots[j][0] - all_spots[i][0]) + abs(all_spots[j][1] - all_spots[i][1])

        if dist <= 20:
            # How much picoseconds did it save?
            save = cost_dir[all_spots[j]] - cost_dir[all_spots[i]] - dist
            if save >= threshold:
                result += 1

print(result)


