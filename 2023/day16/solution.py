#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import deque

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    mirror_map = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            mirror_map.append(list(line.strip().rstrip()))
    return mirror_map

def project_beam(mirror_map, start_row, start_col, start_dir_row, start_dir_col):
    beam_map = [[0 for _ in range(len(mirror_map[0]))] for _ in range(len(mirror_map))]
    queue = deque([(start_row, start_col, start_dir_row, start_dir_col)])
    # For detecting sycles, foward slah and backward slash mirrors can both be on the 'l' or 'r' side. Cache seen sides
    forward_dict = {}
    backward_dict = {}
    while len(queue):
        row, col, dir_row, dir_col = queue.popleft()
        if row < 0 or row >= len(mirror_map) or col < 0 or col >= len(mirror_map[0]):
            continue
        char = mirror_map[row][col]
        if char == '.':
            queue.append((row + dir_row, col+dir_col, dir_row, dir_col))
        elif char == '/':
            if dir_row == 1:
                dir_row = 0
                dir_col = -1
                if (row, col) in forward_dict and 'l' in forward_dict[(row, col)]:
                    continue
                else:
                    forward_dict.setdefault((row, col), set()).add('l')
            elif dir_row == -1:
                dir_row = 0
                dir_col = 1
                if (row, col) in forward_dict and 'r' in forward_dict[(row, col)]:
                    continue
                else:
                    forward_dict.setdefault((row, col), set()).add('r')
            elif dir_col == 1:
                dir_col = 0
                dir_row = -1
                if (row, col) in forward_dict and 'l' in forward_dict[(row, col)]:
                    continue
                else:
                    forward_dict.setdefault((row, col), set()).add('l')
            elif dir_col == -1:
                dir_col = 0
                dir_row = 1
                if (row, col) in forward_dict and 'r' in forward_dict[(row, col)]:
                    continue
                else:
                    forward_dict.setdefault((row, col), set()).add('r')
            queue.append((row + dir_row, col+dir_col, dir_row, dir_col))
        elif char == '\\':
            if dir_row == 1:
                dir_row = 0
                dir_col = 1
                if (row, col) in backward_dict and 'r' in backward_dict[(row, col)]:
                    continue
                else:
                    backward_dict.setdefault((row, col), set()).add('r')
            elif dir_row == -1:
                dir_row = 0
                dir_col = -1
                if (row, col) in backward_dict and 'l' in backward_dict[(row, col)]:
                    continue
                else:
                    backward_dict.setdefault((row, col), set()).add('l')
            elif dir_col == 1:
                dir_col = 0
                dir_row = 1
                if (row, col) in backward_dict and 'l' in backward_dict[(row, col)]:
                    continue
                else:
                    backward_dict.setdefault((row, col), set()).add('l')
            elif dir_col == -1:
                dir_col = 0
                dir_row = -1
                if (row, col) in backward_dict and 'r' in backward_dict[(row, col)]:
                    continue
                else:
                    backward_dict.setdefault((row, col), set()).add('r')

            queue.append((row + dir_row, col+dir_col, dir_row, dir_col))
        elif char == '|':
            if beam_map[row][col] > 0:
                continue
            if dir_row != 0:
                queue.append((row + dir_row, col+dir_col, dir_row, dir_col))
            else:
                dir_col = 0
                queue.append((row + 1, col+dir_col, 1, dir_col))
                queue.append((row - 1, col+dir_col, -1, dir_col))
        elif char == '-':
            if beam_map[row][col] > 0:
                continue
            if dir_col != 0:
                queue.append((row + dir_row, col+dir_col, dir_row, dir_col))
            else:
                dir_row = 0
                queue.append((row, col+1, dir_row, 1))
                queue.append((row, col-1, dir_row, -1))
        beam_map[row][col] = 1
    return beam_map


def solve_part1(mirror_map) -> int:
    beam_map = project_beam(mirror_map, 0, 0, 0, 1)
    energized = sum(map(sum, beam_map))
    return energized

def solve_part2(mirror_map):
    best = 0
    for row_idx in range(len(mirror_map)):
        # Try every row from the left
        beam_map = project_beam(mirror_map, row_idx, 0, 0, 1)
        energized = sum(map(sum, beam_map))
        best = max(best, energized)

        # Try every row from the right
        beam_map = project_beam(mirror_map, row_idx, len(mirror_map[0])-1, 0, -1)
        energized = sum(map(sum, beam_map))
        best = max(best, energized)

    for col_idx in range(len(mirror_map[0])):
        # Try every row from the top
        beam_map = project_beam(mirror_map, 0, col_idx, 1, 0)
        energized = sum(map(sum, beam_map))
        best = max(best, energized)

        # Try every row from the bottom
        beam_map = project_beam(mirror_map, len(mirror_map) - 1, col_idx, -1, 0)
        energized = sum(map(sum, beam_map))
        best = max(best, energized)

    return best

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    mirror_map = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(mirror_map)}")
    # part 2
    print(f"Result for part 2: {solve_part2(mirror_map)}")
