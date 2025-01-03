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
    print()
    arr = [[int(val) for val in re.findall(r'(\d+)', row[0])] for row in arr]

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import heapq

arr = load_data(1)

size = 70
map = np.zeros((size+1, size+1))

# 0 = walkable, -1 = corrupted
for i in range(1024):
    x, y = arr[i]
    map[y][x] = -1

# Perform Dijkstra's (although BFS would work just fine)
cost_dict = {}
minHeap = [(0, (0, 0))] # cost, pos
while minHeap:
    cost, pos = heapq.heappop(minHeap)
    if pos in cost_dict:
        continue

    cost_dict[pos] = cost
    for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        new_y = pos[0] + dy
        new_x = pos[1] + dx
        
        if new_y >= 0 and new_y < len(map) and new_x >= 0 and new_x < len(map[0]) \
        and map[new_y][new_x] == 0 and (new_y, new_x) not in cost_dict:
            heapq.heappush(minHeap, (cost+1, (new_y, new_x)))

print(cost_dict[(size, size)])

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import heapq

arr = load_data(1)

size = 70
map = np.zeros((size+1, size+1))

found = False
i = 0
found_path = []
while not found:
    # 0 = walkable, -1 = corrupted
    x, y = arr[i]
    map[y][x] = -1
    
    if len(found_path) > 0 and (y, x) not in found_path: # The new obstacle didn't change the best path
        i += 1
        continue

    # Perform Dijkstra's (although BFS would work just fine)
    cost_dict = {}
    minHeap = [(0, (0, 0), (-1, -1))] # cost, pos, predecessor
    while minHeap:
        cost, pos, predecessor = heapq.heappop(minHeap)
        if pos in cost_dict:
            continue

        cost_dict[pos] = (cost, predecessor)
        for dy, dx in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_y = pos[0] + dy
            new_x = pos[1] + dx
            
            if new_y >= 0 and new_y < len(map) and new_x >= 0 and new_x < len(map[0]) \
            and map[new_y][new_x] == 0 and (new_y, new_x) not in cost_dict:
                heapq.heappush(minHeap, (cost+1, (new_y, new_x), pos))

    if (size, size) not in cost_dict:
        found = True
        print(x, y)
    else:
        # Construct the path
        found_path = [(size, size)]
        predecessor = cost_dict[(size, size)][1]
        while predecessor != (-1, -1):
            found_path.append(predecessor)
            predecessor = cost_dict[predecessor][1]
        i += 1


