#!/usr/bin/env python3
import numpy as np
import argparse
from pathlib import Path
import math

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    garden = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            garden.append(list(line.strip().rstrip()))

    return garden

def find_start(garden):
    for row in range(len(garden)):
        for col in range(len(garden[0])):
            if garden[row][col] == 'S':
                return row, col

def walk_garden(garden, steps):

    start_row, start_col = find_start(garden)
    step_count = 0
    queue = set([(start_row, start_col)])
    new_queue = set()
    while step_count < steps:
        for row, col in queue:
            if (row + 1 < len(garden)) and garden[row+1][col] != '#':
                new_queue.add((row+1, col))
            if (row - 1 >= 0) and garden[row-1][col] != '#':
                new_queue.add((row-1, col))
            if (col + 1 < len(garden[0])) and garden[row][col+1] != '#':
                new_queue.add((row, col+1))
            if (col - 1 >= 0) and garden[row][col-1] != '#':
                new_queue.add((row, col-1))
        queue = new_queue
        new_queue = set()
        step_count += 1
    return len(queue)

def walk_garden_part2(garden, steps):
    dx = [0,-1,0,1]
    dy = [-1,0,1,0]
    start_row, start_col = find_start(garden)
    step_count = 0
    queue = set([(start_row, start_col)])
    new_queue = set()
    m = len(garden)
    n = len(garden[0])
    while step_count < steps:
        for row, col in queue:
            for k in range(4):
                ni = row+dx[k]
                nj = col+dy[k]
                if garden[ni%n][nj%m] != "#":
                    new_queue.add((ni,nj))
        queue = new_queue
        new_queue = set()
        step_count += 1
    return len(queue)

def solve_part1(garden):
    return walk_garden_part2(garden, 64)

def solve_part2(garden):
    points = [(i, walk_garden_part2(garden, 65 + i * 131)) for i in range(3)]
    # Fit a quadratic polynomial (degree=2) through the points
    coefficients = np.polyfit(*zip(*points), 2)

    # Evaluate the quadratic equation at the given x value
    # 202300 * 131 + 65 = 26501365
    n = 202300
    return math.ceil(coefficients[0] * n**2 + coefficients[1] * n + coefficients[2])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    garden = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(garden)}")    
    # part 2
    print(f"Result for part 2: {solve_part2(garden)}")
