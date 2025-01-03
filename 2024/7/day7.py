# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

df = pd.DataFrame(data)
print(df)

# %%
import itertools

def calculate(x1, x2, op):
    if op == '+':
        return x1 + x2
    elif op == '*':
        return x1 * x2

sum = 0
for row in df.iterrows():
    data = row[1].values[0]
    
    target, nums = data.split(':')
    target = int(target)
    nums = [int(num) for num in nums.strip().split(' ')]
    
    possible_ops = itertools.product(['+', '*'], repeat=len(nums) - 1)
    
    for ops in possible_ops:
        result = 0
        for i in range(len(nums)):
            if i == 0:
                result = nums[i]
                continue

            result = calculate(result, nums[i], ops[i-1])

        if result == target:
            sum += target
            break

print(sum)

# %%
import itertools

def calculate(x1, x2, op):
    if op == '+':
        return x1 + x2
    elif op == '*':
        return x1 * x2
    elif op == '|':
        return int(str(x1) + str(x2))

sum = 0
for row in df.iterrows():
    data = row[1].values[0]
    
    target, nums = data.split(':')
    target = int(target)
    nums = [int(num) for num in nums.strip().split(' ')]
    
    possible_ops = itertools.product(['+', '*', '|'], repeat=len(nums) - 1)
    
    for ops in possible_ops:
        result = 0
        for i in range(len(nums)):
            if i == 0:
                result = nums[i]
                continue

            result = calculate(result, nums[i], ops[i-1])

        if result == target:
            sum += target
            break

print(sum)


