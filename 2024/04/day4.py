# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

df = pd.DataFrame(data)
print(df)

# %%
data_arr = np.array([list(string) for string in data])
print(''.join(data_arr[3:0:-1, 0]))

# %%
# Search 'XMAS' in all direction

sum = 0
for i in range(len(data_arr)):
    for j in range(len(data_arr[0])):
        # Horizontal
        if j < len(data_arr[0]) - 3:
            if ''.join(data_arr[i, j:j+4]) == 'XMAS':
                sum += 1
        if j > 2:
            if j == 3 and ''.join(data_arr[i, j::-1]) == 'XMAS': # Special case
                sum += 1
            elif ''.join(data_arr[i, j:j-4:-1]) == 'XMAS':
                sum += 1

        # Vertical
        if i < len(data_arr) - 3:
            if ''.join(data_arr[i:i+4, j]) == 'XMAS':
                sum += 1
        if i > 2:
            if i == 3 and ''.join(data_arr[i::-1, j]) == 'XMAS': # Special case
                sum += 1
            if ''.join(data_arr[i:i-4:-1, j]) == 'XMAS':
                sum += 1

        # Diagonal
        if i < len(data_arr) - 3 and j < len(data_arr[0]) - 3:
            if ''.join((data_arr[i][j], data_arr[i+1][j+1], data_arr[i+2][j+2], data_arr[i+3][j+3])) == 'XMAS':
                sum += 1
        if i < len(data_arr) - 3 and j > 2:
            if ''.join((data_arr[i][j], data_arr[i+1][j-1], data_arr[i+2][j-2], data_arr[i+3][j-3])) == 'XMAS':
                sum += 1
        if i > 2 and j < len(data_arr[0]) - 3:
            if ''.join((data_arr[i][j], data_arr[i-1][j+1], data_arr[i-2][j+2], data_arr[i-3][j+3])) == 'XMAS':
                sum += 1
        if i > 2 and j > 2:
            if ''.join((data_arr[i][j], data_arr[i-1][j-1], data_arr[i-2][j-2], data_arr[i-3][j-3])) == 'XMAS':
                sum += 1

print(sum)

# %%
# Search 'MAS' X shape

sum = 0
for i in range(len(data_arr)):
    for j in range(len(data_arr[0])):
        if i < len(data_arr) - 2 and j < len(data_arr[0]) - 2:
            if (''.join((data_arr[i][j], data_arr[i+1][j+1], data_arr[i+2][j+2])) == 'MAS' or
                ''.join((data_arr[i][j], data_arr[i+1][j+1], data_arr[i+2][j+2])) == 'SAM') and \
               (''.join((data_arr[i+2][j], data_arr[i+1][j+1], data_arr[i][j+2])) == 'MAS' or
                ''.join((data_arr[i+2][j], data_arr[i+1][j+1], data_arr[i][j+2])) == 'SAM'):
                sum += 1

print(sum)


