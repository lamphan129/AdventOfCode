# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [list(row[0]) for row in arr]
print(arr)

# %%
chars = []

antenna_arr = np.zeros((len(arr), len(arr[0])))
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i][j] != '.' and arr[i][j] != '#':
            # Find each char
            chars.append((arr[i][j], i, j))
            char = arr[i][j]

            # Check for other found characters
            for c in chars:
                if c[0] == char:
                    y = i - c[1]
                    x = j - c[2]

                    if x != 0 or y != 0:
                        dest = (i + y, j + x)
                        if dest[0] >= 0 and dest[0] < len(arr) and dest[1] >= 0 and dest[1] < len(arr[0]) and antenna_arr[dest[0]][dest[1]] == 0:
                            antenna_arr[dest[0]][dest[1]] = 1

                        dest2 = (c[1] - y, c[2] - x)
                        if dest2[0] >= 0 and dest2[0] < len(arr) and dest2[1] >= 0 and dest2[1] < len(arr[0]) and antenna_arr[dest2[0]][dest2[1]] == 0:
                            antenna_arr[dest2[0]][dest2[1]] = 1

print(np.sum(antenna_arr))

# %%
chars = []

antenna_arr = np.zeros((len(arr), len(arr[0])))
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if arr[i][j] != '.' and arr[i][j] != '#':
            # Find each char
            chars.append((arr[i][j], i, j))
            char = arr[i][j]
            antenna_arr[i][j] = 1

            # Check for other found characters
            for c in chars:
                if c[0] == char:
                    y = i - c[1]
                    x = j - c[2]

                    if x != 0 or y != 0:
                        dest = (i + y, j + x)
                        
                        while dest[0] >= 0 and dest[0] < len(arr) and dest[1] >= 0 and dest[1] < len(arr[0]):
                            if antenna_arr[dest[0]][dest[1]] == 0:
                                antenna_arr[dest[0]][dest[1]] = 1
                            dest = (dest[0] + y, dest[1] + x)

                        dest2 = (c[1] - y, c[2] - x)
                        while dest2[0] >= 0 and dest2[0] < len(arr) and dest2[1] >= 0 and dest2[1] < len(arr[0]):
                            if antenna_arr[dest2[0]][dest2[1]] == 0:
                                antenna_arr[dest2[0]][dest2[1]] = 1
                            dest2 = (dest2[0] - y, dest2[1] - x)


print(np.sum(antenna_arr))
print(antenna_arr)


