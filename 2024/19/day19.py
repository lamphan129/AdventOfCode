# %%
import pandas as pd
import numpy as np

def load_data(option):
    if option == 0:
        with open('sample.txt') as f:
            data = f.read().splitlines()
    else:
        with open('input.txt') as f:
            data = f.read().splitlines()

    arr = pd.DataFrame(data).to_numpy()
    patterns = [pat.strip() for pat in arr[0][0].split(',')]
    designs = [des[0] for des in arr[2:]]

    return patterns, designs

patterns, designs = load_data(0)
print(patterns, designs)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import heapq

patterns, designs = load_data(1)

# Gather a dictionary of patterns for fast access
patternDict = {}
for pattern in patterns:
    firstChar = pattern[0]
    if firstChar not in patternDict:
        patternDict[firstChar] = [pattern]
    else:
        patternDict[firstChar].append(pattern)

total = 0
for design in designs:
    minHeap = [(len(design), design)] # remaining chars, remaining design to match
    found = False

    while minHeap and not found:
        remainChars, subdesign = heapq.heappop(minHeap)
        firstChar = subdesign[0]

        if firstChar in patternDict:
            for pattern in patternDict[firstChar]:
                match = re.search(pattern, subdesign)

                if match != None and match.start() == 0:
                    if len(pattern) == remainChars: # Found possible designs
                        found = True
                        total += 1
                    else:
                        heapq.heappush(minHeap, (remainChars - len(pattern), subdesign[len(pattern):]))

print(total)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

patterns, designs = load_data(1)

# Gather a dictionary of patterns for fast access
patternDict = {}
for pattern in patterns:
    firstChar = pattern[0]
    if firstChar not in patternDict:
        patternDict[firstChar] = [pattern]
    else:
        patternDict[firstChar].append(pattern)

# Memoization
memo = {}

# Recursive loop
def recursive(remainChars, subdesign):
    if subdesign in memo:
        return memo[subdesign]
    
    firstChar = subdesign[0]
    subtotal = 0
    if firstChar in patternDict:
        for pattern in patternDict[firstChar]:
            match = re.search(pattern, subdesign)

            if match != None and match.start() == 0:
                if len(pattern) == remainChars: # Base case
                    subtotal += 1
                else:
                    subtotal += recursive(remainChars - len(pattern), subdesign[len(pattern):])
        
    if subdesign not in memo:
        memo[subdesign] = subtotal
    return subtotal

# Check each design
total = 0
for design in designs:
    total += recursive(len(design), design)

print(total)


