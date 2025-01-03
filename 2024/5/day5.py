# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

df = pd.DataFrame(data)
print(df)

# %%
# Find all rules
import re

rule_forward = {}
rule_backward = {}
sum = 0
for data in df.iterrows():
    data = data[1].values[0]
    value = re.split(r'\|', data)
    
    # Its a rule
    if len(value) == 2:
        first_val, second_val = int(value[0]), int(value[1])
        if first_val not in rule_forward:
            rule_forward[first_val] = [second_val]
        else:
            rule_forward[first_val].append(second_val)

        if second_val not in rule_backward:
            rule_backward[second_val] = [first_val]
        else:
            rule_backward[second_val].append(first_val)

    # Its an update
    elif value[0] != '':
        valid = True
        list = np.array([int(x) for x in value[0].split(',')])
        
        for i in range(len(list)):
            forward_list = np.delete(list[i:], 0)
            backward_list = list[:i]

            if len(forward_list) > 0:
                if list[i] in rule_forward and len(np.intersect1d(rule_forward[list[i]], forward_list)) != len(forward_list):
                    valid = False
                    break

            if len(backward_list) > 0:
                if list[i] in rule_backward and len(np.intersect1d(rule_backward[list[i]], backward_list)) != len(backward_list):
                    valid = False
                    break

        if valid:
            sum += list[len(list)//2]

print(sum)

# %%
# Find all rules
import re

rule_forward = {}
rule_backward = {}
sum = 0
for data in df.iterrows():
    data = data[1].values[0]
    value = re.split(r'\|', data)
    
    # Its a rule
    if len(value) == 2:
        first_val, second_val = int(value[0]), int(value[1])
        if first_val not in rule_forward:
            rule_forward[first_val] = [second_val]
        else:
            rule_forward[first_val].append(second_val)

        if second_val not in rule_backward:
            rule_backward[second_val] = [first_val]
        else:
            rule_backward[second_val].append(first_val)

    # Its an update
    elif value[0] != '':
        valid = True
        list = np.array([int(x) for x in value[0].split(',')])
        
        for i in range(len(list)):
            forward_list = np.delete(list[i:], 0)
            backward_list = list[:i]

            if len(forward_list) > 0:
                if list[i] in rule_forward and len(np.intersect1d(rule_forward[list[i]], forward_list)) != len(forward_list):
                    valid = False
                    break

            if len(backward_list) > 0:
                if list[i] in rule_backward and len(np.intersect1d(rule_backward[list[i]], backward_list)) != len(backward_list):
                    valid = False
                    break

        if not valid:
            backward_count = []
            for i in range(len(list)):
                list_without_i = np.delete(list, i)
                backward_count.append(len(np.intersect1d(rule_backward[list[i]], list_without_i)))

            fixed_list = np.zeros_like(list)
            for i, count in enumerate(backward_count):
                fixed_list[count] = list[i]

            sum += fixed_list[len(fixed_list)//2]
            
print(sum)


