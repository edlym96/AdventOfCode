#!/usr/bin/env python3
import argparse
from pathlib import Path

FILEPATH = str(Path(__file__).parent / 'input.txt')


def load_txt(filepath) -> list[int]:
    matrix = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            matrix.append(list(line.strip().rstrip()))
    return matrix

def find_symbol_coordinates(matrix):
    symbol_coords = []
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] != '.' and not matrix[row][col].isnumeric():
                symbol_coords.append((row, col))
    return symbol_coords

def find_parts(matrix):
    # Get coordinates of all symbols
    symbol_coords = find_symbol_coordinates(matrix)
    # Store set of seen coordinates
    seen = set()
    score = 0
    all_digits = []
    for row, col in symbol_coords:
        # scan all adjacent squares of symbols
        for row_mod in range(-1, 2):
            for col_mod in range(-1,2):
                row_idx = row+row_mod
                col_idx = col+col_mod
                # check bounds
                if row_idx < 0 or row_idx >= len(matrix) or col_idx < 0 or col_idx >= len(matrix[0]) or (row_mod == 0 and col_mod == 0) :
                    continue
                # if already seen, continue
                if (row_idx, col_idx) in seen:
                    continue
                seen.add((row_idx, col_idx))
                char = matrix[row_idx][col_idx]
                # If adjacent square is numeric, do a dfs to get the full number
                if char.isnumeric():
                    # numbers are horizontal only, dfs left and right side to get the full digit
                    val = int(dfs_left(matrix, seen, row_idx, col_idx-1) + char + dfs_right(matrix, seen, row_idx, col_idx+1))
                    all_digits.append((row_idx, col_idx, val))
                    score += val
    return score

def find_gear_ratio(matrix):
    total = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            # Only care about gears '*' symbol
            if matrix[row][col] == '*':
                adjacents = 0
                vals = []
                seen = set()
                for row_mod in range(-1, 2):
                    for col_mod in range(-1,2):
                        row_idx = row+row_mod
                        col_idx = col+col_mod
                        if row_idx < 0 or row_idx >= len(matrix) or col_idx < 0 or col_idx >= len(matrix[0]) or (row_mod == 0 and col_mod == 0) :
                            continue
                        if (row_idx, col_idx) in seen:
                            continue
                        seen.add((row_idx, col_idx))
                        char = matrix[row_idx][col_idx]
                        if matrix[row_idx][col_idx].isnumeric():
                            vals.append(int(dfs_left(matrix, seen, row_idx, col_idx-1) + char + dfs_right(matrix, seen, row_idx, col_idx+1)))
                            adjacents += 1
                # Only count if there are exactly 2 adjacent numbers
                if adjacents == 2:
                    total += vals[0] * vals[1]
    return total

def dfs_left(matrix, seen, row, col):
    if col < 0 or matrix[row][col] == '.' or not matrix[row][col].isnumeric():
        return ''

    seen.add((row, col))
    return dfs_left(matrix, seen, row, col-1) + matrix[row][col]

def dfs_right(matrix, seen, row, col):
    if col >= len(matrix) or matrix[row][col] == '.' or not matrix[row][col].isnumeric():
        return ''

    seen.add((row, col))
    return matrix[row][col] + dfs_right(matrix, seen, row, col+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    matrix = load_txt(pargs.filepath)
    print(f"Result for part 1: {find_parts(matrix)}")
    # part 2    
    print(f"Result for part 2: {find_gear_ratio(matrix)}")
