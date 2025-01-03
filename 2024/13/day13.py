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
    arr = [[int(num) for num in re.findall(r'\d+', row[0])] for row in arr]

    return arr

arr = load_data(0)
print(arr)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)

cost = 0
for i in range(0, len(arr), 4):
    a = arr[i]
    b = arr[i+1]
    target = arr[i+2]

    x, y = np.linalg.solve([[a[0], b[0]], [a[1], b[1]]], target)

    if abs(round(x) - x) < 1e-2 and abs(round(y) - y) < 1e-2 and x > 0 and x < 100 and y > 0 and y < 100:
        cost += 3*round(x) + round(y)
print(cost)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

arr = load_data(1)

cost = 0
for i in range(0, len(arr), 4):
    a = arr[i]
    b = arr[i+1]
    target = [arr[i+2][0] + 10000000000000, arr[i+2][1] + 10000000000000]

    x, y = np.linalg.solve([[a[0], b[0]], [a[1], b[1]]], target)

    if abs(round(x) - x) < 1e-2 and abs(round(y) - y) < 1e-2 and x > 0 and y > 0:
        cost += 3*round(x) + round(y)
print(cost)


