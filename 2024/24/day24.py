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
    gate_val = {}
    gate_con = {}
    for row in arr:
        value = re.split(':', row[0])
        
        if len(value) == 2: # It's a gate value
            gate_val[value[0]] = int(value[1].strip())
        elif value[0] != '': # It's a gate connection (target_gate: (input_gates, operations))
            value = re.split('->', row[0])
            input_gates = re.split('(AND|OR|XOR)', value[0])
            gate_con[value[1].strip()] = ((input_gates[0].strip(), input_gates[2].strip()), input_gates[1])

    return gate_val, gate_con

gate_val, gate_con = load_data(0)
print(gate_val, gate_con)

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

gate_val, gate_con = load_data(1)

def compute_gate(input_1, input_2, op):
    match op:
        case 'AND':
            return input_1 and input_2
        case 'OR':
            return input_1 or input_2
        case 'XOR':
            return input_1 ^ input_2

# Count total gate starts with z
total = 0
for gate in gate_con.keys():
    if gate[0] == 'z':
        total += 1

# Iterate over all rules until all gates start with 'z' have a value
while total > 0:
    calculated_gate = [] # Keep track of which gate was calculated
    for gate, rule in gate_con.items():
        # Check if all inputs exists
        if rule[0][0] in gate_val and rule[0][1] in gate_val:
            gate_val[gate] = compute_gate(gate_val[rule[0][0]], gate_val[rule[0][1]], rule[1])
            calculated_gate.append(gate)

    # Remove calculated gate
    for gate in calculated_gate:
        gate_con.pop(gate)

        # Reduce count
        if gate[0] == 'z':
            total -= 1

# Obtain only gate value starting with z
z_gates = []
for gate in gate_val:
    if gate[0] == 'z':
        z_gates.append(gate)

# Reverse sort
z_gates_sorted = sorted(z_gates, reverse=True)
z_gates_str_val = [str(gate_val[gate]) for gate in z_gates_sorted]
print(int(''.join(z_gates_str_val), 2))

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

gate_val, gate_con = load_data(1)

def compute_gate(input_1, input_2, op):
    match op:
        case 'AND':
            return input_1 and input_2
        case 'OR':
            return input_1 or input_2
        case 'XOR':
            return input_1 ^ input_2

# Count total gate starts with z
total = 0
for gate in gate_con.keys():
    if gate[0] == 'z':
        total += 1

# Iterate over all rules until all gates start with 'z' have a value
while total > 0:
    calculated_gate = [] # Keep track of which gate was calculated
    for gate, rule in gate_con.items():
        # Check if all inputs exists
        if rule[0][0] in gate_val and rule[0][1] in gate_val and gate not in gate_val:
            gate_val[gate] = compute_gate(gate_val[rule[0][0]], gate_val[rule[0][1]], rule[1])
            calculated_gate.append(gate)

    for gate in calculated_gate:
        # Reduce count
        if gate[0] == 'z':
            total -= 1

# Obtain only gate value starting with x, y, and z
x_gates = []
for gate in gate_val:
    if gate[0] == 'x':
        x_gates.append(gate)

y_gates = []
for gate in gate_val:
    if gate[0] == 'y':
        y_gates.append(gate)

z_gates = []
for gate in gate_val:
    if gate[0] == 'z':
        z_gates.append(gate)

# Reverse sort
z_gates_sorted = sorted(z_gates, reverse=True)
z_gates_str_val = [str(gate_val[gate]) for gate in z_gates_sorted]

########
# Obtain the flipped directory for easier access
gate_con_flip = {} # (Gate inputs, operation): Gate output
for gate, rule in gate_con.items():
    gate_con_flip[rule] = gate

# Rename gate - 1st pass: x, y, and z
renamed_dir = {}
for gates in [x_gates, y_gates, z_gates]:
    for gate in gates:
        renamed_dir[gate] = gate

# Rename gate - 2nd pass: rename every other gate until no changes were made
patience = 10
old_size = len(renamed_dir)
while patience > 0:
    # Did we make new changes?
    if len(renamed_dir) > old_size:
        patience = 10
        old_size = len(renamed_dir)
    else:
        patience -= 1
    
    for ((input_1, input_2), op), output_gate in gate_con_flip.items():
        # If the gate has already been renamed, skip
        if output_gate in renamed_dir:
            continue
        
        if input_1 in renamed_dir:
            input_1 = renamed_dir[input_1]
        if input_2 in renamed_dir:
            input_2 = renamed_dir[input_2]
        init_char = set([input_1[0], input_2[0]])
        # If the two input gates start with x and y, rename their respective output gates
        if len(init_char.intersection({'x', 'y'})) == 2:
            num = input_1[1:]

            if num == '00' and op == 'AND':
                renamed_dir[output_gate] = 'CARRY00'
            else:
                if op == 'AND':
                    renamed_dir[output_gate] = f'1STCARRY{num}'
                elif op == 'XOR':
                    renamed_dir[output_gate] = f'HALFSUM{num}'
        elif len(init_char.intersection({'C', 'H'})) == 2 and op == 'AND':
            num = max(input_1[-2:], input_2[-2:])
            renamed_dir[output_gate] = f'2NDCARRY{num}'
        elif len(init_char.intersection({'1', '2'})) == 2 and op == 'OR':
            num = input_1[-2:]
            renamed_dir[output_gate] = f'CARRY{num}'

# Use the renamed directory, fix the directory
renamed_con = {}
for gate_input, gate_output in gate_con_flip.items():
    new_input = ((renamed_dir.get(gate_input[0][0], gate_input[0][0]), renamed_dir.get(gate_input[0][1], gate_input[0][1])), gate_input[1])
    new_output = renamed_dir.get(gate_output, gate_output)
    
    renamed_con[new_input] = new_output

# Stop if there's any inconsistency
for i in range(len(x_gates)):
    num = f'{i:02d}'
    prev_num = f'{i-1:02d}'

    if num == '00':
        xor_output = renamed_con.get(((f'x{num}', f'y{num}'), 'XOR')) or renamed_con.get(((f'y{num}', f'x{num}'), 'XOR'))
        and_output = renamed_con.get(((f'x{num}', f'y{num}'), 'AND')) or renamed_con.get(((f'y{num}', f'x{num}'), 'AND'))

        if xor_output is None or and_output is None:
            print(f'Inconsistency found at x{num} and y{num}')
            break

        print(f'x{num} XOR y{num} -> {xor_output}')
        print(f'x{num} AND y{num} -> {and_output}')
        print()
    else:
        xor_output_1 = renamed_con.get(((f'x{num}', f'y{num}'), 'XOR')) or renamed_con.get(((f'y{num}', f'x{num}'), 'XOR'))
        and_output_1 = renamed_con.get(((f'x{num}', f'y{num}'), 'AND')) or renamed_con.get(((f'y{num}', f'x{num}'), 'AND'))
        xor_output_2 = renamed_con.get(((f'HALFSUM{num}', f'CARRY{prev_num}'), 'XOR')) or renamed_con.get(((f'CARRY{prev_num}', f'HALFSUM{num}'), 'XOR'))
        and_output_2 = renamed_con.get(((f'HALFSUM{num}', f'CARRY{prev_num}'), 'AND')) or renamed_con.get(((f'CARRY{prev_num}', f'HALFSUM{num}'), 'AND'))
        or_output = renamed_con.get(((f'1STCARRY{num}', f'2NDCARRY{num}'), 'OR')) or renamed_con.get(((f'2NDCARRY{num}', f'1STCARRY{num}'), 'OR'))

        if xor_output_1 is None or and_output_1 is None or xor_output_2 is None or and_output_2 is None or or_output is None:
            print(f'#################')
            print(f'Inconsistency found at x{num} and y{num}')
            print(f'x{num} XOR y{num} -> {xor_output_1}')
            print(f'x{num} AND y{num} -> {and_output_1}')
            print(f'HALFSUM{num} XOR CARRY{prev_num} -> {xor_output_2}')
            print(f'HALFSUM{num} AND CARRY{prev_num} -> {and_output_2}')
            print(f'1STCARRY{num} OR 2NDCARRY{num} -> {or_output}')
            print(f'#################')
            break

        print(f'x{num} XOR y{num} -> {xor_output_1}')
        print(f'x{num} AND y{num} -> {and_output_1}')
        print(f'HALFSUM{num} XOR CARRY{prev_num} -> {xor_output_2}')
        print(f'HALFSUM{num} AND CARRY{prev_num} -> {and_output_2}')
        print(f'1STCARRY{num} OR 2NDCARRY{num} -> {or_output}')
        print()

# %%
print(','.join(sorted(['ksv', 'z06', 'kbs', 'nbd', 'z20', 'tqq', 'z39', 'ckb'])))


