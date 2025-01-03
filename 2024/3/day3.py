# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

df = pd.DataFrame(data)
print(df)

# %%
import re

sum = 0
for row in df.iterrows():
  x = re.findall(r'mul\((\d+),(\d+)\)', row[1].values[0])
  for match in x:
    sum += int(match[0]) * int(match[1])
print(sum)

# %%
import re

sum = 0

full_data = ''
for row in df.iterrows():
  full_data += row[1].values[0]

value = re.split('do\(\)|don\'t\(\)', full_data)
splitter = re.findall(r'do\(\)|don\'t\(\)', full_data)

for i in range(len(value)):
    x = re.findall(r'mul\((\d+),(\d+)\)', value[i], flags=re.ASCII)

    if i == 0 or splitter[i-1] == 'do()':
        for match in x:
            sum += int(match[0]) * int(match[1])
print(sum)


