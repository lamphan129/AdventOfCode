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
    arr = np.array([list(row[0]) for row in arr], dtype=object)

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(0)

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
q = [(ys, xs, 0, 2)] # y, x, prev_cost, prev_direction: 0 = West, 1 = North, 2 = East, 3 = South
cost_dir = {}

while q:
    y, x, prev_cost, prev_direction = q.pop()
    for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        new_y = y + dy
        new_x = x + dx

        if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) and arr[new_y, new_x] == '.':
            # Calculate cost (didn't move at first)
            cost = prev_cost + 1
            if prev_cost == 0:
                cost = prev_cost

            # If reach the end, update cost, then continue
            if (y, x) == (ye, xe):
                if (ye, xe) in cost_dir:
                    if cost < cost_dir[(ye, xe)]: # Is it better?
                        cost_dir[(ye, xe)] = cost
                else:
                    cost_dir[(ye, xe)] = cost
                continue
            
            # Else, find target direction, and calculate rotation cost
            target_direction = 0
            if dy == -1:
                target_direction = 1
            elif dx == 1:
                target_direction = 2
            elif dy == 1:
                target_direction = 3
            direction = target_direction

            # Account for 270 degrees turn
            dist = abs(prev_direction - target_direction)
            if dist == 3:
                dist = 1
            
            cost += dist * 1000
            
            # Did we check this node?
            if (y, x) in cost_dir:
                if cost < cost_dir[(y, x)]: # Is it better?
                    cost_dir[(y, x)] = cost
            else:
                cost_dir[(y, x)] = cost
                q.append((new_y, new_x, cost, direction))

            # Should we add adjacent nodes if it's potentially better?
            if (new_y, new_x) not in cost_dir or cost+1 < cost_dir[(new_y, new_x)]:
                q.append((new_y, new_x, cost, direction))

cost_map = np.zeros_like(arr, dtype=int)

for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i, j] == '#':
            cost_map[i, j] = -1
        else:
            if (i, j) in cost_dir:
                cost_map[i, j] = cost_dir[(i, j)]
            else:
                cost_map[i, j] = 0

df = pd.DataFrame(cost_map)
df.to_excel(excel_writer = "result.xlsx")

# Find the cost at end
best_cost = cost_dir[(ye, xe)]
print(best_cost)

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

# Check forward and backward, combine the result
O_map = np.zeros_like(arr, dtype=int)
for ys, xs, ye, xe in [(ys, xs, ye, xe), (ye, xe, ys, xs)]:
    # Find the shortest path (with cost)
    q = [(ys, xs, 0, 2)] # y, x, cost, direction: 0 = West, 1 = North, 2 = East, 3 = South
    cost_dir = {} # Cost to reach node (y, x)

    while q:
        y, x, prev_cost, prev_direction = q.pop()
        for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_y = y + dy
            new_x = x + dx

            if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) and arr[new_y, new_x] == '.':
                # Calculate cost (didn't move at first)
                cost = prev_cost + 1
                if (y, x) == (ys, xs):
                    cost = prev_cost

                # If reach the end, update cost, then continue
                if (y, x) == (ye, xe):
                    if (ye, xe) in cost_dir:
                        if cost < cost_dir[(ye, xe)]: # Is it better?
                            cost_dir[(ye, xe)] = cost
                    else:
                        cost_dir[(ye, xe)] = cost
                    continue
                
                # Else, find target direction, and calculate rotation cost
                target_direction = 0
                if dy == -1:
                    target_direction = 1
                elif dx == 1:
                    target_direction = 2
                elif dy == 1:
                    target_direction = 3
                direction = target_direction

                # Account for 270 degrees turn
                dist = abs(prev_direction - target_direction)
                if dist == 3:
                    dist = 1
                
                cost += dist * 1000
                
                # Did we check this node?
                if (y, x) in cost_dir:
                    if cost < cost_dir[(y, x)]: # Is it better?
                        cost_dir[(y, x)] = cost
                else:
                    cost_dir[(y, x)] = cost
                    q.append((new_y, new_x, cost, direction))

                # Should we add adjacent nodes if it's potentially better?
                if (new_y, new_x) not in cost_dir or cost+1 < cost_dir[(new_y, new_x)]:
                    q.append((new_y, new_x, cost, direction))

    cost_map = np.zeros_like(arr, dtype=int)

    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i, j] == '#':
                cost_map[i, j] = 9999999
            else:
                if (i, j) in cost_dir:
                    cost_map[i, j] = cost_dir[(i, j)]
                else:
                    cost_map[i, j] = 9999999

    # Extract spots
    q = [(ye, xe)]
    while q:
        y, x = q.pop()
        O_map[y, x] = 1

        if (y, x) != (ys, xs):
            # Check adjacent nodes
            for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                new_y = y + dy
                new_x = x + dx

                if new_y > 0 and new_y < len(arr) and new_x > 0 and new_x < len(arr[0]) \
                and cost_map[(new_y, new_x)] < cost_map[(y, x)]:
                    q.append((new_y, new_x))

print(np.sum(O_map))


