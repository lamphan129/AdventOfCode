# %%
import pandas as pd
import numpy as np

df = pd.read_csv('input.txt', header=None)
print(df)

# %%
num_safe = 0
for row in df.iterrows():
    safe = True
    report = np.array(row[1].values[0].split(' ')).astype(int)
    
    # If increasing
    if report[0] < report[-1]:
        for i in range(len(report) - 1):
            if report[i+1] - report[i] < 1 or report[i+1] - report[i] > 3:
                safe = False
                break
    # If decreasing
    else:
        for i in range(len(report) - 1):
            if report[i] - report[i+1] < 1 or report[i] - report[i+1] > 3:
                safe = False
                break
                
    if safe:
        num_safe += 1

print(num_safe)

# %%
num_safe = 0
for row in df.iterrows():
    this_shit = True
    that_shit = True
    report = np.array(row[1].values[0].split(' ')).astype(int)

    # Check for increasing
    for i in range(len(report) - 1):
        if report[i+1] - report[i] < 1 or report[i+1] - report[i] > 3:
            # Second check
            # Remove the first value
            this_little_shit = True
            list1 = np.delete(report, i)
            for j in range(len(list1) - 1):
                if this_little_shit and (list1[j+1] - list1[j] < 1 or list1[j+1] - list1[j] > 3):
                    this_little_shit = False
            
            # Remove the last value
            this_second_little_shit = True
            list2 = np.delete(report, i+1)
            for j in range(len(list2) - 1):
                if this_second_little_shit and (list2[j+1] - list2[j] < 1 or list2[j+1] - list2[j] > 3):
                    this_second_little_shit = False

            if not (this_little_shit or this_second_little_shit): # Both are shit
                this_shit = False

    # Check for decreasing
    for i in range(len(report) - 1):
        if report[i] - report[i+1] < 1 or report[i] - report[i+1] > 3:
            # Second check
            # Remove the first value
            that_little_shit = True
            list1 = np.delete(report, i)
            for j in range(len(list1) - 1):
                if that_little_shit and (list1[j] - list1[j+1] < 1 or list1[j] - list1[j+1] > 3):
                    that_little_shit = False
            
            # Remove the last value
            that_second_little_shit = True
            list2 = np.delete(report, i+1)
            for j in range(len(list2) - 1):
                if that_second_little_shit and (list2[j] - list2[j+1] < 1 or list2[j] - list2[j+1] > 3):
                    that_second_little_shit = False
            
            if not (that_little_shit or that_second_little_shit): # Both are shit (again)
                that_shit = False

    if this_shit or that_shit: # Some of the shit are safe
        num_safe += 1

print(num_safe)

# %%
import cv2
import numpy as np

# Contrast enhancement
old_mean = np.mean(img)
brightness = -(old_mean - 100.0)
img = cv2.addWeighted(img, 1, img, 0, brightness)

# Linear Stretching
new_mean = np.mean(img)
new_std = np.std(img)
img = ((img - old_mean) / new_std) * 255 + new_mean


