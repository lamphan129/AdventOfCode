# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

arr = pd.DataFrame(data).to_numpy()
arr = [list(row[0]) for row in arr]
arr = [int(item) for item in arr[0]]
print(arr)

# %%
# Constrict the disk map
disk = []
id = 0
for i in range(len(arr)):
    if i % 2 == 0:
        disk.extend([id]*arr[i])
        id += 1
    else:
        disk.extend([-1]*arr[i])

# Move the elements
start = 0
end = len(disk) - 1

while start < end:
    if disk[start] != -1:
        start += 1
    else:
        if disk[end] == -1:
            end -= 1
        else:
            disk[start], disk[end] = disk[end], disk[start]
            start += 1
            end -= 1

# Find checksum
checksum = 0
for i, item in enumerate(disk):
    if item != -1:
        checksum += i * item
print(checksum)

# %%
arr = [2, 3, 0, 5, 7, 2, 1, 5, 0, 2, 0, 0, 3]

# Constrict the disk map
disk = []
id = 0
for i in range(len(arr)):
    if i % 2 == 0:
        disk.extend([id]*arr[i])
        id += 1
    else:
        disk.extend([-1]*arr[i])

# Move blocks to its leftist position (if possible)
num_block = [arr[i] for i in range(len(arr)) if i % 2 == 0]
space_block = [arr[i] for i in range(len(arr)) if i % 2 == 1]
num_pos = [sum(num_block[:i] + space_block[:i]) for i in range(len(num_block))]
space_pos = [sum(num_block[:i+1] + space_block[:i]) for i in range(len(space_block))]

# Merge two consecutive space blocks
for i in range(len(num_block)-1, -1, -1):
    if num_block[i] == 0 and i > 0 and i <= len(num_block)-1:
        space_block[i-1] += space_block[i]
        space_block[i] = 0

# Remove 0 (this is unnecessary, I think, but just to be safe)
for i in range(len(num_block)-1, -1, -1):
    if num_block[i] == 0:
        num_block.pop(i)
        num_pos.pop(i)

for i in range(len(space_block)-1, -1, -1):
    if space_block[i] == 0:
        space_block.pop(i)
        space_pos.pop(i)

for i in range(len(num_block)-1, -1, -1):
    for j in range(len(space_block)):
        if space_block[j] >= num_block[i] and space_pos[j] < num_pos[i]:
            disk[space_pos[j]:space_pos[j]+num_block[i]], disk[num_pos[i]:num_pos[i]+num_block[i]] = disk[num_pos[i]:num_pos[i]+num_block[i]], disk[space_pos[j]:space_pos[j]+num_block[i]]
            space_block[j] -= num_block[i]
            space_pos[j] += num_block[i]
            num_block[i] = 0
            break

# Find checksum
checksum = 0
for i, item in enumerate(disk):
    if item != -1:
        checksum += i * item
print(checksum)

# %%
2 8 7 2 1 7 3
0 2 10 17 19 20 27


