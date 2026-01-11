#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple, deque

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[int]:
    galaxy_map = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            galaxy_map.append(list(line.strip().rstrip()))
    return galaxy_map
    
# Find all the empty rows and cols
def get_empty_row_cols(galaxy_map):
    empty_rows = set()
    empty_cols = set()
    for row in range(len(galaxy_map)):
        if all(c == '.' for c in galaxy_map[row]):
            empty_rows.add(row)
    
    for col in range(len(galaxy_map[0])):
        if all(galaxy_map[r][col] == '.' for r in range(len(galaxy_map))):
            empty_cols.add(col)
    
    return empty_rows, empty_cols

# Find positions of all galaxies in the map
def find_galaxy_pos(galaxy_map) -> list[tuple]:
    galaxies = []
    for row in range(len(galaxy_map)):
        for col in range(len(galaxy_map[0])):
            if galaxy_map[row][col] == "#":
                galaxies.append((row, col))
    return galaxies

# Steps from galaxy1 -> galaxy2 is the difference between the row and col positions of the two galaxies + the expansion of any rows and cols between these points
# In part 1, empty rows, cols are doubled in size. In part2, this is a 1000000 multiplier
def get_step(galaxy1, galaxy2, empty_rows, empty_cols, multiplier=2):
    flat_steps = abs(galaxy2[0] - galaxy1[0]) + abs(galaxy2[1] - galaxy1[1])
    min_row = min(galaxy1[0], galaxy2[0])
    max_row = max(galaxy1[0], galaxy2[0])
    min_col = min(galaxy1[1], galaxy2[1])
    max_col = max(galaxy1[1], galaxy2[1])
    for row in empty_rows:
        if min_row < row < max_row:
            flat_steps += 1 * (multiplier - 1)
    for col in empty_cols:
        if min_col < col < max_col:
            flat_steps += 1 * (multiplier - 1)
    return flat_steps

def get_score(galaxy_positions, empty_rows, empty_cols, multiplier=2):
    total_steps = 0
    for i in range(len(galaxy_positions) - 1):
        for j in range(i+1, len(galaxy_positions)):
            step_incr = get_step(galaxy_positions[i], galaxy_positions[j], empty_rows, empty_cols, multiplier)
            total_steps += step_incr
    return total_steps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    galaxy_map = load_txt(pargs.filepath)
    empty_rows, empty_cols = get_empty_row_cols(galaxy_map)
    galaxy_positions = find_galaxy_pos(galaxy_map)
    print(f"Result for part 1: {get_score(galaxy_positions, empty_rows, empty_cols)}")
    # part 2
    print(f"Result for part 2: {get_score(galaxy_positions, empty_rows, empty_cols, 1000000)}")
