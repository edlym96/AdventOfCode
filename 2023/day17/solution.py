#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from heapq import heappop, heappush

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    heat_map = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            heat_map.append([int(elem) for elem in line.strip().rstrip()])
    return heat_map

def traverse_heat_map(heat_map, min_step, max_step) -> int:
    queue = [(0, 0, 0, (0, 0))]
    seen = set()
    while len(queue):
        step_heat_loss, step_row, step_col, (dir_row, dir_col) = heappop(queue)
        if step_row == len(heat_map)-1 and step_col == len(heat_map[0])-1:
            return step_heat_loss
        
        if (step_row, step_col, dir_row, dir_col) in seen:
            continue
        
        seen.add((step_row, step_col, dir_row, dir_col))

        for d_row, d_col in {(0,1), (1, 0), (-1, 0), (0, -1)} - {(dir_row, dir_col), (-dir_row, -dir_col)}:
            curr_step_heat_loss = step_heat_loss
            for count in range(1, max_step + 1):
                row = step_row + d_row * count
                col = step_col + d_col * count
                if row < 0 or row >= len(heat_map) or col < 0 or col >= len(heat_map[0]):
                    break
                curr_step_heat_loss += heat_map[row][col]
                if count >= min_step:
                    heappush(queue, (curr_step_heat_loss, row, col, (d_row, d_col)))


def solve_part1(heat_map) -> int:
    heat_loss = traverse_heat_map(heat_map, 1, 3)
    return heat_loss

def solve_part2(heat_map) -> int:
    heat_loss = traverse_heat_map(heat_map, 4, 10)
    return heat_loss

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    heat_map = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(heat_map)}")
    # part 2
    print(f"Result for part 2: {solve_part2(heat_map)}")
