# %%
import pandas as pd
import numpy as np
import re

def load_data(option):
    if option == 0:
        with open('sample.txt') as f:
            data = f.read().splitlines()
    else:
        with open('input.txt') as f:
            data = f.read().splitlines()

    arr = pd.DataFrame(data).to_numpy()
    print()
    arr = [re.findall(r'(\d+)', row[0]) for row in arr]
    a, b, c, _, program = arr

    return int(a[0]), int(b[0]), int(c[0]), [int(op) for op in program]

a, b, c, program = load_data(0)
print(a, b, c, program)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

a, b, c, program = load_data(1)

# Return value of the combo, based on operand
def combo(operand):
    global a, b, c
    match operand:
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c
        case 7:
            return None
        case _:
            return operand

# Perform operation, given opcode and operand
# Operation 3 is not included since it deals with pointer location
# This function return any output (if any)
def perform_op(opcode, operand):
    global a, b, c
    match opcode:
        case 0:
            a = int(a / 2**(combo(operand)))
        case 1:
            x = list(format(b, 'b'))
            y = list(format(operand, 'b'))
            
            # Fill in 0
            diff = abs(len(x) - len(y))
            if len(x) < len(y):
                x = (['0'] * diff) + x
            else:
                y = (['0'] * diff) + y

            b = int(''.join([str(int(x != y)) for x, y in zip(x, y)]), 2)
        case 2:
            b = combo(operand) % 8
        case 4:
            x = list(format(b, 'b'))
            y = list(format(c, 'b'))
            
            # Fill in 0
            diff = abs(len(x) - len(y))
            if len(x) < len(y):
                x = (['0'] * diff) + x
            else:
                y = (['0'] * diff) + y

            b = int(''.join([str(int(x != y)) for x, y in zip(x, y)]), 2)
        case 5:
            return str(combo(operand) % 8)
        case 6:
            b = int(a / 2**(combo(operand)))
        case 7:
            c = int(a / 2**(combo(operand)))

# Read the instructions and follow until halt
pointer = 0
output = []
while pointer < len(program):
    opcode = program[pointer]
    operand = program[pointer+1]

    # Deal with jump
    if opcode == 3:
        if a != 0:
            pointer = operand
        else:
            pointer += 2
        continue

    # Deal with out
    if opcode == 5:
        output.append(perform_op(opcode, operand))
    else:
        perform_op(opcode, operand)
    pointer += 2
print((',').join(output))

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm

a, b, c, program = load_data(1)

# Return value of the combo, based on operand
def combo(operand):
    global a, b, c
    match operand:
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c
        case 7:
            return None
        case _:
            return operand

# Perform operation, given opcode and operand
# Operation 3 is not included since it deals with pointer location
# This function return any output (if any)
def perform_op(opcode, operand):
    global a, b, c
    match opcode:
        case 0:
            a = int(a / 2**(combo(operand)))
        case 1:
            x = list(format(b, 'b'))
            y = list(format(operand, 'b'))
            
            # Fill in 0
            diff = abs(len(x) - len(y))
            if len(x) < len(y):
                x = (['0'] * diff) + x
            else:
                y = (['0'] * diff) + y

            b = int(''.join([str(int(x != y)) for x, y in zip(x, y)]), 2)
        case 2:
            b = combo(operand) % 8
        case 4:
            x = list(format(b, 'b'))
            y = list(format(c, 'b'))
            
            # Fill in 0
            diff = abs(len(x) - len(y))
            if len(x) < len(y):
                x = (['0'] * diff) + x
            else:
                y = (['0'] * diff) + y

            b = int(''.join([str(int(x != y)) for x, y in zip(x, y)]), 2)
        case 5:
            return combo(operand) % 8
        case 6:
            b = int(a / 2**(combo(operand)))
        case 7:
            c = int(a / 2**(combo(operand)))

# Read the instructions and follow until halt
possible_a = 1 # This would be changed to the starting 'a' value found below
found = False
best_correct = 0

while not found:
    a = possible_a
    pointer = 0
    output = []
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer+1]

        # Deal with jump
        if opcode == 3:
            if a != 0:
                pointer = operand
            else:
                pointer += 2
            continue

        # Deal with out
        if opcode == 5:
            output.append(perform_op(opcode, operand))
        else:
            perform_op(opcode, operand)
        pointer += 2
    res = (',').join([str(out) for out in output])
    target = ','.join([str(op) for op in program])
    
    if res == target:
        print(possible_a)
        found = True
    else:
        # Heuristically, a should be big to obtain a longer instructions
        # If the output is way smaller than the target, we increase a by a big amount
        if len(output) < len(program):
            possible_a *= 10
        else:
            """
            Initially:
            - Possible_a = 1
            - Use this code to find the starting 'a' when there are 14 MATCHES
            (If found, note the number down as stop the program)
            - Number of correct instructions is count from right to left (so, 
            in reverse)

            Note: The formula to increment possible_a might need to be fine-tuned
            depends on input length
            """
            correct = 0
            for i in range(len(output)-1, -1, -1):
                if output[i] == program[i]:
                    correct += 1
                else:
                    break

            if correct > best_correct:
                best_correct = correct
                print(f"Found {best_correct} matches at {possible_a}")
            possible_a += 2**((len(output) - correct)*2) # This might need finetuning to work

            """
            Once found:
            - Comment the previous code block out
            - Place the found value into possible_a and RUN THE CODE AGAIN
            - Since we're close to target, this time only increment possible_a by 1

            Note: Yes, I'm lazy to make it work in one try, but it works
            """
            # possible_a += 1


