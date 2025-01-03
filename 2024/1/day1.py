# %%
import pandas as pd
import numpy as np

df = pd.read_csv('input.txt', sep='   ', header=None)
print(df)

# %%
list1 = np.array(df.iloc[:, 0].tolist())
list1.sort()

list2 = np.array(df.iloc[:, 1].tolist())
list2.sort()

sum = np.sum(np.abs(list1 - list2))
print(sum)

# %%
dict = {}
for num in list2:
    if num in dict.keys():
        dict[num] += 1
    else:
        dict[num] = 1

similarity_score = 0
for num in list1:
    if num in dict.keys():
        similarity_score += num * dict[num]

print(similarity_score)


