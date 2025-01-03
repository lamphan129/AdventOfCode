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
    locks = []
    keys = []
    for i in range(0, len(arr), 8):
        puzzle = np.array([list(row[0]) for row in arr[i:i+7, :]])

        if np.count_nonzero(puzzle[0] == '#') == 5: # This is a lock
            pin_height = np.count_nonzero(puzzle[1:, :] == '#', axis=0)
            locks.append(pin_height)
        else: # This is a key
            pin_height = np.count_nonzero(puzzle[:-1, :] == '#', axis=0)
            keys.append(pin_height)

    return locks, keys

locks, keys = load_data(0)
print(locks, keys)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

locks, keys = load_data(1)

result = 0
for lock in locks:
    for key in keys:
        if max(lock + key) <= 5:
            result += 1
print(result)


