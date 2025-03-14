#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Convert direct coordination to cartesian. Written by Qiang, modified for Python 3 by Moly.

import sys
import os
import numpy as np

print("Please read the head part of this script and get more information!")
print("""
###################################
#                                 #
# for VASP 5.2 or higher versions  #
#                                 #
###################################
""")

if len(sys.argv) <= 1:
    print('\n' + ' Warning! ' * 3 + '\n')
    print('You did not select the input file to be converted.\nBy default, we are going to convert your CONTCAR.\n')
    
    if not os.path.isfile("POSCAR") and not os.path.isfile("CONTCAR"):
        print("Error:" * 3 + "\nCannot find either POSCAR or CONTCAR!\n")
        sys.exit()
    else:
        file_to_be_converted = "CONTCAR" if os.path.isfile("CONTCAR") else "POSCAR"
        print(f"\nConversion starts for {file_to_be_converted}...\n")
else:
    file_to_be_converted = sys.argv[1]
    print(f"\nConversion starts for {file_to_be_converted}...\n")
    
fixedlayer = int(sys.argv[2]) if len(sys.argv) > 2 else None

def get_infor():
    with open(file_to_be_converted, 'r') as f:
        lines = f.readlines()
    
    num_atoms = sum(map(int, lines[6].split()))
    start_num = 9 if lines[7][0].lower() == 's' else 8
    is_direct = lines[start_num - 1][0].lower() == 'd'
    
    if start_num == 8:
        print('-' * 52)
        print(f'Pay Attention! There is no TTT in {file_to_be_converted}')
        print('-' * 52)
    
    vector = np.array([list(map(float, lines[i].split())) for i in range(2, 5)]) if is_direct else np.eye(3)
    
    return vector, lines, start_num, num_atoms, is_direct

def determine_layers(z_cartesian, threshold=0.5):
    sorted_z = sorted(z_cartesian)
    layer_sets = [sorted_z[0]]
    layers = {}
    
    for val in sorted_z:
        if abs(val - layer_sets[-1]) >= threshold:
            layer_sets.append(val)
    
    for i, layer in enumerate(layer_sets, 1):
        layers[i] = [idx for idx, z in enumerate(z_cartesian) if abs(z - layer) <= threshold]
    
    return layers

def convert():
    coords = np.array([list(map(float, lines[i].split()[:3])) for i in range(start_num, start_num + num_atoms)])
    cartesian_coords = coords @ vector
    
    tf = [lines[i].split()[3:] if start_num == 9 else [' '] for i in range(start_num, start_num + num_atoms)]
    layers = determine_layers(cartesian_coords[:, 2])
    
    print(f'\nFind {len(layers)} layers! ' * 3)
    
    with open(f"{file_to_be_converted}_C", 'w') as file_out:
        file_out.writelines(lines[:7])
        if fixedlayer is not None:
            file_out.write("Selective\nCartesian\n")
            for i in range(1, len(layers) + 1):
                for j in layers[i]:
                    tf[j] = ['F', 'F', 'F'] if i <= fixedlayer else ['T', 'T', 'T']
        else:
            file_out.write("Selective\nCartesian\n" if start_num == 9 else "Cartesian\n")
        
        for i, (x, y, z) in enumerate(cartesian_coords):
            file_out.write(f"\t{x:+.10f}   {y:+.10f}   {z:+.10f}  {' '.join(tf[i])}\n")

vector, lines, start_num, num_atoms, is_direct = get_infor()

if is_direct:
    print(f"\n{file_to_be_converted} has Direct Coordinates, Conversion starts.... ")
    convert()
else:
    print(f"\n{file_to_be_converted} has Cartesian Coordinates already! We are going to fix layers only.")
    convert()

print('-' * 53)
print(f'\n{file_to_be_converted} with Cartesian Coordinates is named as {file_to_be_converted}_C\n')
print('-' * 53)
