# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [list(row[0]) for row in arr]
arr = [[int(x) if x != '.' else -1 for x in row] for row in arr]
print(arr)

# %%
sum = 0
for i in range(len(arr)):
    for j in range(len(arr[i])):
        # Find trailheads
        if arr[i][j] == 0:
            # Find possible paths, using bfs
            q = [(i,j)]
            found = []

            while q:
                m,n = q.pop(0)
                if arr[m][n] == 9 and (m,n) not in found: # Found a hike
                    found.append((m,n))
                    sum += 1
                    continue

                for dm,dn in [(0,1),(0,-1),(1,0),(-1,0)]:
                    if 0 <= m+dm < len(arr) and 0 <= n+dn < len(arr[i]) and arr[m+dm][n+dn] - arr[m][n] == 1:
                        q.append((m+dm,n+dn))
            
print(sum)

# %%
sum = 0
for i in range(len(arr)):
    for j in range(len(arr[i])):
        # Find trailheads
        if arr[i][j] == 0:
            # Find possible paths, using bfs
            q = [(i,j)]

            while q:
                m,n = q.pop(0)
                if arr[m][n] == 9: # Found a hike
                    sum += 1
                    continue

                for dm,dn in [(0,1),(0,-1),(1,0),(-1,0)]:
                    if 0 <= m+dm < len(arr) and 0 <= n+dn < len(arr[i]) and arr[m+dm][n+dn] - arr[m][n] == 1:
                        q.append((m+dm,n+dn))
            
print(sum)

# %%
2 8 7 2 1 7 3
0 2 10 17 19 20 27


