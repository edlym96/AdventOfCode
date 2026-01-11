#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from functools import cache

FILEPATH = str(Path(__file__).parent / 'input.txt')
CYCLE_COUNT = 1000000000

def load_txt(filepath) -> list[str]:
    stone_map = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            stone_map.append(line.strip().rstrip())
    return stone_map

def rotate_clock(stone_map):
    return [''.join(row) for row in zip(*stone_map[::-1])]

def rotate_anticlock(stone_map):
    return [''.join(row) for row in zip(*stone_map)][::-1]

def slide(stone_map):
    for row in range(len(stone_map)):
        for _ in range(len(stone_map[row])-1):
            stone_map[row] = stone_map[row].replace('O.', '.O')
    return stone_map

def calc_score(stone_map):
    score = 0
    for i, row in enumerate(stone_map):
        score += (sum(1 for c in row if c == 'O') * (len(stone_map) - i))
    return score

def solve_part1(stone_map):
    stone_map = rotate_clock(stone_map)
    stone_map = slide(stone_map)
    stone_map = rotate_anticlock(stone_map)
    return calc_score(stone_map)

def cycle(stone_map):
    # slide north
    stone_map = slide(rotate_clock(stone_map))
    # slide west
    stone_map = slide(rotate_clock(stone_map))
    # slide south
    stone_map = slide(rotate_clock(stone_map))
    # slide east
    stone_map = slide(rotate_clock(stone_map))
    return stone_map

def solve_part2(stone_map):
    grid_dict = {}
    grid_dict[tuple(stone_map)] = 0
    
    for idx in range(1, CYCLE_COUNT + 1):
        stone_map = cycle(stone_map)
        stone_key = tuple(stone_map)
        if stone_key not in grid_dict:
            grid_dict[stone_key] = idx
        else:
            # pattern found, first find the length of the cycle ie. curr_idx - idx when first encountered pattern
            cycle_length = idx - grid_dict[stone_key]
            # Calculate the offset from when we first encountered pattern. This is remainder of remaining cycle count and cycle length
            target = grid_dict[stone_key] + ((CYCLE_COUNT - grid_dict[stone_key]) % cycle_length)
            # since dict is ordered in python, we get the targeth index inside the grid dict
            stone_map = list(grid_dict.keys())[target]
            break
    return calc_score(stone_map)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    stone_map = load_txt(pargs.filepath)    
    print(f"Result for part 1: {solve_part1(stone_map)}")
    # part 2
    print(f"Result for part 2: {solve_part2(stone_map)}")
