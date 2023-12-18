#!/usr/bin/env python3
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
from heapq import heappop, heappush

FILEPATH = str(Path(__file__).parent / 'input.txt')

# https://stackoverflow.com/a/30408825
def shoelace_formula_area(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def load_txt(filepath) -> list[list[str]]:
    instructions = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            direction, steps, color = line.strip().rstrip().split(' ')
            steps = int(steps)
            color = color[1:-1]
            instructions.append((direction, steps, color))
    return instructions

def parse_hex_to_instruction(hex_string) -> tuple:
    dir_map = {'0':'R', '1':'D', '2':'L', '3':'U'}
    hex_string = hex_string.replace('#', '0x')
    direction = dir_map[hex_string[-1]]
    hex_string = hex_string[:-1]
    steps = int(hex_string, 16)
    return direction, steps

def build_vertices(instructions):
    loc = (0, 0)
    xs = []
    ys = []
    dir_map = {"U": (1, 0), "D": (-1, 0), "R": (0, 1), "L": (0, -1)}
    num_pts = 0
    for direction, steps in instructions:
        cur_dir = dir_map[direction]
        cur_len = steps
        num_pts += cur_len 
        loc = (loc[0] + cur_len * cur_dir[0], loc[1] + cur_len * cur_dir[1])
        xs.append(loc[0])
        ys.append(loc[1])
    return xs, ys, num_pts

def solve_part1(instructions) -> int:
    instructions = [(d, s) for d,s,_ in instructions]
    xs, ys, num_points = build_vertices(instructions)
    A = shoelace_formula_area(xs, ys)
    b = num_points
    # A = i + b/2 - 1 -> i = A + 1 - b/2
    # i = internal points
    # b = boundary points
    # A = total area
    assert(b % 2 == 0)
    I = A + 1 - b // 2
    return I + b

def solve_part2(instructions) -> int:
    instructions = [parse_hex_to_instruction(color) for _, _, color in instructions]
    xs, ys, num_points = build_vertices(instructions)
    A = shoelace_formula_area(xs, ys)
    b = num_points
    # A = i + b/2 - 1 -> i = A + 1 - b/2
    # i = internal points
    # b = boundary points
    # A = total area
    assert(b % 2 == 0)
    I = A + 1 - b // 2
    return I + b

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()

    # part 1
    instructions = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(instructions)}")
    # part 2
    print(f"Result for part 2: {solve_part2(instructions)}")
