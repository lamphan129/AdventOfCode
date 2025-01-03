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
    arr = [re.findall(r'(\w+)-(\w+)', row[0])[0] for row in arr]

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

arr = load_data(1)

# Store connection in dictionary for fast access
# Only count connection starting with 't'
dict = {}
for con in arr:
    a, b = con
    if a[0] == 't':
        if a not in dict:
            dict[a] = set([b])
        else:
            dict[a].add(b)
    
    if b[0] == 't':
        if b not in dict:
            dict[b] = set([a])
        else:
            dict[b].add(a)

# Check for three inter-connected computers
found_set = []
for key, value in dict.items():
    value = list(value)
    for i in range(len(value)-1):
        for j in range(i+1, len(value)):
            if (value[i], value[j]) in arr or (value[j], value[i]) in arr:
                found_set.append({key, value[i], value[j]})

# Remove duplicates:
count = len(found_set)
for i in range(len(found_set)-1, -1, -1):
    for j in range(i-1, -1, -1):
        if len(found_set[i].intersection(found_set[j])) == 3:
            count -= 1
print(count)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

arr = load_data(1)

# Store connection in dictionary for fast access
dict = {}
for con in arr:
    a, b = con

    if a not in dict:
        dict[a] = set([b])
    else:
        dict[a].add(b)

    if b not in dict:
        dict[b] = set([a])
    else:
        dict[b].add(a)

# For each node, check the largest possible set and store all connections
largest_set = set([])
for key, values in dict.items():
    # Establish the connectivity dir
    # The count reflect the number of neighbors (excluding self)
    connectivity_dir = {}
    for value in values:
        connectivity_dir[value] = 1
    
    # Calculate the connectivity (basically a 2-step BFS from key)
    for other_key in values:
        for value in dict[other_key]:
            if value != key:
                if value not in connectivity_dir:
                    connectivity_dir[value] = 1
                else:
                    connectivity_dir[value] += 1

    # Flip the directory (so that it becomes count: members)
    set_dir = {}
    for other_key, value in connectivity_dir.items():
        if value not in set_dir:
            set_dir[value] = set([other_key])
        else:
            set_dir[value].add(other_key)

    # Does the largest count (except for self) higher than the current best set?
    max_count = max(set_dir.keys())
    if max_count <= len(largest_set):
        continue

    # Does the largest set makes sense (there could be more than one largest set from self)
    if len(set_dir[max_count]) != max_count:
        continue

    # We found a new max set, save it
    largest_set = set_dir[max_count]
    largest_set.add(key)

# Once the largest set is found, sort them
sorted_set = sorted(largest_set)
print(','.join(sorted_set))


