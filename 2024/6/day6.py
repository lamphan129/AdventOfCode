# %%
import pandas as pd
import numpy as np

with open('input.txt') as f:
    data = f.read().splitlines()

df = pd.DataFrame(data)
print(df)

# %%
import copy

game = np.array(df)
game = [list(row[0]) for row in game]

# Find player
player = []
for i in range(len(game)):
    for j in range(len(game[0])):
        if game[i][j] == "^":
            player = [i,j]
            break

orig_player = copy.deepcopy(player)
# Move player
# 0 = up, 1 = right, 2 = down, 3 = left
direction = 0
while (direction == 0 and player[0] > 0) or (direction == 1 and player[1] < len(game[0]) - 1) or (direction == 2 and player[0] < len(game) - 1) or (direction == 3 and player[1] > 0): # Not at border
    game[player[0]][player[1]] = "X"
    if direction == 0:
        if game[player[0] - 1][player[1]] != "#": # Up
            player[0] -= 1
        else:
            direction = 1
    elif direction == 1:
        if game[player[0]][player[1] + 1] != "#": # Right
            player[1] += 1
        else:
            direction = 2
    elif direction == 2:
        if game[player[0] + 1][player[1]] != "#": # Down
            player[0] += 1
        else:
            direction = 3
    elif direction == 3:
        if game[player[0]][player[1] - 1] != "#": # Left
            player[1] -= 1
        else:
            direction = 0

# Mark at exit
game[player[0]][player[1]] = "X"

orig_game = copy.deepcopy(game)
print(np.sum([row.count("X") for row in game]))

# %%
import copy
from tqdm import tqdm
import numpy as np

empty_game = np.array(df)
empty_game = [list(row[0]) for row in empty_game]

# Move player
# 0 = up, 1 = right, 2 = down, 3 = left
# Xu, Xr, Xd, Xl
sum = 0
for i in tqdm(range(len(orig_game))):
    for j in range(len(orig_game[0])):
        # Check if its possible to add obstacle
        if orig_game[i][j] != "X" or (i == orig_player[0] and j == orig_player[1]):
            continue

        # Try add obstacle at X
        game = copy.deepcopy(empty_game)
        game[i][j] = "#"
        player = copy.deepcopy(orig_player)
        
        direction = 0
        loop = False
        while (direction == 0 and player[0] > 0) or (direction == 1 and player[1] < len(game[0]) - 1) or (direction == 2 and player[0] < len(game) - 1) or (direction == 3 and player[1] > 0): # Not at border
            if direction == 0:
                if game[player[0] - 1][player[1]] != "#": # Up
                    game[player[0]][player[1]] = "Xu"
                    player[0] -= 1
                else:
                    direction = 1
            elif direction == 1:
                if game[player[0]][player[1] + 1] != "#": # Right
                    game[player[0]][player[1]] = "Xr"
                    player[1] += 1
                else:
                    direction = 2
            elif direction == 2:
                if game[player[0] + 1][player[1]] != "#": # Down
                    game[player[0]][player[1]] = "Xd"
                    player[0] += 1
                else:
                    direction = 3
            elif direction == 3:
                if game[player[0]][player[1] - 1] != "#": # Left
                    game[player[0]][player[1]] = "Xl"
                    player[1] -= 1
                else:
                    direction = 0

            # Check if loop
            if (direction == 0 and game[player[0]][player[1]] == "Xu") or \
            (direction == 1 and game[player[0]][player[1]] == "Xr") or \
            (direction == 2 and game[player[0]][player[1]] == "Xd") or \
            (direction == 3 and game[player[0]][player[1]] == "Xl"):
                loop = True
                break

        if loop:
            sum += 1

print(sum)


