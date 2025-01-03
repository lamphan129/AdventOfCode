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
    arr = [int(row[0]) for row in arr]

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

arr = load_data(1)

# Given an input number, return the next secret number
def find_secret(num):
    secret = ((num * 64) ^ num) % 16777216
    secret = (int(secret / 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

total = 0
for num in arr:
    for i in range(2000):
        num = find_secret(num)
    total += num
print(total)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools

arr = load_data(1)

# Given an input number, return the next secret number
def find_secret(num):
    secret = ((num * 64) ^ num) % 16777216
    secret = (int(secret / 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

# index: (num_list: int, diff_list: str)
num_dir = {}
for i, num in enumerate(arr):
    num_list = [num % 10]
    for j in range(2000):
        num = find_secret(num)
        num_list.append(num % 10)

    # diff_list has value ranging from -9 to 9, which is mapped to A-S for easier pattern matching
    # This list doesn't contain the difference between the 1st and 2nd elements
    diff_list = [chr(num_list[j] - num_list[j-1] + 74) for j, _ in enumerate(num_list) if j > 0]
    num_dir[i] = (num_list, ''.join(diff_list))

# Find total sequence count
sequence_dict = {}
for num_list, diff_str in num_dir.values():
    cur_dict = {}
    
    for i in range(len(diff_str)-3):
        sequence = diff_str[i:i+4]
        if sequence not in cur_dict:
            if sequence not in sequence_dict:
                cur_dict[sequence] = num_list[i+4]
            else:
                cur_dict[sequence] = sequence_dict[sequence] + num_list[i+4]

    # Update total count
    sequence_dict.update(cur_dict)

print(max(sequence_dict.values()))


