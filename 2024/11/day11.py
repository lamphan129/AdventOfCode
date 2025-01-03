# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [int(num) for num in arr[0][0].split(' ')]
print(arr)

# %%
from tqdm import tqdm

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [int(num) for num in arr[0][0].split(' ')]
print(arr)

# Return list of numbers
def rule(num):
    num_str = str(num)
    if num_str == '0':
        return [1]
    elif len(list(num_str)) % 2 == 0:
        mid = (len(list(num_str)) // 2)
        return [int(num_str[:mid]), int(num_str[mid:])]
    else:
        return [int(num * 2024)]

num_blink = 25
for _ in tqdm(range(num_blink)):
    new_arr = []
    for num in arr:
        new_arr.extend(rule(num))
    arr = new_arr
print(len(arr))

# %%
from tqdm import tqdm

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [int(num) for num in arr[0][0].split(' ')]
print(arr)

# Return list of numbers
def rule(num):
    num_str = str(num)
    if num_str == '0':
        return [1]
    elif len(list(num_str)) % 2 == 0:
        mid = (len(list(num_str)) // 2)
        return [int(num_str[:mid]), int(num_str[mid:])]
    else:
        return [int(num * 2024)]

count_map = {}

for num in arr:
    if num not in count_map:
        count_map[num] = 1
    else:
        count_map[num] += 1

num_blink = 75
for _ in tqdm(range(num_blink)):
    new_map = {}
    for num in count_map.keys():
        count = count_map[num]
        result = rule(num)

        if len(result) == 2:
            if result[0] not in new_map:
                new_map[result[0]] = count
            else:
                new_map[result[0]] += count

            if result[1] not in new_map:
                new_map[result[1]] = count
            else:
                new_map[result[1]] += count
        else:
            if result[0] not in new_map:
                new_map[result[0]] = count
            else:
                new_map[result[0]] += count
    count_map = new_map

print(sum(list(count_map.values())))


